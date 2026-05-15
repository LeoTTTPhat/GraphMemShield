from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge, MemoryNode


@dataclass(frozen=True)
class DialogueRelation:
    source: str
    relation: str
    target: str
    sensitivity: str = "normal"


@dataclass(frozen=True)
class DialogueRecord:
    user_id: str
    session_id: str
    turn_id: str
    timestamp: str
    domain: str
    text: str
    entities: dict[str, Any]
    relations: tuple[DialogueRelation, ...]


def load_dialogue_jsonl(path: str | Path) -> list[DialogueRecord]:
    records: list[DialogueRecord] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            records.append(_parse_record(payload, line_number))
    return records


def dialogue_records_to_graph(records: Iterable[DialogueRecord]) -> DynamicMemoryGraph:
    graph = DynamicMemoryGraph()
    for record in records:
        user_node = _node_id(f"user:{record.user_id}")
        graph.add_node(
            MemoryNode(
                user_node,
                record.user_id,
                node_type="user",
                owner_session_id=record.session_id,
                source_user_id=record.user_id,
            )
        )
        for name, value in record.entities.items():
            raw_node = f"{name}:{value}"
            graph.add_node(
                MemoryNode(
                    _node_id(raw_node),
                    str(value),
                    node_type=name,
                    owner_session_id=record.session_id,
                    source_user_id=record.user_id,
                )
            )
        for index, relation in enumerate(record.relations):
            source_id = _node_id(relation.source)
            target_id = _node_id(relation.target)
            graph.add_node(MemoryNode(source_id, _label_from_raw(relation.source)))
            graph.add_node(MemoryNode(target_id, _label_from_raw(relation.target)))
            graph.add_edge(
                MemoryEdge(
                    edge_id=f"{record.session_id}:{record.turn_id}:{index}",
                    source_id=source_id,
                    relation=relation.relation,
                    target_id=target_id,
                    owner_session_id=record.session_id,
                    source_user_id=record.user_id,
                    turn_id=record.turn_id,
                    sensitivity=relation.sensitivity,
                    created_at=_timestamp_to_float(record.timestamp),
                    metadata={"domain": record.domain, "text": record.text},
                )
            )
    return graph


def dialogue_records_to_privacyguard_docs(
    records: Iterable[DialogueRecord],
) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []
    for record in records:
        docs.append(
            {
                "userId": record.user_id,
                "policyHash": "graphmemshield-dialogue-policy",
                "dataType": record.domain,
                "payload": record.entities,
                "dataHash": f"graphmemshield-{record.session_id}-{record.turn_id}",
                "timestamp": {"$date": record.timestamp.replace("Z", ".000Z")},
                "retainUntil": {"$date": "2027-05-09T00:00:00.000Z"},
                "metadata": {
                    "source": "graphmemshield-dialogue-jsonl",
                    "sessionId": record.session_id,
                    "turnId": record.turn_id,
                    "dataType": record.domain,
                    "text": record.text,
                    "relations": [
                        {
                            "source": relation.source,
                            "relation": relation.relation,
                            "target": relation.target,
                            "sensitivity": relation.sensitivity,
                        }
                        for relation in record.relations
                    ],
                },
            }
        )
    return docs


def session_ids(records: Iterable[DialogueRecord]) -> tuple[str, ...]:
    return tuple(sorted({record.session_id for record in records}))


def user_ids(records: Iterable[DialogueRecord]) -> tuple[str, ...]:
    return tuple(sorted({record.user_id for record in records}))


def _parse_record(payload: dict[str, Any], line_number: int) -> DialogueRecord:
    required = ("user_id", "session_id", "turn_id", "timestamp", "domain", "text")
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"line {line_number}: missing required keys {missing}")

    return DialogueRecord(
        user_id=payload["user_id"],
        session_id=payload["session_id"],
        turn_id=payload["turn_id"],
        timestamp=payload["timestamp"],
        domain=payload["domain"],
        text=payload["text"],
        entities=dict(payload.get("entities") or {}),
        relations=tuple(
            DialogueRelation(
                source=item["source"],
                relation=item["relation"],
                target=item["target"],
                sensitivity=item.get("sensitivity", "normal"),
            )
            for item in payload.get("relations", [])
        ),
    )


def _node_id(raw: str) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "-" for ch in raw).strip("-")
    while "--" in safe:
        safe = safe.replace("--", "-")
    return safe


def _label_from_raw(raw: str) -> str:
    return raw.split(":", 1)[-1]


def _timestamp_to_float(timestamp: str) -> float:
    digits = "".join(ch for ch in timestamp if ch.isdigit())
    return float(digits[:14] or 0)
