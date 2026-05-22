import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "internal_tracekg_rag_tasks_60.json"


DOMAINS = [
    (
        "reliability",
        "absorbing Markov chain",
        "TraceKG models reliability with an absorbing Markov chain over success, failure, and repair states.",
    ),
    (
        "retrieval",
        "retrieval-before-answer gating",
        "TraceKG recommends retrieval-before-answer gating when an agent answers without sufficient evidence.",
    ),
    (
        "navigation",
        "navigation rollback",
        "Repeated failed navigation is handled by page-state memory and navigation rollback.",
    ),
    (
        "verification",
        "mandatory verification",
        "Terminal success without tests triggers a mandatory verification repair.",
    ),
    (
        "schema",
        "schema validation",
        "Tool precondition failures are mitigated with schema validation before tool execution.",
    ),
    (
        "budget",
        "step budget guard",
        "BudgetExceeded failures are handled by a step budget guard followed by replanning.",
    ),
    (
        "web",
        "WebArena",
        "WebArena evaluates realistic web navigation agents in browser-like environments.",
    ),
    (
        "coding",
        "SWE-bench",
        "SWE-bench evaluates agents on real-world GitHub issue resolution tasks.",
    ),
    (
        "agent",
        "AgentBench",
        "AgentBench evaluates language-model agents across multiple interactive environments.",
    ),
    (
        "privacy",
        "provenance minimization",
        "Privacy-sensitive trace sharing uses provenance minimization and de-identified benchmark observations.",
    ),
]


def main() -> None:
    OUTPUT.parent.mkdir(exist_ok=True)
    tasks = []
    for index in range(60):
        domain, answer, fact = DOMAINS[index % len(DOMAINS)]
        task_id = f"rag-internal-{index + 1:03d}"
        distractor_a = DOMAINS[(index + 3) % len(DOMAINS)]
        distractor_b = DOMAINS[(index + 7) % len(DOMAINS)]
        tasks.append(
            {
                "task_id": task_id,
                "question": f"For approved internal TraceKG case {index + 1}, what is the controlled answer named in the primary {domain} document?",
                "answer": answer,
                "documents": [
                    {
                        "id": f"{task_id}-d1",
                        "text": f"Primary {domain} document for approved internal TraceKG case {index + 1}. Controlled answer: {answer}. {fact}",
                    },
                    {
                        "id": f"{task_id}-d2",
                        "text": f"Secondary distractor for unrelated case {index + 101}. Controlled answer: {distractor_a[1]}. {distractor_a[2]}",
                    },
                    {
                        "id": f"{task_id}-d3",
                        "text": f"Secondary distractor for unrelated case {index + 201}. Controlled answer: {distractor_b[1]}. {distractor_b[2]}",
                    },
                ],
            }
        )
    OUTPUT.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
    print(f"wrote {len(tasks)} tasks to {OUTPUT}")


if __name__ == "__main__":
    main()
