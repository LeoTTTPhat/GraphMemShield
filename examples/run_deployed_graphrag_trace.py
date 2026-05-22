import csv
import json
import os
import sys
import threading
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.adapters.sqlite_property_graph import SQLitePropertyGraphAdapter  # noqa: E402
from graphmemshield.attacks.cross_session_probe import ProbeReport  # noqa: E402
from graphmemshield.core.types import RetrievalResult  # noqa: E402
from graphmemshield.datasets.dialogue import (  # noqa: E402
    dialogue_records_to_graph,
    load_dialogue_jsonl,
)
from graphmemshield.defenses.guard import GraphMemGuard, GraphMemGuardPolicy  # noqa: E402
from graphmemshield.evaluation.blackbox import (  # noqa: E402
    EvidenceDumpResponseGenerator,
    LocalAbstractiveResponseGenerator,
    OpenAIChatResponseGenerator,
    ResponseLeakageScorer,
    TemplateResponseGenerator,
)


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"


def main() -> None:
    source_path = Path(
        os.environ.get(
            "GRAPHMEMSHIELD_PRODUCTION_GRAPHRAG_JSONL",
            DATA_DIR / "multiwoz_2_1_sample.jsonl",
        )
    )
    if not source_path.exists():
        raise SystemExit(
            f"missing trace {source_path}; run examples/run_multiwoz_experiment.py "
            "or set GRAPHMEMSHIELD_PRODUCTION_GRAPHRAG_JSONL"
        )

    records = load_dialogue_jsonl(source_path)
    graph = dialogue_records_to_graph(records)

    OUTPUT_DIR.mkdir(exist_ok=True)
    sqlite_path = OUTPUT_DIR / "deployed_graphrag_trace.sqlite"
    adapter = SQLitePropertyGraphAdapter(sqlite_path)
    adapter.write_graph(graph)
    deployed_graph = adapter.read_graph()

    service = AgentMemoryHTTPService(deployed_graph)
    service.start()
    try:
        rows = []
        rows.extend(_dataset_rows(records, deployed_graph, source_path, sqlite_path, service.url))
        rows.extend(_http_probe_rows(service, deployed_graph))
        rows.extend(_response_rows(service, deployed_graph))
        rows.extend(_generator_response_rows(service, deployed_graph))
        rows.extend(_qa_accuracy_rows(service, deployed_graph))
        rows.extend(_case_example_rows(service, deployed_graph))
        rows.extend(_latency_rows(service, deployed_graph))
    finally:
        service.stop()

    _write_json(rows, "deployed_graphrag_trace.json")
    _write_csv(rows, "deployed_graphrag_trace.csv")
    _write_markdown(rows, "deployed_graphrag_trace.md")
    print(f"deployed graphrag rows: {len(rows)}")
    print(f"trace source: {source_path}")
    print(f"sqlite backend: {sqlite_path}")


class AgentMemoryHTTPService:
    """Small live HTTP retrieval surface for deployed-style audit runs."""

    def __init__(self, graph) -> None:
        self.graph = graph
        self.guards = _make_guards()
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    def reset_policy_state(self) -> None:
        self.guards = _make_guards()

    @property
    def url(self) -> str:
        if self._server is None:
            raise RuntimeError("service is not running")
        host, port = self._server.server_address
        return f"http://{host}:{port}"

    def start(self) -> None:
        service = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                parsed = urllib.parse.urlparse(self.path)
                if parsed.path != "/retrieve":
                    self.send_error(404)
                    return
                params = urllib.parse.parse_qs(parsed.query)
                query = _one(params, "query", "")
                session_id = _one(params, "session_id", "")
                policy = _one(params, "policy", "global")
                hops = int(_one(params, "hops", "1"))
                guard = service.guards.get(policy)
                result = service.graph.retrieve(
                    query,
                    session_id,
                    max_hops=hops,
                    guard=guard,
                )
                response_text = TemplateResponseGenerator().generate(result)
                payload = _result_payload(result, response_text)
                body = json.dumps(payload, sort_keys=True).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: Any) -> None:
                return

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)

    def retrieve_json(self, *, query: str, session_id: str, hops: int, policy: str) -> dict[str, Any]:
        url = (
            f"{self.url}/retrieve?"
            + urllib.parse.urlencode(
                {
                    "query": query,
                    "session_id": session_id,
                    "hops": str(hops),
                    "policy": policy,
                }
            )
        )
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))


