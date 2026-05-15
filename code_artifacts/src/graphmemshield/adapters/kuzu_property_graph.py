from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge, MemoryNode


class KuzuPropertyGraphAdapter:
    """Optional Kuzu-backed property graph adapter."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    @staticmethod
    def available() -> bool:
        try:
            import kuzu  # noqa: F401
        except Exception:
            return False
        return True

    def write_graph(self, graph: DynamicMemoryGraph) -> None:
        try:
            import kuzu
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("kuzu package is not installed") from exc

        if self.path.exists() and self.path.is_dir():
            shutil.rmtree(self.path)
        elif self.path.exists():
            self.path.unlink()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        db = kuzu.Database(str(self.path))
        conn = kuzu.Connection(db)
        conn.execute(
            "CREATE NODE TABLE Entity("
            "node_id STRING, label STRING, node_type STRING, "
            "owner_session_id STRING, source_user_id STRING, PRIMARY KEY(node_id))"
        )
        conn.execute(
            "CREATE REL TABLE MemoryEdge("
            "FROM Entity TO Entity, edge_id STRING, relation STRING, "
            "owner_session_id STRING, source_user_id STRING, sensitivity STRING, created_at DOUBLE)"
        )
        for node in graph.nodes:
            conn.execute(
                "CREATE (:Entity {node_id: $node_id, label: $label, node_type: $node_type, "
                "owner_session_id: $owner_session_id, source_user_id: $source_user_id})",
                {
                    "node_id": node.node_id,
                    "label": node.label,
                    "node_type": node.node_type,
                    "owner_session_id": node.owner_session_id or "",
                    "source_user_id": node.source_user_id or "",
                },
            )
        for edge in graph.edges:
            conn.execute(
                "MATCH (a:Entity), (b:Entity) WHERE a.node_id = $source_id AND b.node_id = $target_id "
                "CREATE (a)-[:MemoryEdge {edge_id: $edge_id, relation: $relation, "
                "owner_session_id: $owner_session_id, source_user_id: $source_user_id, "
                "sensitivity: $sensitivity, created_at: $created_at}]->(b)",
                {
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                    "edge_id": edge.edge_id,
                    "relation": edge.relation,
                    "owner_session_id": edge.owner_session_id,
                    "source_user_id": edge.source_user_id or "",
                    "sensitivity": edge.sensitivity,
                    "created_at": float(edge.created_at),
                },
            )

    def summary(self) -> dict[str, Any]:
        try:
            import kuzu
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("kuzu package is not installed") from exc
        db = kuzu.Database(str(self.path))
        conn = kuzu.Connection(db)
        node_count = conn.execute("MATCH (n:Entity) RETURN count(n)").get_next()[0]
        edge_count = conn.execute("MATCH ()-[e:MemoryEdge]->() RETURN count(e)").get_next()[0]
        return {
            "backend": "kuzu_property_graph",
            "nodes": node_count,
            "edges": edge_count,
        }

    def read_graph(self) -> DynamicMemoryGraph:
        try:
            import kuzu
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("kuzu package is not installed") from exc
        graph = DynamicMemoryGraph()
        db = kuzu.Database(str(self.path))
        conn = kuzu.Connection(db)
        nodes = conn.execute("MATCH (n:Entity) RETURN n.node_id, n.label, n.node_type, n.owner_session_id, n.source_user_id")
        while nodes.has_next():
            node_id, label, node_type, owner_session_id, source_user_id = nodes.get_next()
            graph.add_node(
                MemoryNode(
                    node_id=node_id,
                    label=label,
                    node_type=node_type,
                    owner_session_id=owner_session_id or None,
                    source_user_id=source_user_id or None,
                )
            )
        edges = conn.execute(
            "MATCH (a:Entity)-[e:MemoryEdge]->(b:Entity) "
            "RETURN e.edge_id, a.node_id, e.relation, b.node_id, e.owner_session_id, "
            "e.source_user_id, e.sensitivity, e.created_at"
        )
        while edges.has_next():
            edge_id, source_id, relation, target_id, owner_session_id, source_user_id, sensitivity, created_at = edges.get_next()
            graph.add_edge(
                MemoryEdge(
                    edge_id=edge_id,
                    source_id=source_id,
                    relation=relation,
                    target_id=target_id,
                    owner_session_id=owner_session_id,
                    source_user_id=source_user_id or None,
                    sensitivity=sensitivity,
                    created_at=float(created_at),
                )
            )
        return graph
