from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge, MemoryNode


class SQLitePropertyGraphAdapter:
    """Persistent property-graph adapter backed by SQLite tables."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def write_graph(self, graph: DynamicMemoryGraph) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.executescript(
                """
                drop table if exists edges;
                drop table if exists nodes;
                create table nodes (
                    node_id text primary key,
                    label text not null,
                    node_type text not null,
                    owner_session_id text,
                    source_user_id text,
                    created_at real not null,
                    metadata_json text not null
                );
                create table edges (
                    edge_id text primary key,
                    source_id text not null,
                    relation text not null,
                    target_id text not null,
                    owner_session_id text not null,
                    source_user_id text,
                    turn_id text,
                    sensitivity text not null,
                    created_at real not null,
                    metadata_json text not null
                );
                create index edge_source_idx on edges(source_id);
                create index edge_target_idx on edges(target_id);
                create index edge_owner_idx on edges(owner_session_id);
                """
            )
            db.executemany(
                """
                insert into nodes values (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        node.node_id,
                        node.label,
                        node.node_type,
                        node.owner_session_id,
                        node.source_user_id,
                        node.created_at,
                        json.dumps(node.metadata, sort_keys=True),
                    )
                    for node in graph.nodes
                ],
            )
            db.executemany(
                """
                insert into edges values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        edge.edge_id,
                        edge.source_id,
                        edge.relation,
                        edge.target_id,
                        edge.owner_session_id,
                        edge.source_user_id,
                        edge.turn_id,
                        edge.sensitivity,
                        edge.created_at,
                        json.dumps(edge.metadata, sort_keys=True),
                    )
                    for edge in graph.edges
                ],
            )

    def read_graph(self) -> DynamicMemoryGraph:
        graph = DynamicMemoryGraph()
        with sqlite3.connect(self.path) as db:
            db.row_factory = sqlite3.Row
            for row in db.execute("select * from nodes order by node_id"):
                graph.add_node(
                    MemoryNode(
                        node_id=row["node_id"],
                        label=row["label"],
                        node_type=row["node_type"],
                        owner_session_id=row["owner_session_id"],
                        source_user_id=row["source_user_id"],
                        created_at=row["created_at"],
                        metadata=_json(row["metadata_json"]),
                    )
                )
            for row in db.execute("select * from edges order by edge_id"):
                graph.add_edge(
                    MemoryEdge(
                        edge_id=row["edge_id"],
                        source_id=row["source_id"],
                        relation=row["relation"],
                        target_id=row["target_id"],
                        owner_session_id=row["owner_session_id"],
                        source_user_id=row["source_user_id"],
                        turn_id=row["turn_id"],
                        sensitivity=row["sensitivity"],
                        created_at=row["created_at"],
                        metadata=_json(row["metadata_json"]),
                    )
                )
        return graph

    def summary(self) -> dict[str, Any]:
        with sqlite3.connect(self.path) as db:
            node_count = db.execute("select count(*) from nodes").fetchone()[0]
            edge_count = db.execute("select count(*) from edges").fetchone()[0]
            session_count = db.execute(
                "select count(distinct owner_session_id) from edges"
            ).fetchone()[0]
        return {
            "backend": "sqlite_property_graph",
            "nodes": node_count,
            "edges": edge_count,
            "sessions": session_count,
        }


def _json(payload: str) -> dict[str, Any]:
    parsed = json.loads(payload or "{}")
    return parsed if isinstance(parsed, dict) else {}