def _http_probe_rows(service: AgentMemoryHTTPService, graph) -> list[dict[str, Any]]:
    victim, attacker = _victim_attacker(graph)
    queries = _queries_for_victim(graph, victim)[:8]
    rows = []
    for policy in _POLICY_ORDER:
        service.reset_policy_state()
        report = _http_probe(
            service,
            attacker_session_id=attacker,
            victim_session_id=victim,
            victim_edge_ids={edge.edge_id for edge in graph.edges_by_session(victim)},
            queries=queries,
            policy=policy,
            hops=2,
        )
        rows.extend(
            [
                _row(policy, "http_cross_session_probe", "queries", report.query_count),
                _row(policy, "http_cross_session_probe", "retrieved_edges", report.retrieved_edge_count),
                _row(policy, "http_cross_session_probe", "unique_retrieved_edges", report.unique_retrieved_edge_count),
                _row(policy, "http_cross_session_probe", "leaked_edges", report.leaked_edge_count),
                _row(policy, "http_cross_session_probe", "leakage_events", report.leakage_event_count),
                _row(policy, "http_cross_session_probe", "per_query_leak_rate", round(report.per_query_leak_rate, 4)),
            ]
        )
    return rows


def _response_rows(service: AgentMemoryHTTPService, graph) -> list[dict[str, Any]]:
    victim, attacker = _victim_attacker(graph)
    victim_edges = graph.edges_by_session(victim)
    query = " ".join(_queries_for_victim(graph, victim)[:4])
    scorer = ResponseLeakageScorer()
    rows = []
    for policy in _POLICY_ORDER:
        service.reset_policy_state()
        payload = service.retrieve_json(
            query=query,
            session_id=attacker,
            hops=2,
            policy=policy,
        )
        retrieved_edge_ids = {edge["edge_id"] for edge in payload["edges"]}
        retrieved_victim_edges = tuple(
            edge for edge in victim_edges if edge.edge_id in retrieved_edge_ids
        )
        report = scorer.score(
            response_text=payload["response_text"],
            victim_edges=retrieved_victim_edges,
            secret_terms=_secret_terms_for_edges(retrieved_victim_edges),
        )
        rows.extend(
            [
                _row(policy, "http_blackbox_response", "response_chars", len(payload["response_text"])),
                _row(policy, "http_blackbox_response", "leaked_edges", report.leaked_edge_count),
                _row(policy, "http_blackbox_response", "leaked_terms", report.leaked_secret_term_count),
            ]
        )
    return rows


def _generator_response_rows(service: AgentMemoryHTTPService, graph) -> list[dict[str, Any]]:
    victim, attacker = _victim_attacker(graph)
    victim_edges = graph.edges_by_session(victim)
    query = " ".join(_queries_for_victim(graph, victim)[:4])
    scorer = ResponseLeakageScorer()
    rows = []
    generators: list[tuple[str, Any]] = [
        ("template", TemplateResponseGenerator()),
        ("local_abstractive", LocalAbstractiveResponseGenerator()),
        ("evidence_dump", EvidenceDumpResponseGenerator()),
    ]
    openai_available = bool(os.environ.get("OPENAI_API_KEY"))
    if openai_available:
        generators.append(("openai", OpenAIChatResponseGenerator()))

    for policy in ("global", "owner_only", "bounded5"):
        service.reset_policy_state()
        payload = service.retrieve_json(
            query=query,
            session_id=attacker,
            hops=2,
            policy=policy,
        )
        result = _retrieval_result_from_payload(graph, payload, max_edges=24)
        retrieved_victim_edges = tuple(
            edge for edge in result.edges if edge.owner_session_id == victim
        )
        secret_terms = _secret_terms_for_edges(retrieved_victim_edges)
        for generator_name, generator in generators:
            try:
                response_text = generator.generate(result)
                status = "ok"
            except Exception as exc:  # pragma: no cover - optional LLM path
                response_text = f"skipped: {type(exc).__name__}"
                status = "skipped"
            if status == "ok":
                report = scorer.score(
                    response_text=response_text,
                    victim_edges=retrieved_victim_edges,
                    secret_terms=secret_terms,
                )
                leaked_edges = report.leaked_edge_count
                leaked_terms = report.leaked_secret_term_count
            else:
                leaked_edges = 0
                leaked_terms = 0
            condition = f"{policy}_{generator_name}"
            rows.extend(
                [
                    _row(condition, "http_generator_response", "status", status),
                    _row(condition, "http_generator_response", "context_edges", len(result.edges)),
                    _row(condition, "http_generator_response", "response_chars", len(response_text)),
                    _row(condition, "http_generator_response", "leaked_edges", leaked_edges),
                    _row(condition, "http_generator_response", "leaked_terms", leaked_terms),
                ]
            )
    if not openai_available:
        rows.append(
            _row("openai", "http_generator_response", "status", "skipped_no_api_key")
        )
    return rows


