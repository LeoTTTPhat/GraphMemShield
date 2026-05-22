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
        method: str = "cosine",
    ) -> SessionLinkReport:
        query_edges = self.graph.edges_by_session(query_session_id)
        query_features = session_feature_vector(
            query_edges,
            include_semantic_labels=include_semantic_labels,
        )
        candidates: list[SessionLinkCandidate] = []
        for session_id in candidate_session_ids:
            if session_id == query_session_id:
                continue
            candidate_edges = self.graph.edges_by_session(session_id)
            candidate_features = session_feature_vector(
                candidate_edges,
                include_semantic_labels=include_semantic_labels,
            )
            score = _score_sessions(
                query_edges,
                candidate_edges,
                query_features,
                candidate_features,
                method=method,
            )
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


def _score_sessions(
    query_edges: tuple[MemoryEdge, ...],
    candidate_edges: tuple[MemoryEdge, ...],
    query_features: Counter[str],
    candidate_features: Counter[str],
    *,
    method: str,
) -> float:
    if method == "cosine":
        return cosine_similarity(query_features, candidate_features)
    if method == "wl_kernel":
        return cosine_similarity(_prefix_features(query_features, "wl1:"), _prefix_features(candidate_features, "wl1:"))
    if method == "graph_edit":
        return graph_edit_similarity(query_edges, candidate_edges)
    if method == "embedding":
        return cosine_similarity(
            hashed_embedding(query_features),
            hashed_embedding(candidate_features),
        )
    raise ValueError(f"unknown session-link method: {method}")


class LearnedSessionGraphLink:
    """Train a lightweight supervised linker over session-pair graph features."""

    def __init__(
        self,
        graph: DynamicMemoryGraph,
        *,
        include_semantic_labels: bool = False,
        seed: int = 13,
    ) -> None:
        self.graph = graph
        self.include_semantic_labels = include_semantic_labels
        self.seed = seed
        self._model = None
        self._feature_names: tuple[str, ...] = ()

    def fit(self) -> "LearnedSessionGraphLink":
        session_ids = sorted({edge.owner_session_id for edge in self.graph.edges})
        users_by_session = {
            session_id: _session_user(self.graph.edges_by_session(session_id))
            for session_id in session_ids
        }
        features = []
        labels = []
        for left_index, left in enumerate(session_ids):
            for right in session_ids[left_index + 1 :]:
                if users_by_session[left] is None or users_by_session[right] is None:
                    continue
                features.append(self._pair_features(left, right))
                labels.append(int(users_by_session[left] == users_by_session[right]))

        if len(set(labels)) < 2:
            self._model = _ConstantProbabilityModel(sum(labels) / len(labels) if labels else 0.0)
            return self

        self._feature_names = tuple(sorted({name for row in features for name in row}))
        matrix = [[row.get(name, 0.0) for name in self._feature_names] for row in features]
        try:
            from sklearn.linear_model import LogisticRegression  # type: ignore

            model = LogisticRegression(
                class_weight="balanced",
                max_iter=1000,
                random_state=self.seed,
            )
            model.fit(matrix, labels)
            self._model = model
        except Exception:  # pragma: no cover - sklearn fallback
            self._model = _NearestCentroidProbabilityModel().fit(matrix, labels)
        return self

    def rank(
        self,
        *,
        query_session_id: str,
        candidate_session_ids: Iterable[str],
    ) -> SessionLinkReport:
        if self._model is None:
            self.fit()
        candidates: list[SessionLinkCandidate] = []
        for session_id in candidate_session_ids:
            if session_id == query_session_id:
                continue
            pair = self._pair_features(query_session_id, session_id)
            vector = [[pair.get(name, 0.0) for name in self._feature_names]]
            score = float(self._model.predict_proba(vector)[0][1])
            shared = tuple(
                sorted(
                    set(
                        session_feature_vector(
                            self.graph.edges_by_session(query_session_id),
                            include_semantic_labels=self.include_semantic_labels,
                        )
                    ).intersection(
                        session_feature_vector(
                            self.graph.edges_by_session(session_id),
                            include_semantic_labels=self.include_semantic_labels,
                        )
                    )
                )[:10]
            )
            candidates.append(SessionLinkCandidate(session_id, score, shared))
        ranked = tuple(sorted(candidates, key=lambda item: (-item.score, item.session_id)))
        return SessionLinkReport(query_session_id=query_session_id, candidates=ranked)

    def _pair_features(self, left: str, right: str) -> dict[str, float]:
        left_edges = self.graph.edges_by_session(left)
        right_edges = self.graph.edges_by_session(right)
        left_features = session_feature_vector(
            left_edges,
            include_semantic_labels=self.include_semantic_labels,
        )
        right_features = session_feature_vector(
            right_edges,
            include_semantic_labels=self.include_semantic_labels,
        )
        left_rel = _prefix_features(left_features, "relation:")
        right_rel = _prefix_features(right_features, "relation:")
        left_sens = _prefix_features(left_features, "sensitivity:")
        right_sens = _prefix_features(right_features, "sensitivity:")
        return {
            "cosine": cosine_similarity(left_features, right_features),
            "wl_kernel": cosine_similarity(
                _prefix_features(left_features, "wl1:"),
                _prefix_features(right_features, "wl1:"),
            ),
            "graph_edit": graph_edit_similarity(left_edges, right_edges),
            "relation_cosine": cosine_similarity(left_rel, right_rel),
            "sensitivity_cosine": cosine_similarity(left_sens, right_sens),
            "edge_count_ratio": _ratio(len(left_edges), len(right_edges)),
            "shared_relation_jaccard": _jaccard(set(left_rel), set(right_rel)),
            "shared_sensitive_jaccard": _jaccard(set(left_sens), set(right_sens)),
        }


