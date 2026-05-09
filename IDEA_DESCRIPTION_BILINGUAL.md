# GraphMemShield

## 1. Revised Paper-Style Title

**English title:**
GraphMemShield: Auditing and Mitigating Cross-Session Privacy Leakage in Dynamic Knowledge-Graph Memories for Graph-Backed Applications

**Vietnamese title:**
GraphMemShield: Kiểm Định và Giảm Thiểu Rò Rỉ Riêng Tư Liên Phiên Trong Bộ Nhớ Đồ Thị Tri Thức Động của Graph-Backed Application

---

## 2. Executive Research Claim

graph-backed applications are increasingly equipped with persistent memory that stores user interactions as entities, relations, summaries, timestamps, and provenance metadata. When this memory is implemented as a knowledge graph (KG) or graph-augmented retrieval store, the system no longer behaves like a passive retrieval index. It becomes a continuously updated, multi-user graph whose retrieval behavior depends on historical writes from previous sessions.

Recent work has already shown that graph-backed application memory can leak private facts, and that graph-augmented retrieval systems can expose entities, relationships, and subgraphs. GraphMemShield therefore does **not** claim novelty over all memory leakage or all graph-augmented retrieval reconstruction attacks. Its sharper contribution is the first focused study of **cross-session privacy leakage in dynamic KG-backed application memory**, where the sensitive object is not only a stored fact or static subgraph, but the link between users, sessions, provenance, update order, and graph retrieval behavior.

GraphMemShield contributes:

1. A formal privacy model for dynamic, multi-user application memory graphs.
2. A benchmark methodology for measuring cross-session leakage caused by shared graph memory.
3. Three attacks that exploit update dynamics, session provenance, and graph retrieval traces.
4. GraphMemGuard, a practical defense combining session-aware graph partitioning, provenance filtering, privacy-budgeted retrieval, and differentially private edge admission.

---

## 3. Vietnamese Research Summary

Các nghiên cứu gần đây đã chỉ ra rằng bộ nhớ của graph-backed application có thể bị khai thác để trích xuất thông tin riêng tư, và graph-augmented retrieval có thể làm lộ thực thể, quan hệ hoặc đồ thị con. Vì vậy, GraphMemShield không nên claim quá rộng rằng đây là nghiên cứu đầu tiên về privacy trong application memory hoặc graph-augmented retrieval.

Điểm mới cần nhấn mạnh là: **bộ nhớ system dạng đồ thị tri thức là một hệ thống động, đa người dùng, có provenance và session boundary**. Dữ liệu của một người dùng có thể được ghi vào graph, sau đó ảnh hưởng đến truy xuất hoặc câu trả lời cho người dùng khác. Rủi ro chính không chỉ là lộ một fact riêng lẻ, mà là lộ liên kết giữa session, người dùng, thời điểm ghi nhớ, chuỗi hội thoại và các cạnh trong graph.

GraphMemShield vì vậy được định vị như một nghiên cứu về **rò rỉ riêng tư liên phiên trong dynamic KG-backed application memory**, với cả attack, benchmark và defense có thể triển khai trên framework thật.

---

## 4. Core Problem

### 4.1 Problem Statement

Existing privacy work usually studies leakage from model parameters, prompts, retrieved text chunks, or generic persistent memory. Existing graph privacy work usually studies static graphs, GNN embeddings, or graph-augmented retrieval knowledge bases. These settings miss a distinct failure mode in deployed graph-memory systems:

> A multi-user graph-backed application may write each user's interaction into a shared or partially shared KG memory, then later retrieve across that graph for another user. Even when direct text snippets are hidden, the graph structure, retrieval paths, session provenance, and update order can reveal sensitive cross-user information.

### 4.2 Privacy Failure Modes

1. **Cross-session retrieval contamination**
   - A query from user B retrieves edges, summaries, or paths created from user A's prior session.
   - The response may reveal sensitive attributes even without exposing the raw memory record.

