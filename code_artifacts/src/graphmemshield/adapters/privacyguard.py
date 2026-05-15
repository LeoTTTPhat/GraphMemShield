from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge, MemoryNode


@dataclass(frozen=True)
class PrivacyGuardClient:
    """Small stdlib HTTP client for the Dockerized PrivacyGuard mock system."""

    edge_url: str = "http://localhost:3001"
    fog_url: str = "http://localhost:3002"
    cloud_url: str = "http://localhost:3003"
    timeout_seconds: float = 5.0

    def health(self) -> dict[str, Any]:
        return {
            "edge": self._get_json(f"{self.edge_url}/api/health"),
            "fog": self._get_json(f"{self.fog_url}/api/health"),
            "cloud": self._get_json(f"{self.cloud_url}/api/health"),
        }

    def fetch_user_data(self, user_id: str, *, limit: int = 200) -> list[dict[str, Any]]:
        url = (
            f"{self.cloud_url}/api/data/{urllib.parse.quote(user_id)}"
            f"?limit={limit}"
        )
        payload = self._get_json(url)
        return list(payload.get("data", []))

    def _get_json(self, url: str) -> dict[str, Any]:
        with urllib.request.urlopen(url, timeout=self.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))


class PrivacyGuardGraphBuilder:
    """Maps PrivacyGuard userData documents into GraphMemShield memory edges."""

    def build(self, records_by_user: dict[str, list[dict[str, Any]]]) -> DynamicMemoryGraph:
        graph = DynamicMemoryGraph()
        for user_id, records in records_by_user.items():
            graph.add_node(
                MemoryNode(
                    node_id=_node_id("user", user_id),
                    label=user_id,
                    node_type="user",
                    source_user_id=user_id,
                )
            )
            for index, record in enumerate(records):
                self._add_record(graph, user_id, record, index)
        return graph

    def _add_record(
        self,
        graph: DynamicMemoryGraph,
        user_id: str,
        record: dict[str, Any],
        index: int,
    ) -> None:
        metadata = record.get("metadata") or {}
        payload = record.get("payload") or {}
        session_id = metadata.get("sessionId") or f"{user_id}-session"
        turn_id = metadata.get("turnId") or f"record-{index}"
        data_type = record.get("dataType") or metadata.get("dataType") or "unknown"
        sensitivity = _sensitivity_for(data_type, payload)
        source_node = _node_id("user", user_id)
        data_node = _node_id("datatype", data_type)

        graph.add_node(MemoryNode(data_node, data_type, node_type="data_type"))
        self._add_edge(
            graph,
            edge_id=f"{record.get('_id', user_id + '-' + str(index))}:submitted",
            source_id=source_node,
            relation="submitted",
            target_id=data_node,
            owner_session_id=session_id,
            source_user_id=user_id,
            turn_id=turn_id,
            sensitivity=sensitivity,
            created_at=_timestamp_to_float(record.get("timestamp"), index),
        )

        metadata_relations = metadata.get("relations") or []
        if metadata_relations:
            for rel_index, relation in enumerate(metadata_relations):
                source_id = _node_id_from_raw(relation["source"])
                target_id = _node_id_from_raw(relation["target"])
                graph.add_node(
                    MemoryNode(source_id, _label_from_raw(relation["source"]))
                )
                graph.add_node(
                    MemoryNode(target_id, _label_from_raw(relation["target"]))
                )
                self._add_edge(
                    graph,
                    edge_id=(
                        f"{record.get('_id', user_id + '-' + str(index))}:"
                        f"relation:{rel_index}"
                    ),
                    source_id=source_id,
                    relation=relation["relation"],
                    target_id=target_id,
                    owner_session_id=session_id,
                    source_user_id=user_id,
                    turn_id=turn_id,
                    sensitivity=relation.get("sensitivity", sensitivity),
                    created_at=_timestamp_to_float(record.get("timestamp"), index),
                )
            return

        for field_name, value in sorted(payload.items()):
            if value is None or isinstance(value, (dict, list)):
                continue
            value_node = _node_id(field_name, str(value))
            graph.add_node(
                MemoryNode(
                    value_node,
                    str(value),
                    node_type=field_name,
                    owner_session_id=session_id,
                    source_user_id=user_id,
                )
            )
            self._add_edge(
                graph,
                edge_id=f"{record.get('_id', user_id + '-' + str(index))}:{field_name}",
                source_id=source_node,
                relation=_relation_for(field_name),
                target_id=value_node,
                owner_session_id=session_id,
                source_user_id=user_id,
                turn_id=turn_id,
                sensitivity=sensitivity,
                created_at=_timestamp_to_float(record.get("timestamp"), index),
            )

    def _add_edge(self, graph: DynamicMemoryGraph, **kwargs: Any) -> None:
        graph.add_edge(MemoryEdge(**kwargs))


