import json
import os
import sys
from dataclasses import asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.datasets.enterprise import (  # noqa: E402
    build_enterprise_health_finance_records,
)


def main() -> None:
    records = build_enterprise_health_finance_records()
    output_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "enterprise_health_finance.jsonl"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        for record in records:
            payload = asdict(record)
            payload["relations"] = [asdict(relation) for relation in record.relations]
            handle.write(json.dumps(payload, sort_keys=True) + "\n")
    print(f"records: {len(records)}")
    print(f"jsonl: {output_path}")


if __name__ == "__main__":
    main()