2. **Session-linkage leakage**
   - An attacker links two anonymized sessions to the same user by comparing local graph structures, repeated entities, relation motifs, or provenance traces.
   - This remains possible even when entity names are pseudonymized.

3. **Temporal path inference**
   - Dynamic memory writes preserve insertion order, timestamps, edge provenance, or local topology changes.
   - An attacker can infer the sequence of interactions that caused a sensitive subgraph to appear.

4. **Edge-admission leakage**
   - The presence or absence of an edge after a user interaction reveals whether a sensitive relation was extracted, accepted, and stored by the memory system.

---

## 5. Novelty Positioning for a Q1 Journal

### 5.1 What This Paper Should Not Claim

The paper should avoid these overclaims:

- "First study of privacy risks in graph-backed application memory."
- "First study of privacy leakage in graph-augmented retrieval."
- "First graph reconstruction attack against graph-augmented retrieval."
- "First edge privacy defense for graph data."

These claims are too broad and overlap with recent work on application memory extraction, graph-augmented retrieval leakage, graph privacy, and subgraph reconstruction.

### 5.2 Defensible Novelty Claim

The stronger and more defensible claim is:

> GraphMemShield is a focused framework for auditing and mitigating cross-session privacy leakage in **dynamic, multi-user KG-backed graph-backed application memory**, where leakage arises from the interaction between memory writes, graph retrieval, provenance metadata, and session boundary failures.

### 5.3 Relation to Prior Work

| Research Line | Representative Work | What It Covers | Remaining Gap Addressed by GraphMemShield |
|---|---|---|---|
| graph-backed application memory extraction | MEXTRA / Unveiling Privacy Risks in Graph-Backed Application Memory (ACL 2025) | Extracting private content from application memory via black-box interaction | Does not focus on KG topology, graph retrieval paths, provenance-aware session linkage, or cross-user graph contamination |
| graph-augmented retrieval privacy leakage | Exposing Privacy Risks in Graph Retrieval-Augmented Generation (2025) | Leakage of entities and relationships in graph-augmented retrieval | Mostly treats the graph as a retrieval resource, not as a continuously updated multi-user application memory |
| graph-augmented retrieval subgraph reconstruction | Subgraph Reconstruction Attacks on Graph retrieval Deployments (2026) | Reconstructing static or deployed graph-augmented retrieval subgraphs through queries | Does not model user-session writes, temporal memory evolution, or cross-session privacy boundaries |
| GNN graph privacy | GraphMI, GAP, GRID, graph representation privacy | Model inversion, link stealing, embedding leakage, DP for graph learning | Focuses on trained graph models or static graph representations, not retrieval-driven graph-backed application memory |
| Memory isolation and access control | Practical retrieval isolation patterns | Tenant filtering, ACLs, namespace separation | Usually lacks formal leakage metrics and attack evaluation for graph-memory sessions |

---

## 6. Research Questions

**RQ1: Cross-session leakage.**
How often do KG-backed application memory systems retrieve, summarize, or reason over graph elements written by another user's session under realistic multi-user workloads?

**RQ2: Attack feasibility.**
Can a black-box or gray-box adversary infer sensitive session membership, edge existence, or temporal interaction paths from responses and retrieved graph context?

**RQ3: Defense effectiveness.**
Can session-aware graph partitioning, provenance filtering, and privacy-budgeted retrieval reduce cross-session leakage while preserving useful long-term memory?

**RQ4: Privacy-utility tradeoff.**
What is the empirical and formal tradeoff between privacy protection and system utility across different graph sizes, memory update rates, and retrieval depths?

---

## 7. Threat Model

### 7.1 System Model

The target system is a multi-user graph-backed application with persistent memory implemented using one or more of:

- KG triples or property graphs, such as `(entity_a, relation, entity_b)`.
- Graph-augmented retrieval indexes with entity/relation extraction.
- Conversation summaries linked to entities, sessions, timestamps, and source messages.
- Graph traversal retrieval, such as k-hop expansion, Cypher queries, entity-neighborhood search, or hybrid vector-graph retrieval.