def _qa_accuracy_rows(service: AgentMemoryHTTPService, graph) -> list[dict[str, Any]]:
    victim, attacker = _victim_attacker(graph)
    victim_edges = graph.edges_by_session(victim)
    queries = _qa_queries(victim_edges)[:24]
    rows = []
    for policy in _POLICY_ORDER:
        service.reset_policy_state()
        hits = 0
        for query, expected_edge_ids in queries:
            payload = service.retrieve_json(
                query=query,
                session_id=attacker,
                hops=2,
                policy=policy,
            )
            retrieved = {edge["edge_id"] for edge in payload["edges"]}
            if retrieved & expected_edge_ids:
                hits += 1
        accuracy = hits / len(queries) if queries else 0.0
        rows.append(_row(policy, "http_graph_qa", "accuracy", round(accuracy, 4)))
    return rows


def _case_example_rows(service: AgentMemoryHTTPService, graph) -> list[dict[str, Any]]:
    victim, attacker = _victim_attacker(graph)
    query = _queries_for_victim(graph, victim)[0]
    examples = []
    for policy, label in (
        ("global", "global_leak"),
        ("owner_only", "owner_only_blocked"),
        ("bounded5", "bounded_partial_sharing"),
    ):
        service.reset_policy_state()
        payload = service.retrieve_json(
            query=query,
            session_id=attacker,
            hops=2,
            policy=policy,
        )
        victim_edges = [
            edge for edge in payload["edges"] if edge["owner_session_id"] == victim
        ]
        edges = victim_edges[:2] if victim_edges else payload["edges"][:2]
        snippet = "; ".join(
            f"{edge['source_id']} {edge['relation']} {edge['target_id']}"
            for edge in edges
        )
        examples.append(
            _row(label, "http_case_examples", "snippet", _shorten(snippet, 180))
        )
        examples.append(
            _row(label, "http_case_examples", "victim_edges_in_response", len(victim_edges))
        )
    return examples


def _latency_rows(service: AgentMemoryHTTPService, graph) -> list[dict[str, Any]]:
    _, attacker = _victim_attacker(graph)
    queries = _queries_for_victim(graph, _victim_attacker(graph)[0])[:5] * 4
    rows = []
    for policy in ("global", "owner_only", "bounded5"):
        service.reset_policy_state()
        start = time.perf_counter()
        for query in queries:
            service.retrieve_json(query=query, session_id=attacker, hops=2, policy=policy)
        elapsed_ms = 1000.0 * (time.perf_counter() - start) / len(queries)
        rows.append(_row(policy, "http_latency", "mean_ms_per_query", round(elapsed_ms, 4)))
    return rows


