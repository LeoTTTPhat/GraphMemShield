import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.datasets import (
    dialogue_records_to_graph,
    dialogue_records_to_privacyguard_docs,
    load_dialogue_jsonl,
    session_ids,
    user_ids,
)


DATASET_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "sample_dialogues.jsonl"
)


def test_sample_dialogue_jsonl_loads_with_ground_truth():
    records = load_dialogue_jsonl(DATASET_PATH)

    assert len(records) == 12
    assert len(user_ids(records)) == 6
    assert len(session_ids(records)) == 12
    assert all(record.relations for record in records)


def test_dialogue_records_convert_to_graph_and_privacyguard_docs():
    records = load_dialogue_jsonl(DATASET_PATH)
    graph = dialogue_records_to_graph(records)
    docs = dialogue_records_to_privacyguard_docs(records)

    assert len(graph.edges) == 36
    assert len(docs) == len(records)
    assert docs[0]["metadata"]["relations"]
