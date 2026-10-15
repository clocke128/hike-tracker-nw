from datetime import date

import duckdb
import pytest

from capstone.pipeline import DataValidationError, run_pipeline, validate
from capstone.sources import build_mock_data


def test_mock_data_is_deterministic():
    first = build_mock_data(date(2026, 1, 15), seed=42)
    second = build_mock_data(date(2026, 1, 15), seed=42)
    assert first == second
    assert {row["park_code"] for row in first["parks"]} == {"pine", "mesa", "lake", "cave"}


def test_pipeline_builds_outputs_and_warehouse(tmp_path):
    manifest = run_pipeline(as_of_date=date(2026, 1, 15), seed=42, output_root=tmp_path)
    assert manifest["record_counts"] == {
        "parks": 4,
        "campgrounds": 3,
        "alerts": 2,
        "weather": 12,
    }
    assert (tmp_path / "manifests" / "latest.json").is_file()
    assert (tmp_path / "raw" / "mock" / "2026-01-15" / "parks.json").is_file()
    with duckdb.connect(str(tmp_path / "warehouse.duckdb"), read_only=True) as connection:
        assert connection.execute("SELECT count(*) FROM parks").fetchone()[0] == 4
        assert connection.execute("SELECT count(*) FROM weather").fetchone()[0] == 12


def test_validation_rejects_unknown_park():
    import pandas as pd

    records = build_mock_data(date(2026, 1, 15))
    records["campgrounds"][0]["park_code"] = "missing"
    frames = {name: pd.DataFrame(rows) for name, rows in records.items()}
    with pytest.raises(DataValidationError, match="unknown parks"):
        validate(frames)
