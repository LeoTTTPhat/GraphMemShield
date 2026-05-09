# GraphMemShield Release Checklist

Use this checklist before handing the artifact to reviewers or publishing a research artifact snapshot.

- [x] License file present: `LICENSE`.
- [x] Citation metadata present: `CITATION.cff`.
- [x] Python packaging metadata present: `pyproject.toml`.
- [x] Ignore rules present: `.gitignore`.
- [x] CI workflow template present: `.github/workflows/graphmemshield-tests.yml`.
- [x] Reproducibility guide present: `REPRODUCIBILITY.md`.
- [x] Experiment manifest present: `EXPERIMENT_MANIFEST.md`.
- [x] Limitations documented: `LIMITATIONS_AND_NEXT_STEPS.md`.
- [x] Paper-ready tables present: `PAPER_READY_TABLES.md`.
- [x] Current test suite passes with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest Ideas/GraphMemShield/tests -q`.

Known pre-release caveats:

- Docker experiments seed de-identified records directly into MongoDB for controlled read-path evaluation.
- `RandomizedEdgeAdmission` is a seeded proxy, not a formal DP mechanism.
- `TemporalPathInfer` is a timestamp/provenance exposure baseline.
- Public large-dataset ingestion and real response scoring are not included in this snapshot.