### 7.2 Attacker Capabilities

1. **Black-box user**
   - Sends queries to the graph-memory service.
   - Observes final responses only.
   - May adapt prompts over multiple turns.

2. **Gray-box user**
   - Observes retrieved context, citations, memory snippets, or debug traces exposed by the system.
   - This models developer tools, transparency modes, or enterprise audit views.

3. **Semi-honest operator**
   - Can inspect graph records and metadata but does not modify the system.
   - Used to evaluate insider leakage and validate ground truth.

### 7.3 Victim and Sensitive Objects

Victims are users whose sessions have been stored in the shared or partially shared memory graph. Sensitive objects include:

- Edge existence: whether a relation was stored.
- Edge provenance: which session or user caused the edge.
- Local ego-graph structure: a user's session-level memory subgraph.
- Temporal path: the sequence of writes that produced a sensitive graph neighborhood.
- Cross-session influence: whether one user's memory affected another user's response.

### 7.4 Adjacency Definition

For formal privacy analysis, two memory histories are adjacent if they differ in one protected session event:

- one extracted edge,
- one memory write batch from a single user turn, or
- one session-local ego graph, depending on the privacy granularity.

This should be stated explicitly because relation-level randomized response alone does not protect edge existence if the endpoints or edge count remain visible.

---

## 8. Proposed Attacks

### Attack 1: CrossSessionProbe

**Goal:** Determine whether memory written by victim session `s_v` influences responses to attacker session `s_a`.

**Method:**

- Construct probe queries around target entities, attributes, and relation motifs.
- Measure response changes when victim memory is present versus removed in controlled experiments.
- In black-box settings, score leakage using calibrated response classifiers and semantic similarity.
- In gray-box settings, measure direct retrieval of victim-owned graph elements.

**Output:** Cross-session leakage score, victim-edge exposure rate, and response-level attribution confidence.

**Novelty:** Focuses on cross-session influence in dynamic memory, not merely extraction of stored facts.

### Attack 2: SessionGraphLink

**Goal:** Link anonymized memory subgraphs to the same underlying user or session family.

**Method:**

- Represent each session as an ego graph containing entities, relation types, timestamps, and provenance features.
- Compare anonymized graphs using Weisfeiler-Lehman kernels, graph edit distance approximations, motif histograms, and temporal signatures.
- Evaluate both structure-only and structure-plus-semantics settings.

**Output:** Top-k session linkage accuracy, false match rate, and robustness under entity pseudonymization.

**Novelty:** Treats graph memory itself as a behavioral fingerprint, which is different from direct memory extraction.

### Attack 3: TemporalPathInfer

**Goal:** Infer the sequence of user interactions or memory writes that produced a sensitive graph neighborhood.

**Method:**

- Issue multi-turn prompts that trigger k-hop graph retrieval around target entities.
- Use observed response order, retrieved context order, timestamps when available, and relation co-occurrence to infer likely insertion paths.
- Apply beam search over candidate write sequences and rank paths by response likelihood.

**Output:** Path precision/recall, graph edit distance to ground-truth write path, and temporal ordering accuracy.

**Novelty:** Extends static subgraph reconstruction by targeting the temporal write process of application memory.

---

## 9. Defense: GraphMemGuard

The defense should be renamed from GraphMemDP to **GraphMemGuard** because a purely DP-based defense is unlikely to be sufficient by itself. The practical system should combine isolation, filtering, and formal privacy mechanisms.

### 9.1 Defense Components

1. **Session-aware graph partitioning**
   - Store user/session provenance on every node, edge, summary, and extracted relation.
   - Enforce retrieval constraints so cross-session traversal requires explicit policy permission.

2. **Provenance-filtered retrieval**
   - Apply policy checks before graph expansion, not after response generation.
   - Prevent sensitive paths from entering the context window.

3. **Privacy-budgeted graph traversal**
   - Limit the number of protected edges, hops, and victim-owned records exposed across repeated queries.
   - Track exposure budget per attacker session and per protected victim session.

