from __future__ import annotations

from pathlib import Path
from typing import Any

from graphmemshield.core.graph import DynamicMemoryGraph, RetrievalGuard
from graphmemshield.core.types import MemoryEdge, RetrievalResult


class Mem0MemoryAdapter:
    """Mem0-backed memory index with GraphMemShield provenance filtering."""

    def __init__(
        self,
        *,
        graph: DynamicMemoryGraph,
        storage_dir: str | Path,
        collection_name: str = "graphmemshield_mem0",
        shared_user_id: str = "graphmemshield_shared",
        embedding_model: str = "text-embedding-3-small",
    ) -> None:
        self.graph = graph
        self.storage_dir = Path(storage_dir)
        self.collection_name = collection_name
        self.shared_user_id = shared_user_id
        self.embedding_model = embedding_model
        self._memory = self._make_memory()

    @classmethod
    def available(cls) -> bool:
        try:
            import mem0  # noqa: F401
        except Exception:
            return False
        return True

    def add_edge(self, edge: MemoryEdge) -> None:
        self._memory.add(
            _edge_text(edge),
            user_id=self.shared_user_id,
            run_id=edge.owner_session_id,
            metadata={
                "edge_id": edge.edge_id,
                "owner_session_id": edge.owner_session_id,
                "sensitivity": edge.sensitivity,
            },
            infer=False,
        )

    def load_edges(self, edges) -> None:
        for edge in edges:
            self.add_edge(edge)

    def search(
        self,
        *,
        query: str,
        requester_session_id: str,
        top_k: int = 20,
        guard: RetrievalGuard | None = None,
    ) -> RetrievalResult:
        payload = self._memory.search(
            query,
            filters={"user_id": self.shared_user_id},
            top_k=top_k,
        )
        visible_edges = []
        for item in payload.get("results", []):
            edge_id = item.get("metadata", {}).get("edge_id")
            edge = self.graph.get_edge(edge_id) if edge_id else None
            if edge is None:
                continue
            if guard is not None and not guard.allow_edge(edge, requester_session_id):
                continue
            visible_edges.append(edge)
            if guard is not None:
                guard.record_exposure(edge, requester_session_id)
        node_ids = sorted({edge.source_id for edge in visible_edges} | {edge.target_id for edge in visible_edges})
        nodes = tuple(node for node_id in node_ids if (node := self.graph.get_node(node_id)) is not None)
        return RetrievalResult(
            query=query,
            requester_session_id=requester_session_id,
            edges=tuple(visible_edges),
            nodes=nodes,
        )

    def _make_memory(self):
        try:
            from mem0 import Memory
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("mem0ai package is required for this adapter") from exc

        self.storage_dir.mkdir(parents=True, exist_ok=True)
        config: dict[str, Any] = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "path": str(self.storage_dir / "qdrant"),
                    "collection_name": self.collection_name,
                    "embedding_model_dims": 1536,
                },
            },
            "history_db_path": str(self.storage_dir / "history.db"),
            "llm": {"provider": "openai", "config": {"model": "gpt-4.1-mini"}},
            "embedder": {"provider": "openai", "config": {"model": self.embedding_model}},
        }
        return Memory.from_config(config)


def _edge_text(edge: MemoryEdge) -> str:
    return (
        f"{edge.source_id} {edge.relation.replace('_', ' ')} {edge.target_id}. "
        f"Sensitivity: {edge.sensitivity}. Owner session: {edge.owner_session_id}."
    )
