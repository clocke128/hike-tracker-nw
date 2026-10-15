# Mock pipeline handoff

This infrastructure uses deterministic fictional records and makes no network calls.

## Local run

```bash
python scripts/run_pipeline.py --source mock --as-of-date 2026-01-15 --seed 42
```

Outputs are raw JSON, processed Parquet, a DuckDB warehouse, and a run manifest under `data/`.

## Remote run

Open **GitHub → Actions → Scheduled mock pipeline → Run workflow**. GitHub runs it remotely and publishes the outputs as a downloadable artifact. It also runs each Monday at 11:17 UTC.

## Student handoff

The production data-source adapter is intentionally not implemented. Replace or complement `src/capstone/sources/mock.py` while preserving the datasets expected by `src/capstone/pipeline.py`. Add source-specific tests before changing the scheduled workflow from `--source mock`.