4. **DP edge admission**
   - For sensitive relation classes, use randomized edge admission rather than relation swapping alone.
   - Candidate mechanisms include edge subsampling, decoy edge insertion, relation generalization, and bounded-degree clipping.
   - The privacy guarantee should be stated over the defined adjacency unit: edge-level, turn-level, or session-level.

5. **Semantic utility preservation**
   - Decoy or generalized relations should be sampled from ontology-compatible clusters.
   - Retrieval quality should be measured after filtering, not assumed.

### 9.2 Why Relation Swapping Alone Is Insufficient

The original GraphMemDP design swapped relation labels while keeping endpoints visible. This can still reveal that a relationship exists between two sensitive entities. For Q1-level rigor, the defense must protect at least one of:

- whether an edge exists,
- whether a user/session caused that edge,
- whether a graph path crosses a protected session boundary,
- whether repeated queries consume protected retrieval budget.

---

## 10. Evaluation Plan

### 10.1 Systems Under Study

Primary systems:

- Neo4j-style persistent graph memory prototype.
- Property graph index or equivalent KG-backed memory layer.
- graph-augmented entity/relation extraction pipeline.

Optional systems:

- Neo4j-backed graph memory prototype.
- Zep or similar production-oriented memory store, if API access and reproducibility are sufficient.

### 10.2 Datasets

Use datasets that support session/user separation and sensitive-attribute annotation:

- PersonaChat: synthetic persona attributes and repeated personal facts.
- MultiWOZ 2.4: task-oriented private entities such as names, addresses, bookings, and preferences.
- Enron email subsets: real entity-relation structure, used with careful ethics filtering.
- Synthetic multi-user health or finance dialogues: controlled sensitive relations and ground-truth graph writes.

### 10.3 Experimental Protocol

1. Populate each memory system with multiple user sessions.
2. Extract or log ground-truth graph writes, provenance, timestamps, and retrieval traces.
3. Run attacker sessions with fixed query budgets.
4. Measure leakage under black-box and gray-box settings.
5. Apply defenses and repeat the same attacks.
6. Report privacy, utility, and overhead with confidence intervals.

### 10.4 Attack Metrics

- Cross-session retrieval rate: fraction of retrieved graph elements owned by other sessions.
- Victim-edge exposure AUC: ability to infer protected edge existence.
- Session linkage top-k accuracy: ability to match anonymized session graphs.
- Temporal path precision/recall: correctness of inferred write paths.
- Graph edit distance: distance between reconstructed and ground-truth memory subgraphs.
- Query efficiency: leakage per attacker query.

Avoid relying only on BLEU/ROUGE for PathReconstruct because reconstructed graph paths are more important than surface text similarity.

### 10.5 Defense Metrics

- Leakage reduction: relative decrease in cross-session retrieval and inferred protected edges.
- Utility retention: QA accuracy, memory recall accuracy, task success rate, and answer helpfulness.
- Latency overhead: write latency, retrieval latency, and policy-check overhead.
- Storage overhead: additional provenance labels, decoys, and budget accounting state.
- Privacy accounting: cumulative budget per protected session under repeated queries.

### 10.6 Baselines

- No defense: shared graph memory.
- Namespace isolation: per-user or per-session memory partition.
- ACL filtering: basic access-control list on graph records.
- Output filtering: post-hoc redaction after retrieval.
- Embedding perturbation: vector-space noise baseline.
- GraphMemGuard: proposed combined defense.

---

## 11. Expected Contributions

1. **Formal model:** A privacy model for dynamic multi-user KG-backed application memory, including provenance, temporal writes, and cross-session retrieval.
2. **Attack suite:** CrossSessionProbe, SessionGraphLink, and TemporalPathInfer, evaluated under black-box and gray-box access.
3. **Benchmark:** A reproducible benchmark for cross-session memory leakage in graph-based graph-backed applications.
4. **Defense system:** GraphMemGuard, combining session-aware partitioning, provenance-filtered retrieval, privacy-budgeted traversal, and DP edge admission.
5. **Empirical findings:** Quantitative evidence about when shared graph memory is unsafe, which metadata causes leakage, and which defenses preserve utility.

