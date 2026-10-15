# Northwestern Parks Capstone

Workspace and automation for a Northwestern University data engineering capstone focused on hiking, camping, and national parks.

The repository provides:

- A ready-to-use Python, R, Jupyter, and DuckDB environment
- A standard structure for raw and processed data
- Automated testing and linting
- A small synthetic dataset for testing the infrastructure
- GitHub Actions that test the repository after every push and once daily

The student provides the real data, modeling, analysis, and business presentation.

## Start in GitHub Codespaces

1. Open this repository on GitHub.
2. Select **Code → Codespaces**.
3. Create a codespace on `master`.
4. Wait for setup to finish.
5. Open a notebook under `notebooks/`.
6. Select the Python interpreter containing `.venv`.

Nothing needs to be installed on the laptop.

## Project structure

| Location | Purpose |
|---|---|
| `notebooks/` | Exploration, modeling, analysis, and presentation |
| `src/capstone/` | Reusable Python code |
| `tests/` | Automated tests and data-quality checks |
| `data/raw/` | Original source data |
| `data/processed/` | Cleaned and model-ready data |
| `data/warehouse.duckdb` | Local DuckDB warehouse |
| `scripts/` | Setup and infrastructure utilities |
| `.github/workflows/` | GitHub Actions automation |

Generated data and credentials are excluded from Git.

## Check the environment

From the repository root:

```bash
source .venv/bin/activate

python scripts/check_setup.py
ruff check src scripts tests
pytest -q
```

A healthy environment should report:

```text
All checks passed!
6 passed
Everything required is working.
```

Warnings about optional API keys, R on a local host, or restricted network access do not necessarily indicate a failure.

## Test the data infrastructure

The repository includes deterministic synthetic data for fictional parks, campgrounds, alerts, and weather.

Run the test pipeline with:

```bash
python scripts/run_pipeline.py \
  --source mock \
  --as-of-date 2026-01-15 \
  --seed 42
```

Expected record counts:

```text
parks: 4
campgrounds: 3
alerts: 2
weather: 12
```

This verifies that the infrastructure can:

- Validate records and relationships
- Reject invalid records
- Write raw JSON
- Create Parquet datasets
- Build a DuckDB warehouse
- Produce repeatable results

The synthetic records are only test fixtures. They are not real park data and must not be used for capstone findings.

## Add capstone work

The normal workflow is:

1. Add Python dependencies to `requirements.txt`.
2. Put reusable Python code under `src/capstone/`.
3. Put notebooks under `notebooks/`.
4. Put automated tests under `tests/`.
5. Commit and push the changes.

Example:

```bash
git add .
git commit -m "Add campground analysis"
git push
```

GitHub automatically retrieves everything included in the commit.

Tests placed under `tests/` should use names such as:

```text
test_data_quality.py
test_model.py
test_analysis.py
```

Pytest discovers and runs files named `test_*.py`.

## GitHub automation

The workflow in `.github/workflows/ci.yml` runs:

- After every push
- For every pull request
- Daily at `00:00 UTC`
- Manually from the GitHub **Actions** page

Each run:

1. Checks out the latest committed code.
2. Creates a clean Python 3.12 environment.
3. Installs `requirements.txt`.
4. Installs the local `capstone` package.
5. Runs Ruff.
6. Runs all Pytest tests.
7. Exercises the storage pipeline with deterministic synthetic data.

GitHub performs this work on a hosted runner. The laptop does not need to remain on.

The workflow tests committed code and data rules. It does not determine whether a model, analysis, or business conclusion is academically correct.

## API keys

Never commit API keys or place them directly in notebooks.

For local use:

```bash
cp .env.example .env
```

Add keys to `.env`. That file is excluded from Git.

For GitHub Actions, add keys under:

**Repository Settings → Secrets and variables → Actions**

Optional supported names include:

```text
NPS_API_KEY
RIDB_API_KEY
```

## Before pushing

Run:

```bash
ruff check src scripts tests
pytest -q
git diff --check
```

After pushing, confirm the run is green under **GitHub → Actions → CI**.