def build_seed_documents() -> list[dict[str, Any]]:
    """De-identified but realistic records for the Docker mock system."""

    return [
        _seed_doc(
            user_id="graphmem-alice",
            session_id="alice-session-1",
            turn_id="t1",
            data_type="HealthVisit",
            payload={
                "clinic": "Heart Clinic",
                "condition": "arrhythmia",
                "heartRate": 118,
                "city": "Melbourne",
            },
            timestamp="2026-05-09T02:00:00.000Z",
        ),
        _seed_doc(
            user_id="graphmem-alice",
            session_id="alice-session-2",
            turn_id="t2",
            data_type="MedicationLog",
            payload={
                "medication": "beta blocker",
                "condition": "arrhythmia",
                "pharmacy": "Central Pharmacy",
                "city": "Melbourne",
            },
            timestamp="2026-05-09T02:05:00.000Z",
        ),
        _seed_doc(
            user_id="graphmem-bob",
            session_id="bob-session-1",
            turn_id="t1",
            data_type="PurchaseRecord",
            payload={
                "merchant": "Laptop Store",
                "item": "work laptop",
                "amount": 1840,
                "city": "Sydney",
            },
            timestamp="2026-05-09T02:10:00.000Z",
        ),
    ]


def _seed_doc(
    *,
    user_id: str,
    session_id: str,
    turn_id: str,
    data_type: str,
    payload: dict[str, Any],
    timestamp: str,
) -> dict[str, Any]:
    return {
        "userId": user_id,
        "policyHash": "graphmemshield-seed-policy",
        "dataType": data_type,
        "payload": payload,
        "dataHash": f"graphmemshield-{user_id}-{session_id}-{turn_id}",
        "timestamp": {"$date": timestamp},
        "retainUntil": {"$date": "2027-05-09T00:00:00.000Z"},
        "metadata": {
            "source": "graphmemshield-docker-seed",
            "sessionId": session_id,
            "turnId": turn_id,
            "dataType": data_type,
        },
    }


def _sensitivity_for(data_type: str, payload: dict[str, Any]) -> str:
    lowered = " ".join([data_type, *payload.keys(), *map(str, payload.values())]).lower()
    if any(term in lowered for term in ("health", "clinic", "condition", "medication", "heart")):
        return "medical"
    if any(term in lowered for term in ("purchase", "amount", "merchant", "invoice")):
        return "financial"
    return "normal"


def _relation_for(field_name: str) -> str:
    return {
        "clinic": "visited",
        "condition": "has_condition",
        "medication": "takes_medication",
        "pharmacy": "uses_pharmacy",
        "merchant": "purchased_from",
        "item": "purchased_item",
        "amount": "paid_amount",
        "city": "located_in",
    }.get(field_name, f"has_{field_name}")


def _node_id(prefix: str, raw: str) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "-" for ch in raw).strip("-")
    while "--" in safe:
        safe = safe.replace("--", "-")
    return f"{prefix}:{safe}"


def _node_id_from_raw(raw: str) -> str:
    if ":" in raw:
        prefix, value = raw.split(":", 1)
        return _node_id(prefix, value)
    return _node_id("entity", raw)


def _label_from_raw(raw: str) -> str:
    return raw.split(":", 1)[-1]


def _timestamp_to_float(timestamp: Any, fallback: int) -> float:
    if isinstance(timestamp, dict):
        if "$date" in timestamp:
            return _timestamp_to_float(timestamp["$date"], fallback)
        if "date" in timestamp:
            return _timestamp_to_float(timestamp["date"], fallback)
    if isinstance(timestamp, str):
        digits = "".join(ch for ch in timestamp if ch.isdigit())
        return float(digits[:14] or fallback)
    return float(fallback)