def _http_probe(
    service: AgentMemoryHTTPService,
    *,
    attacker_session_id: str,
    victim_session_id: str,
    victim_edge_ids: set[str],
    queries: tuple[str, ...],
    policy: str,
    hops: int,
) -> ProbeReport:
    retrieved = []
    leaked = []
    events = 0
    queries_with_leak = 0
    for query in queries:
        payload = service.retrieve_json(
            query=query,
            session_id=attacker_session_id,
            hops=hops,
            policy=policy,
        )
        edge_ids = [edge["edge_id"] for edge in payload["edges"]]
        retrieved.extend(edge_ids)
        query_leaks = [edge_id for edge_id in edge_ids if edge_id in victim_edge_ids]
        if query_leaks:
            queries_with_leak += 1
        events += len(query_leaks)
        leaked.extend(query_leaks)
    unique_retrieved = set(retrieved)
    unique_leaked = tuple(sorted(set(leaked)))
    return ProbeReport(
        attacker_session_id=attacker_session_id,
        victim_session_id=victim_session_id,
        query_count=len(queries),
        retrieved_edge_count=len(retrieved),
        unique_retrieved_edge_count=len(unique_retrieved),
        leaked_edge_count=len(unique_leaked),
        unique_leaked_edge_count=len(unique_leaked),
        leakage_event_count=events,
        leaked_edge_ids=unique_leaked,
        leakage_rate=len(unique_leaked) / len(unique_retrieved) if unique_retrieved else 0.0,
        event_leakage_rate=events / len(retrieved) if retrieved else 0.0,
        per_query_leak_rate=queries_with_leak / len(queries) if queries else 0.0,
        results=tuple(),
    )


def _dataset_rows(records, graph, source_path: Path, sqlite_path: Path, service_url: str) -> list[dict[str, Any]]:
    trace_mode = (
        "user_supplied_production_jsonl"
        if os.environ.get("GRAPHMEMSHIELD_PRODUCTION_GRAPHRAG_JSONL")
        else "public_multiwoz_proxy"
    )
    return [
        _row("deployed_http_agent_memory", "dataset", "trace_mode", trace_mode),
        _row("deployed_http_agent_memory", "dataset", "approved_internal_deployment_trace", trace_mode == "user_supplied_production_jsonl"),
        _row("deployed_http_agent_memory", "dataset", "source_path", str(source_path)),
        _row("deployed_http_agent_memory", "dataset", "records", len(records)),
        _row("deployed_http_agent_memory", "dataset", "users", len({r.user_id for r in records})),
        _row("deployed_http_agent_memory", "dataset", "sessions", len({r.session_id for r in records})),
        _row("deployed_http_agent_memory", "dataset", "nodes", len(graph.nodes)),
        _row("deployed_http_agent_memory", "dataset", "edges", len(graph.edges)),
        _row("deployed_http_agent_memory", "backend", "sqlite_path", str(sqlite_path)),
        _row("deployed_http_agent_memory", "backend", "http_service", service_url),
    ]


def _result_payload(result: RetrievalResult, response_text: str) -> dict[str, Any]:
    return {
        "query": result.query,
        "requester_session_id": result.requester_session_id,
        "edge_count": result.edge_count,
        "cross_session_edge_count": result.cross_session_edge_count,
        "edges": [
            {
                "edge_id": edge.edge_id,
                "source_id": edge.source_id,
                "relation": edge.relation,
                "target_id": edge.target_id,
                "owner_session_id": edge.owner_session_id,
                "sensitivity": edge.sensitivity,
            }
            for edge in result.edges
        ],
        "response_text": response_text,
    }


class LabelOnlyGuard:
    def __init__(self, blocked: frozenset[str]) -> None:
        self.blocked = blocked

    def allow_edge(self, edge, requester_session_id: str) -> bool:
        return edge.sensitivity not in self.blocked

    def record_exposure(self, edge, requester_session_id: str) -> None:
        return


class OwnerLevelBudgetGuard:
    def __init__(self, *, budget: int, blocked: frozenset[str]) -> None:
        self.budget = budget
        self.blocked = blocked
        self._admitted_by_owner: dict[str, set[str]] = {}

    def allow_edge(self, edge, requester_session_id: str) -> bool:
        if edge.owner_session_id == requester_session_id:
            return True
        if edge.sensitivity in self.blocked:
            return False
        admitted = self._admitted_by_owner.get(edge.owner_session_id, set())
        return edge.edge_id in admitted or len(admitted) < self.budget

    def record_exposure(self, edge, requester_session_id: str) -> None:
        if edge.owner_session_id == requester_session_id:
            return
        self._admitted_by_owner.setdefault(edge.owner_session_id, set()).add(edge.edge_id)


