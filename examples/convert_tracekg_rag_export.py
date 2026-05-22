import json
import re
import argparse
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = Path(
    "/Users/phatttt/Documents/Claude/Projects/KnoSys/TraceKG/data/rag/rag_openai_traces.jsonl"
)
DEFAULT_OUTPUT = ROOT / "output" / "internal_tracekg_rag_openai_graphmemshield.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)
    if not source.exists():
        raise SystemExit(f"missing TraceKG RAG export: {source}")
    output.parent.mkdir(exist_ok=True)

    rows = []
    with source.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))

    with output.open("w", encoding="utf-8") as handle:
        for event in rows:
            record = _event_to_dialogue_record(event)
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    print(f"converted {len(rows)} TraceKG RAG events")
    print(f"source: {source}")
    print(f"output: {output}")


def _event_to_dialogue_record(event: dict[str, Any]) -> dict[str, Any]:
    task_id = str(event["task_id"])
    run_id = str(event["run_id"])
    step = int(event["step"])
    phase = str(event["phase"])
    action = str(event["action"])
    tool = str(event.get("tool") or "none")
    observation = str(event.get("observation") or "")
    outcome = str(event.get("outcome") or "none")
    failure_type = str(event.get("failure_type") or "none")
    observation_node = f"observation:{_compact(observation)}"

    sensitivity = "secret" if phase in {"Act", "Verify", "Report"} else "normal"
    relations = [
        {
            "source": f"agent:{event['agent_id']}",
            "relation": "ran_model",
            "target": f"model:{event['model_id']}",
            "sensitivity": "normal",
        },
        {
            "source": f"task:{task_id}",
            "relation": "has_phase",
            "target": f"phase:{phase}",
            "sensitivity": "normal",
        },
        {
            "source": f"phase:{phase}",
            "relation": "performed_action",
            "target": f"action:{_compact(action)}",
            "sensitivity": "normal",
        },
        {
            "source": f"action:{_compact(action)}",
            "relation": "used_tool",
            "target": f"tool:{tool}",
            "sensitivity": "normal",
        },
        {
            "source": f"task:{task_id}",
            "relation": "observed",
            "target": observation_node,
            "sensitivity": sensitivity,
        },
        {
            "source": observation_node,
            "relation": "event_outcome",
            "target": f"outcome:{outcome}",
            "sensitivity": sensitivity,
        },
        {
            "source": observation_node,
            "relation": "failure_type",
            "target": f"failure:{failure_type}",
            "sensitivity": sensitivity,
        },
    ]
    return {
        "user_id": str(event["agent_id"]),
        "session_id": f"{run_id}:{task_id}",
        "turn_id": f"step-{step}",
        "timestamp": f"2026-05-22T00:{step:02d}:00Z",
        "domain": "approved_internal_rag_trace",
        "text": observation,
        "entities": {
            "task_id": task_id,
            "run_id": run_id,
            "phase": phase,
            "action": action,
            "tool": tool,
            "outcome": outcome,
            "failure_type": failure_type,
        },
        "relations": relations,
    }


def _compact(text: str, *, max_tokens: int = 10) -> str:
    tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
    compact = "-".join(tokens[:max_tokens]) or "empty"
    return compact[:120]


if __name__ == "__main__":
    main()
