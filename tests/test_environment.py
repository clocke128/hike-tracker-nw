"""Quick checks that the environment is wired up. Run with the task "Run tests".

Put tests for your own code (src/capstone) in this folder too.
"""

import duckdb
import pandas as pd

from capstone.config import PROCESSED_DIR, RAW_DIR, get_secret


def test_data_folders_exist():
    assert RAW_DIR.is_dir()
    assert PROCESSED_DIR.is_dir()


def test_duckdb_reads_a_dataframe():
    con = duckdb.connect()
    con.register(
        "highs", pd.DataFrame({"park": ["Zion", "Zion", "Yosemite"], "high_f": [71, 75, 64]})
    )
    rows = con.sql("SELECT park, avg(high_f) FROM highs GROUP BY park ORDER BY park").fetchall()
    assert rows == [("Yosemite", 64.0), ("Zion", 73.0)]


def test_missing_optional_secret_returns_none(monkeypatch):
    monkeypatch.delenv("SOME_KEY_THAT_IS_NOT_SET", raising=False)
    assert get_secret("SOME_KEY_THAT_IS_NOT_SET", required=False) is None