---

## 12. Feasibility and Risk Assessment

| Dimension | Assessment |
|---|---|
| Feasibility | High for attack evaluation and benchmark construction; medium for formal DP proof. |
| Implementation scope | Moderate. A reproducible prototype can be built with a Neo4j-backed memory layer before integrating with larger system frameworks. |
| Compute | Low to moderate. Most experiments require retrieval, graph construction, and inference, not model training. |
| Main novelty risk | Static graph-augmented retrieval reconstruction papers are close to TemporalPathInfer. The paper must emphasize dynamic writes, session provenance, and cross-session influence. |
| Main technical risk | DP edge admission may reduce memory utility. Include non-DP defenses and treat DP as one component of GraphMemGuard. |
| Main evaluation risk | Real systems may already isolate sessions by default. Include controlled misconfiguration and partially shared enterprise-memory scenarios. |

---

## 13. Target Publication Strategy

This work is better positioned as a **security/privacy systems paper** than as a pure graph-learning paper.

Potential Q1 journal targets:

- IEEE Transactions on Information Forensics and Security (TIFS)
- IEEE Transactions on Dependable and Secure Computing (TDSC)
- ACM Transactions on Privacy and Security (TOPS)
- Computers & Security
- IEEE Transactions on Services Computing, if framed around secure graph-memory services

Suggested submission strategy:

1. Build a strong experimental artifact first: benchmark, attacks, and defense prototype.
2. Submit an earlier conference/workshop version if needed to get feedback.
3. Extend to journal quality with broader systems, stronger formal model, ablations, and defense evaluation.

For Q1 journal quality, the paper should include:

- At least two real or realistic KG-backed application memory systems.
- At least three datasets with clear user/session boundaries.
- Controlled ground truth for graph writes and retrieval traces.
- Formal privacy definitions and threat model.
- Strong baselines including namespace isolation and ACL filtering.
- Reproducibility package with scripts, prompts, graph schemas, and evaluation metrics.

---

## 14. Revised Vietnamese Summary for Supervisor

**Tóm tắt đề tài sau khi chỉnh novelty:**

GraphMemShield nghiên cứu rò rỉ riêng tư trong bộ nhớ dài hạn của graph-backed application khi bộ nhớ được tổ chức dưới dạng đồ thị tri thức động. Điểm mới không nằm ở việc graph-augmented retrieval nói chung có thể bị rò rỉ, vì đã có các nghiên cứu gần đây về memory extraction và graph-augmented retrieval subgraph reconstruction. Điểm mới nằm ở bối cảnh **multi-user dynamic application memory**, nơi dữ liệu của nhiều người dùng được ghi liên tục vào cùng một graph hoặc graph dùng chung một phần.

Trong bối cảnh này, attacker có thể không cần đọc trực tiếp raw memory. Chỉ cần tương tác với dịch vụ graph-memory, attacker có thể suy luận rằng một cạnh nhạy cảm tồn tại, một session thuộc về cùng một người dùng, hoặc memory của người dùng khác đã ảnh hưởng đến kết quả truy xuất hiện tại. Đây là dạng rò rỉ liên phiên, gắn với provenance, temporal writes và graph traversal.

Đóng góp chính nên được viết lại thành:

1. Mô hình riêng tư cho dynamic multi-user KG-backed application memory.
2. Bộ attack đo cross-session leakage, session linkage và temporal path inference.
3. Benchmark tái lập để đánh giá memory leakage trong system dùng graph memory.
4. GraphMemGuard, một defense kết hợp session partitioning, provenance filtering, privacy-budgeted retrieval và DP edge admission.

Với cách định vị này, đề tài có tiềm năng đạt chất lượng journal Q1 nếu phần thực nghiệm đủ mạnh và không overclaim. Trọng tâm cần giữ là **cross-session privacy leakage in dynamic graph memory**, không phải graph-augmented retrieval privacy nói chung.
