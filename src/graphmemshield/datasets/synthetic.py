from __future__ import annotations

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge, MemoryNode


def build_synthetic_multisession_graph() -> DynamicMemoryGraph:
    """Build a tiny graph with repeated user motifs for deterministic tests."""

    graph = DynamicMemoryGraph()
    for node_id, label in [
        ("alice", "Alice"),
        ("alice-alt", "A. Nguyen"),
        ("bob", "Bob"),
        ("clinic", "Heart Clinic"),
        ("condition", "arrhythmia"),
        ("gym", "Gym"),
        ("laptop", "Laptop"),
        ("invoice", "Invoice"),
    ]:
        graph.add_node(MemoryNode(node_id=node_id, label=label))

    edges = [
        MemoryEdge(
            edge_id="alice-s1-e1",
            source_id="alice",
            relation="visited",
            target_id="clinic",
            owner_session_id="alice-session-1",
            source_user_id="alice-user",
            turn_id="t1",
            sensitivity="medical",
            created_at=1.0,
        ),
        MemoryEdge(
            edge_id="alice-s1-e2",
            source_id="clinic",
            relation="diagnosed",
            target_id="condition",
            owner_session_id="alice-session-1",
            source_user_id="alice-user",
            turn_id="t2",
            sensitivity="medical",
            created_at=2.0,
        ),
        MemoryEdge(
            edge_id="alice-s2-e1",
            source_id="alice-alt",
            relation="visited",
            target_id="clinic",
            owner_session_id="alice-session-2",
            source_user_id="alice-user",
            turn_id="t1",
            sensitivity="medical",
            created_at=3.0,
        ),
        MemoryEdge(
            edge_id="alice-s2-e2",
            source_id="clinic",
            relation="diagnosed",
            target_id="condition",
            owner_session_id="alice-session-2",
            source_user_id="alice-user",
            turn_id="t2",
            sensitivity="medical",
            created_at=4.0,
        ),
        MemoryEdge(
            edge_id="bob-s1-e1",
            source_id="bob",
            relation="visited",
            target_id="gym",
            owner_session_id="bob-session-1",
            source_user_id="bob-user",
            turn_id="t1",
            sensitivity="normal",
            created_at=5.0,
        ),
        MemoryEdge(
            edge_id="bob-s1-e2",
            source_id="bob",
            relation="purchased",
            target_id="laptop",
            owner_session_id="bob-session-1",
            source_user_id="bob-user",
            turn_id="t2",
            sensitivity="financial",
            created_at=6.0,
        ),
        MemoryEdge(
            edge_id="bob-s1-e3",
            source_id="laptop",
            relation="has_record",
            target_id="invoice",
            owner_session_id="bob-session-1",
            source_user_id="bob-user",
            turn_id="t3",
            sensitivity="financial",
            created_at=7.0,
        ),
    ]
    for edge in edges:
        graph.add_edge(edge)
    return graph


import random

def build_large_synthetic_graph(num_users: int = 100, sessions_per_user: int = 5, seed: int = 42) -> DynamicMemoryGraph:
    """Build a large-scale synthetic graph with multiple users and domains."""
    random.seed(seed)
    graph = DynamicMemoryGraph()
    
    domains = ["health", "finance", "work", "location"]
    
    clinics = [f"Clinic_{i}" for i in range(10)]
    conditions = ["arrhythmia", "diabetes", "hypertension", "asthma"]
    pharmacies = [f"Pharmacy_{i}" for i in range(10)]
    medications = ["beta blocker", "insulin", "lisinopril", "albuterol"]
    
    merchants = [f"Merchant_{i}" for i in range(20)]
    items = ["laptop", "monitor", "software license", "server", "insurance"]
    
    projects = [f"Project_{x}" for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    clients = [f"Client_{i}" for i in range(15)]
    
    hotels = [f"Hotel_{i}" for i in range(15)]
    cities = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
    
    for e in clinics + conditions + pharmacies + medications + merchants + items + projects + clients + hotels + cities:
        graph.add_node(MemoryNode(node_id=e, label=e.replace("_", " ")))
        
    global_time = 1.0
    
    for u in range(num_users):
        user_id = f"user_{u}"
        graph.add_node(MemoryNode(node_id=user_id, label=f"User {u}"))
        
        for s in range(sessions_per_user):
            session_id = f"session_{u}_{s}"
            domain = random.choice(domains)
            
            if domain == "health":
                clinic = random.choice(clinics)
                condition = random.choice(conditions)
                medication = random.choice(medications)
                
                edges = [
                    (user_id, "visited", clinic, "medical"),
                    (user_id, "has_condition", condition, "medical"),
                    (user_id, "takes_medication", medication, "medical"),
                ]
            elif domain == "finance":
                merchant = random.choice(merchants)
                item = random.choice(items)
                
                edges = [
                    (user_id, "purchased_from", merchant, "financial"),
                    (user_id, "purchased_item", item, "financial"),
                    (item, "from_merchant", merchant, "financial"),
                ]
            elif domain == "work":
                project = random.choice(projects)
                client = random.choice(clients)
                
                edges = [
                    (user_id, "works_on", project, "secret"),
                    (project, "for_client", client, "secret"),
                ]
            else:
                hotel = random.choice(hotels)
                city = random.choice(cities)
                
                edges = [
                    (user_id, "booked_hotel", hotel, "normal"),
                    (hotel, "located_in", city, "normal"),
                ]
                
            for i, (src, rel, tgt, sens) in enumerate(edges):
                graph.add_edge(MemoryEdge(
                    edge_id=f"edge_{u}_{s}_{i}",
                    source_id=src,
                    relation=rel,
                    target_id=tgt,
                    owner_session_id=session_id,
                    source_user_id=user_id,
                    turn_id=f"t{i+1}",
                    sensitivity=sens,
                    created_at=global_time
                ))
                global_time += 1.0
                
    return graph
