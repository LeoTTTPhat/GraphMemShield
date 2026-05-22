import csv
import json
import os
import sys
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def main() -> None:
    rows: list[dict[str, Any]] = []
    rows.extend(_load_synthetic_rows())
    rows.extend(_load_single_docker_rows())
    rows.extend(_load_batch_rows())
    rows.extend(_load_cikm_revision_rows())
    rows.extend(_load_multiwoz_rows())
    rows.extend(_load_langgraph_rows())
    rows.extend(_load_mem0_rows())
    rows.extend(_load_deployed_graphrag_rows())
    rows.extend(_load_enron_rows())

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, "aggregate_results.json")
    csv_path = os.path.join(OUTPUT_DIR, "aggregate_results.csv")
    md_path = os.path.join(OUTPUT_DIR, "aggregate_results.md")

    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2)

    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "system",
                "dataset",
                "attack",
                "condition",
                "metric",
                "value",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write(_render_markdown(rows))

    print(f"aggregate rows: {len(rows)}")
    print(f"json: {json_path}")
    print(f"csv: {csv_path}")
    print(f"markdown: {md_path}")


def _load_synthetic_rows() -> list[dict[str, Any]]:
    path = os.path.join(OUTPUT_DIR, "synthetic_experiments.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        records = json.load(handle)
    return [
        _row(
            system="in_memory_simulator",
            dataset="synthetic_multisession",
            attack=record["experiment"],
            condition=record["condition"],
            metric=record["metric"],
            value=record["value"],
            notes=record.get("notes", ""),
        )
        for record in records
    ]


def _load_single_docker_rows() -> list[dict[str, Any]]:
    path = os.path.join(OUTPUT_DIR, "privacyguard_docker_experiment.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [
        _row(
            system="privacyguard-docker",
            dataset="seed_records",
            attack="CrossSessionProbe",
            condition="baseline",
            metric="leaked_edge_count",
            value=payload["baseline"]["leaked_edge_count"],
        ),
        _row(
            system="privacyguard-docker",
            dataset="seed_records",
            attack="CrossSessionProbe",
            condition="baseline",
            metric="leakage_event_count",
            value=payload["baseline"].get("leakage_event_count", ""),
        ),
        _row(
            system="privacyguard-docker",
            dataset="seed_records",
            attack="CrossSessionProbe",
            condition="strict_guard",
            metric="leaked_edge_count",
            value=payload["defended"]["leaked_edge_count"],
        ),
        _row(
            system="privacyguard-docker",
            dataset="seed_records",
            attack="CrossSessionProbe",
            condition="strict_guard",
            metric="leakage_reduction",
            value=payload["defended"]["leakage_reduction"],
            notes="Strict provenance/session isolation blocks cross-session retrieval.",
        ),
    ]


def _load_batch_rows() -> list[dict[str, Any]]:
    path = os.path.join(OUTPUT_DIR, "privacyguard_batch_results.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return list(payload.get("results", []))


def _load_cikm_revision_rows() -> list[dict[str, Any]]:
    path = os.path.join(OUTPUT_DIR, "cikm_revision_results.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [
        _row(
            system=row["system"],
            dataset=row["dataset"],
            attack=row["experiment"],
            condition=row["condition"],
            metric=row["metric"],
            value=row["value"],
            notes="CIKM revision experiment.",
        )
        for row in payload
    ]


def _load_multiwoz_rows() -> list[dict[str, Any]]:
    path = os.path.join(OUTPUT_DIR, "multiwoz_results.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [
        _row(
            system=row["system"],
            dataset=row["dataset"],
            attack=row["experiment"],
            condition=row["condition"],
            metric=row["metric"],
            value=row["value"],
            notes="External MultiWOZ 2.1 corpus run.",
        )
        for row in payload
    ]


def _load_enron_rows() -> list[dict[str, Any]]:
    path = os.path.join(OUTPUT_DIR, "enron_results.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [
        _row(
            system=row["system"],
            dataset=row["dataset"],
            attack=row["experiment"],
            condition=row["condition"],
            metric=row["metric"],
            value=row["value"],
            notes="Enron maildir or Enron-style communication graph run.",
        )
        for row in payload
    ]


def _load_deployed_graphrag_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for filename, dataset, notes in (
        (
            "public_multiwoz_http_trace.json",
            "public_multiwoz_http_trace",
            "Public Proxy GraphRAG Trace: live local HTTP service over MultiWOZ-derived graph memory.",
        ),
        (
            "internal_tracekg_rag_openai_trace.json",
            "approved_internal_openai_rag_trace",
            "Approved Internal OpenAI-RAG Trace: de-identified TraceKG RAG export through the same HTTP audit harness.",
        ),
    ):
        path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        rows.extend(
            _row(
                system=row["system"],
                dataset=dataset,
                attack=row["experiment"],
                condition=row["condition"],
                metric=row["metric"],
                value=row["value"],
                notes=notes,
            )
            for row in payload
        )
    return rows


def _load_langgraph_rows() -> list[dict[str, Any]]:
    path = os.path.join(OUTPUT_DIR, "langgraph_memory_trace.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [
        _row(
            system=row["system"],
            dataset=row["dataset"],
            attack=row["experiment"],
            condition=row["condition"],
            metric=row["metric"],
            value=row["value"],
            notes="Real LangGraph StateGraph memory workflow over the enterprise sensitive graph.",
        )
        for row in payload
    ]


def _load_mem0_rows() -> list[dict[str, Any]]:
    path = os.path.join(OUTPUT_DIR, "mem0_memory_trace.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [
        _row(
            system=row["system"],
            dataset=row["dataset"],
            attack=row["experiment"],
            condition=row["condition"],
            metric=row["metric"],
            value=row["value"],
            notes="Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings.",
        )
        for row in payload
    ]


def _row(
    *,
    system: str,
    dataset: str,
    attack: str,
    condition: str,
    metric: str,
    value: Any,
    notes: str = "",
) -> dict[str, Any]:
    return {
        "system": system,
        "dataset": dataset,
        "attack": attack,
        "condition": condition,
        "metric": metric,
        "value": value,
        "notes": notes,
    }


def _render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# GraphMemShield Aggregate Results",
        "",
        "This table aggregates all currently runnable experiments.",
        "",
        "| System | Dataset | Attack | Condition | Metric | Value | Notes |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['system']} | {row['dataset']} | {row['attack']} | "
            f"{row['condition']} | {row['metric']} | {row['value']} | "
            f"{row.get('notes', '')} |"
        )
    lines.extend(
        [
            "",
            "## Remaining Manual Work",
            "",
            "- Replace de-identified sample data with additional approved public datasets where licensing permits.",
            "- Reproduce the public HTTP trace with `examples/run_deployed_graphrag_trace.py`.",
            "- Reproduce the LangGraph memory integration with `examples/run_langgraph_memory_experiment.py`.",
            "- Reproduce the Mem0 memory integration with `examples/run_mem0_memory_experiment.py` when `OPENAI_API_KEY` is configured.",
            "- Reproduce the approved internal HTTP trace by converting the TraceKG export, setting `GRAPHMEMSHIELD_PRODUCTION_GRAPHRAG_JSONL`, and running `examples/run_deployed_graphrag_trace.py`.",
            "- Run `examples/run_enron_experiment.py` against a full approved Enron maildir by setting `GRAPHMEMSHIELD_ENRON_MAILDIR`.",
            "- Connect the property-graph adapter to a live Neo4j deployment for system-level latency and policy tests.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
