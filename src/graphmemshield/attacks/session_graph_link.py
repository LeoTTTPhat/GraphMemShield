from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import sqrt
from typing import Iterable

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge


@dataclass(frozen=True)
class SessionLinkCandidate:
    session_id: str
    score: float
    shared_features: tuple[str, ...]


@dataclass(frozen=True)
class SessionLinkReport:
    query_session_id: str
    candidates: tuple[SessionLinkCandidate, ...]

    @property
    def top_session_id(self) -> str | None:
        return self.candidates[0].session_id if self.candidates else None


class SessionGraphLink:
    """Ranks candidate sessions by local graph-structure similarity."""

    def __init__(self, graph: DynamicMemoryGraph) -> None:
        self.graph = graph

    def rank(
        self,
        *,
        query_session_id: str,
        candidate_session_ids: Iterable[str],
        include_semantic_labels: bool = False,
    ) -> SessionLinkReport:
        query_features = session_feature_vector(
            self.graph.edges_by_session(query_session_id),
            include_semantic_labels=include_semantic_labels,
        )
        candidates: list[SessionLinkCandidate] = []
        for session_id in candidate_session_ids:
            if session_id == query_session_id:
                continue
            candidate_features = session_feature_vector(
                self.graph.edges_by_session(session_id),
                include_semantic_labels=include_semantic_labels,
            )
            score = cosine_similarity(query_features, candidate_features)
            shared = tuple(
                sorted(set(query_features).intersection(candidate_features))[:10]
            )
            candidates.append(
                SessionLinkCandidate(
                    session_id=session_id,
                    score=score,
                    shared_features=shared,
                )
            )

        ranked = tuple(
            sorted(candidates, key=lambda item: (-item.score, item.session_id))
        )
        return SessionLinkReport(query_session_id=query_session_id, candidates=ranked)


def session_feature_vector(
    edges: Iterable[MemoryEdge], *, include_semantic_labels: bool
) -> Counter[str]:
    edges = tuple(sorted(edges, key=lambda edge: (edge.created_at, edge.edge_id)))
    degree: Counter[str] = Counter()
    features: Counter[str] = Counter()

    for edge in edges:
        degree[edge.source_id] += 1
        degree[edge.target_id] += 1
        features[f"relation:{edge.relation}"] += 1
        features[f"sensitivity:{edge.sensitivity}"] += 1
        if edge.turn_id:
            features[f"turn-prefix:{edge.turn_id.split('-')[0]}"] += 1
        if include_semantic_labels:
            features[f"source:{edge.source_id}"] += 1
            features[f"target:{edge.target_id}"] += 1

    for left, right in zip(edges, edges[1:]):
        features[f"relation-bigram:{left.relation}>{right.relation}"] += 1
        features[f"sensitivity-bigram:{left.sensitivity}>{right.sensitivity}"] += 1

    relation_set = sorted({edge.relation for edge in edges})
    for left_index, left in enumerate(relation_set):
        for right in relation_set[left_index + 1 :]:
            features[f"relation-cooccur:{left}|{right}"] += 1

    for node_degree in degree.values():
        features[f"degree:{node_degree}"] += 1

    features[f"edge-count:{len(edges)}"] += 1

    # 1-WL Kernel Feature Extraction
    import hashlib
    from collections import defaultdict
    adj = defaultdict(list)
    node_labels = {}
    for edge in edges:
        adj[edge.source_id].append((edge.target_id, edge.relation))
        adj[edge.target_id].append((edge.source_id, edge.relation))
    
    for node in adj.keys():
        node_labels[node] = str(degree[node])
        
    for node, neighbors in adj.items():
        neighbor_labels = sorted([node_labels[n] + rel for n, rel in neighbors])
        wl_string = node_labels[node] + "|" + "-".join(neighbor_labels)
        wl_hash = hashlib.sha256(wl_string.encode()).hexdigest()[:8]
        features[f"wl1:{wl_hash}"] += 1

    return features


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    shared = set(left).intersection(right)
    numerator = sum(left[key] * right[key] for key in shared)
    left_norm = sqrt(sum(value * value for value in left.values()))
    right_norm = sqrt(sum(value * value for value in right.values()))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return numerator / (left_norm * right_norm)
