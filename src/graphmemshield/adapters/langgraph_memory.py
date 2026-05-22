from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypedDict

from graphmemshield.core.graph import DynamicMemoryGraph, RetrievalGuard
from graphmemshield.core.types import MemoryEdge, MemoryNode, RetrievalResult


class LangGraphMemoryState(TypedDict, total=False):
    action: str
    edge: MemoryEdge
    query: str
    requester_session_id: str
    max_hops: int
    guard: RetrievalGuard | None
    result: RetrievalResult
    written_edge_id: str


@dataclass
class LangGraphMemoryAdapter:
    """A small real LangGraph workflow around the GraphMemShield memory API."""

    graph: DynamicMemoryGraph

    @classmethod
    def available(cls) -> bool:
        try:
            import langgraph  # noqa: F401
        except Exception:
            return False
        return True

    def __post_init__(self) -> None:
        self._app = self._compile()

    def write_edge(self, edge: MemoryEdge) -> str:
        output = self._app.invoke({"action": "write", "edge": edge})
        return output["written_edge_id"]

    def retrieve(
        self,
        *,
        query: str,
        requester_session_id: str,
        max_hops: int = 1,
        guard: RetrievalGuard | None = None,
    ) -> RetrievalResult:
        output = self._app.invoke(
            {
                "action": "retrieve",
                "query": query,
                "requester_session_id": requester_session_id,
                "max_hops": max_hops,
                "guard": guard,
            }
        )
        return output["result"]

    def load_graph(self, source: DynamicMemoryGraph) -> None:
        for node in source.nodes:
            self.graph.add_node(node)
        for edge in source.edges:
            self.write_edge(edge)

    def _compile(self):
        try:
            from langgraph.graph import END, StateGraph
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("langgraph package is required for this adapter") from exc

        workflow = StateGraph(LangGraphMemoryState)
        workflow.add_node("route", self._route_node)
        workflow.add_node("write_memory", self._write_node)
        workflow.add_node("retrieve_memory", self._retrieve_node)
        workflow.set_entry_point("route")
        workflow.add_conditional_edges(
            "route",
            lambda state: state.get("action", "retrieve"),
            {
                "write": "write_memory",
                "retrieve": "retrieve_memory",
            },
        )
        workflow.add_edge("write_memory", END)
        workflow.add_edge("retrieve_memory", END)
        return workflow.compile()

    def _route_node(self, state: LangGraphMemoryState) -> dict[str, Any]:
        return {}

    def _write_node(self, state: LangGraphMemoryState) -> dict[str, Any]:
        edge = state["edge"]
        self.graph.add_edge(edge)
        if self.graph.get_node(edge.source_id) is None:
            self.graph.add_node(MemoryNode(node_id=edge.source_id, label=edge.source_id))
        if self.graph.get_node(edge.target_id) is None:
            self.graph.add_node(MemoryNode(node_id=edge.target_id, label=edge.target_id))
        return {"written_edge_id": edge.edge_id}

    def _retrieve_node(self, state: LangGraphMemoryState) -> dict[str, Any]:
        result = self.graph.retrieve(
            state.get("query", ""),
            state.get("requester_session_id", ""),
            max_hops=state.get("max_hops", 1),
            guard=state.get("guard"),
        )
        return {"result": result}
