import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.evaluation import (  # noqa: E402
    run_synthetic_experiments,
    write_experiment_outputs,
)


def main() -> None:
    records = run_synthetic_experiments()
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    paths = write_experiment_outputs(records, output_dir)

    print("GraphMemShield synthetic experiments")
    for record in records:
        print(
            f"{record.experiment} | {record.condition} | "
            f"{record.metric} = {record.value}"
        )
    print(f"json: {paths['json']}")
    print(f"csv: {paths['csv']}")
    print(f"markdown: {paths['markdown']}")


if __name__ == "__main__":
    main()