def _prefix_features(features: Counter[str], prefix: str) -> Counter[str]:
    return Counter({key: value for key, value in features.items() if key.startswith(prefix)})


def _session_user(edges: tuple[MemoryEdge, ...]) -> str | None:
    users = [edge.source_user_id for edge in edges if edge.source_user_id]
    if not users:
        return None
    return Counter(users).most_common(1)[0][0]


def _ratio(left: int, right: int) -> float:
    larger = max(left, right, 1)
    return min(left, right) / larger


def _jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


class _ConstantProbabilityModel:
    def __init__(self, probability: float) -> None:
        self.probability = probability

    def predict_proba(self, matrix):
        return [[1.0 - self.probability, self.probability] for _ in matrix]


class _NearestCentroidProbabilityModel:
    def fit(self, matrix, labels):
        positives = [row for row, label in zip(matrix, labels) if label == 1]
        negatives = [row for row, label in zip(matrix, labels) if label == 0]
        self.positive = _centroid(positives)
        self.negative = _centroid(negatives)
        return self

    def predict_proba(self, matrix):
        probabilities = []
        for row in matrix:
            positive_distance = _euclidean(row, self.positive)
            negative_distance = _euclidean(row, self.negative)
            total = positive_distance + negative_distance
            probability = 0.5 if total == 0 else negative_distance / total
            probabilities.append([1.0 - probability, probability])
        return probabilities


def _centroid(rows):
    if not rows:
        return []
    return [sum(row[index] for row in rows) / len(rows) for index in range(len(rows[0]))]


def _euclidean(left, right) -> float:
    if not left or not right:
        return 0.0
    return sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def graph_edit_similarity(left: tuple[MemoryEdge, ...], right: tuple[MemoryEdge, ...]) -> float:
    """Fast graph-edit proxy based on relation, degree, and sensitivity deltas."""

    left_features = _edit_signature(left)
    right_features = _edit_signature(right)
    keys = set(left_features).union(right_features)
    distance = sum(abs(left_features.get(key, 0) - right_features.get(key, 0)) for key in keys)
    normalizer = sum(left_features.values()) + sum(right_features.values()) or 1
    return 1.0 - min(1.0, distance / normalizer)


def hashed_embedding(features: Counter[str], *, dimensions: int = 32) -> Counter[str]:
    """Deterministic signed feature hashing for a lightweight embedding baseline."""

    import hashlib

    vector: Counter[str] = Counter()
    for feature, value in features.items():
        digest = hashlib.sha256(feature.encode()).digest()
        bucket = digest[0] % dimensions
        sign = 1 if digest[1] % 2 == 0 else -1
        vector[f"dim:{bucket}"] += sign * value
    return vector


def _edit_signature(edges: tuple[MemoryEdge, ...]) -> Counter[str]:
    degree: Counter[str] = Counter()
    signature: Counter[str] = Counter()
    for edge in edges:
        degree[edge.source_id] += 1
        degree[edge.target_id] += 1
        signature[f"relation:{edge.relation}"] += 1
        signature[f"sensitivity:{edge.sensitivity}"] += 1
    for value in degree.values():
        signature[f"degree:{value}"] += 1
    signature[f"edges:{len(edges)}"] += 1
    return signature


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    shared = set(left).intersection(right)
    numerator = sum(left[key] * right[key] for key in shared)
    left_norm = sqrt(sum(value * value for value in left.values()))
    right_norm = sqrt(sum(value * value for value in right.values()))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return max(0.0, min(1.0, numerator / (left_norm * right_norm)))