def _make_guards() -> dict[str, Any]:
    blocked = frozenset({"medical", "financial", "secret"})
    owner_only = GraphMemGuard(GraphMemGuardPolicy())
    return {
        "strict": owner_only,
        "owner_only": owner_only,
        "label_only": LabelOnlyGuard(blocked),
        "owner_label": GraphMemGuard(
            GraphMemGuardPolicy(
                allow_cross_session=True,
                max_cross_session_edges_per_pair=10**9,
                blocked_sensitivity_labels=blocked,
            )
        ),
        "bounded5": GraphMemGuard(
            GraphMemGuardPolicy(
                allow_cross_session=True,
                max_cross_session_edges_per_pair=5,
                blocked_sensitivity_labels=blocked,
            )
        ),
        "owner_level_budget": OwnerLevelBudgetGuard(budget=5, blocked=blocked),
    }


_POLICY_ORDER = (
    "global",
    "owner_only",
    "label_only",
    "owner_label",
    "bounded5",
    "owner_level_budget",
)


def _retrieval_result_from_payload(graph, payload: dict[str, Any], max_edges: int) -> RetrievalResult:
    edge_ids = [edge["edge_id"] for edge in payload["edges"][:max_edges]]
    edges = tuple(edge for edge_id in edge_ids if (edge := graph.get_edge(edge_id)) is not None)
    node_ids = sorted({edge.source_id for edge in edges} | {edge.target_id for edge in edges})
    nodes = tuple(node for node_id in node_ids if (node := graph.get_node(node_id)) is not None)
    return RetrievalResult(
        query=payload["query"],
        requester_session_id=payload["requester_session_id"],
        edges=edges,
        nodes=nodes,
    )


def _qa_queries(victim_edges) -> tuple[tuple[str, set[str]], ...]:
    by_query: dict[str, set[str]] = {}
    for edge in victim_edges:
        for raw in (edge.target_id, edge.relation):
            for term in raw.replace("-", " ").replace("_", " ").split():
                if len(term) < 4:
                    continue
                by_query.setdefault(term, set()).add(edge.edge_id)
    return tuple((query, edge_ids) for query, edge_ids in by_query.items())


def _victim_attacker(graph) -> tuple[str, str]:
    sessions = sorted({edge.owner_session_id for edge in graph.edges})
    return sessions[0], sessions[1]


def _queries_for_victim(graph, victim: str) -> tuple[str, ...]:
    terms = []
    for edge in graph.edges_by_session(victim):
        for raw in (edge.target_id, edge.relation):
            for term in raw.replace("-", " ").replace("_", " ").split():
                if len(term) >= 4 and term not in terms:
                    terms.append(term)
    return tuple(terms or ["hotel", "restaurant"])


def _secret_terms_for_edges(edges) -> tuple[str, ...]:
    terms = []
    for edge in edges:
        for raw in (edge.source_id, edge.target_id, edge.relation):
            for term in raw.replace("-", " ").replace("_", " ").split():
                if len(term) >= 4 and term not in terms:
                    terms.append(term)
    return tuple(terms)


def _shorten(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _one(params: dict[str, list[str]], key: str, default: str) -> str:
    values = params.get(key)
    return values[0] if values else default


def _row(condition: str, experiment: str, metric: str, value: Any) -> dict[str, Any]:
    return {
        "system": "live_http_agent_memory",
        "dataset": "deployed_graphrag_trace",
        "experiment": experiment,
        "condition": condition,
        "metric": metric,
        "value": value,
    }


def _write_json(rows: list[dict[str, Any]], filename: str) -> None:
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2)


def _write_csv(rows: list[dict[str, Any]], filename: str) -> None:
    with (OUTPUT_DIR / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["system", "dataset", "experiment", "condition", "metric", "value"],
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(rows: list[dict[str, Any]], filename: str) -> None:
    lines = [
        "# Deployed-Style Agent-Memory / GraphRAG Trace Experiment",
        "",
        "This experiment starts a live local HTTP retrieval service over a persistent SQLite graph backend.",
        "If `GRAPHMEMSHIELD_PRODUCTION_GRAPHRAG_JSONL` is unset, it uses the public MultiWOZ-derived graph-memory trace.",
        "",
        "| System | Dataset | Experiment | Condition | Metric | Value |",
        "|---|---|---|---|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['system']} | {row['dataset']} | {row['experiment']} | "
            f"{row['condition']} | {row['metric']} | {row['value']} |"
        )
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
