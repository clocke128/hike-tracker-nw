"""Mock-first pipeline: validate, persist JSON/Parquet, and publish DuckDB."""

from __future__ import annotations

import json
import os
from datetime import UTC, date, datetime
from pathlib import Path
from uuid import uuid4

import duckdb
import pandas as pd

from capstone.sources import build_mock_data

TABLES = ("parks", "campgrounds", "alerts", "weather")


class DataValidationError(ValueError):
    """Raised when a source violates the pipeline's data contract."""


def _require_columns(frame: pd.DataFrame, table: str, columns: set[str]) -> None:
    missing = columns - set(frame.columns)
    if missing:
        raise DataValidationError(f"{table} is missing columns: {sorted(missing)}")


def validate(frames: dict[str, pd.DataFrame]) -> None:
    """Validate schemas, identifiers, relationships, and numeric ranges."""
    _require_columns(
        frames["parks"],
        "parks",
        {"park_code", "park_name", "state", "latitude", "longitude"},
    )
    _require_columns(
        frames["campgrounds"],
        "campgrounds",
        {"campground_id", "park_code", "tent_sites", "rv_sites", "nightly_fee_usd"},
    )
    _require_columns(frames["alerts"], "alerts", {"alert_id", "park_code", "category"})
    _require_columns(
        frames["weather"],
        "weather",
        {
            "park_code",
            "forecast_date",
            "temperature_high_f",
            "temperature_low_f",
            "precipitation_probability_pct",
        },
    )

    for table, key in (("parks", "park_code"), ("campgrounds", "campground_id"), ("alerts", "alert_id")):
        if frames[table][key].isna().any() or frames[table][key].duplicated().any():
            raise DataValidationError(f"{table}.{key} must be non-null and unique")

    park_codes = set(frames["parks"]["park_code"])
    for table in ("campgrounds", "alerts", "weather"):
        unknown = set(frames[table]["park_code"]) - park_codes
        if unknown:
            raise DataValidationError(f"{table} references unknown parks: {sorted(unknown)}")

    parks = frames["parks"]
    if not parks["latitude"].between(-90, 90).all():
        raise DataValidationError("park latitude must be between -90 and 90")
    if not parks["longitude"].between(-180, 180).all():
        raise DataValidationError("park longitude must be between -180 and 180")

    camps = frames["campgrounds"]
    if (camps[["tent_sites", "rv_sites", "nightly_fee_usd"]] < 0).any().any():
        raise DataValidationError("campground counts and fees cannot be negative")

    weather = frames["weather"]
    if (weather["temperature_high_f"] < weather["temperature_low_f"]).any():
        raise DataValidationError("weather high temperature cannot be below its low")
    if not weather["precipitation_probability_pct"].between(0, 100).all():
        raise DataValidationError("precipitation probability must be between 0 and 100")


def run_pipeline(
    *,
    source: str = "mock",
    as_of_date: date | None = None,
    seed: int = 42,
    output_root: Path | str = Path("data"),
) -> dict:
    """Execute one pipeline run and return its manifest."""
    if source != "mock":
        raise ValueError("Only the mock source is installed; the live adapter is student work.")

    as_of_date = as_of_date or datetime.now(UTC).date()
    output_root = Path(output_root)
    records = build_mock_data(as_of_date, seed)
    frames = {name: pd.DataFrame(records[name]) for name in TABLES}
    validate(frames)

    raw_dir = output_root / "raw" / source / as_of_date.isoformat()
    processed_dir = output_root / "processed"
    manifest_dir = output_root / "manifests"
    for folder in (raw_dir, processed_dir, manifest_dir):
        folder.mkdir(parents=True, exist_ok=True)

    for name in TABLES:
        (raw_dir / f"{name}.json").write_text(
            json.dumps(records[name], indent=2) + "\n", encoding="utf-8"
        )
        frames[name].to_parquet(processed_dir / f"{name}.parquet", index=False)

    warehouse = output_root / "warehouse.duckdb"
    temporary_warehouse = warehouse.with_name(f".{warehouse.name}.{uuid4().hex}.tmp")
    try:
        with duckdb.connect(str(temporary_warehouse)) as connection:
            for name in TABLES:
                parquet = (processed_dir / f"{name}.parquet").resolve()
                connection.execute(
                    f'CREATE OR REPLACE TABLE "{name}" AS SELECT * FROM read_parquet(?)',
                    [str(parquet)],
                )
        os.replace(temporary_warehouse, warehouse)
    finally:
        temporary_warehouse.unlink(missing_ok=True)

    manifest = {
        "source": source,
        "as_of_date": as_of_date.isoformat(),
        "seed": seed,
        "completed_at_utc": datetime.now(UTC).isoformat(),
        "record_counts": {name: len(frames[name]) for name in TABLES},
        "warehouse": str(warehouse),
    }
    (manifest_dir / "latest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest
