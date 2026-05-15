# GraphMemShield Code Artifacts

This folder contains the runnable code and generated experiment artifacts for the
GraphMemShield submission. Manuscript files are intentionally excluded.

## Included

- `src/`: GraphMemShield package source.
- `examples/`: experiment and report-generation scripts.
- `tests/`: unit and integration-style tests.
- `data/`: synthetic, enterprise-style, MultiWOZ-derived, and Enron-style fixture data.
- `output/`: generated JSON/CSV/Markdown experiment outputs and backend artifacts.
- `.github/`: CI workflow metadata.
- Project metadata and docs: `pyproject.toml`, `setup.py`, `requirements.txt`,
  `README.md`, `REPRODUCIBILITY.md`, `EXPERIMENT_MANIFEST.md`,
  `PAPER_READY_TABLES.md`, `LIMITATIONS_AND_NEXT_STEPS.md`,
  `RELEASE_CHECKLIST.md`, `LICENSE`, and `CITATION.cff`.

## Excluded

- `paper/`
- `*.tex`
- PDF/manuscript build files
- `.git/`, `.venv/`, `.pytest_cache/`, `__pycache__/`, and bytecode caches

## Basic Verification

From this folder:

```bash
python -m pip install -e ".[dev]"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests -q
python examples/generate_aggregate_report.py
```

Expected current aggregate row count: `391`.
