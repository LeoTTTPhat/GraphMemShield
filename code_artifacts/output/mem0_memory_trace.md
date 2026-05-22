# Mem0 Agent-Memory Integration

This run uses the real `mem0ai` package with local Qdrant storage and OpenAI embeddings.
It indexes a bounded enterprise edge sample to keep the reproducible run small.

| System | Dataset | Experiment | Condition | Metric | Value |
|---|---|---|---|---:|---:|
| mem0_agent_memory | enterprise_health_finance | dataset | mem0 | framework | Mem0 |
| mem0_agent_memory | enterprise_health_finance | dataset | mem0 | framework_available | True |
| mem0_agent_memory | enterprise_health_finance | dataset | mem0 | indexed_edges | 40 |
| mem0_agent_memory | enterprise_health_finance | dataset | mem0 | victim_indexed_edges | 12 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | retrieved_edges | 24 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | leaked_edges | 10 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | response_leaked_edges | 6 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | response_leaked_terms | 8 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | qa_accuracy | 1.0 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | retrieved_edges | 7 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | leaked_edges | 0 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | response_leaked_edges | 0 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | response_leaked_terms | 0 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | qa_accuracy | 1.0 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | retrieved_edges | 10 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | leaked_edges | 3 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | response_leaked_edges | 3 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | response_leaked_terms | 2 |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | qa_accuracy | 1.0 |
