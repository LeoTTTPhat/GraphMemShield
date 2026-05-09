# GraphMemShield PrivacyGuard Docker Experiment

This experiment seeds de-identified records into the running PrivacyGuard MongoDB
mock, fetches them through the Cloud API, maps them into a GraphMemShield
memory graph, and evaluates cross-session leakage.

## System Health

- Edge: `ok`
- Fog: `ok`
- Cloud: `ok`
- Mongo state: `1`

## Data and Graph

- Records: `{'graphmem-alice': 2, 'graphmem-bob': 1}`
- Nodes: `15`
- Edges: `15`

## Leakage Results

- Baseline leaked edges: `5`
- Baseline leakage events: `15`
- Baseline leakage rate: `0.5`
- Baseline event leakage rate: `0.5`
- Defended leaked edges: `0`
- Leakage reduction: `1.0`
- Defense framing: `strict provenance/session isolation`

## Manual Follow-up

- Replace seed records with public datasets or approved real records.
- Avoid storing raw personal identifiers in seed data; use de-identified IDs.
- Add API-level write flow through `/api/validate-and-prove` and `/api/store` when proof material is available.
- Add repeated query budgets and multiple attacker sessions.
