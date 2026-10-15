"""Project paths and API keys in one place, so notebooks never hard-code either."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
WAREHOUSE = DATA_DIR / "warehouse.duckdb"

for _folder in (RAW_DIR, PROCESSED_DIR):
    _folder.mkdir(parents=True, exist_ok=True)

# Codespaces secrets arrive as environment variables. A local .env file fills in
# anything missing but never overrides a real secret.
load_dotenv(PROJECT_ROOT / ".env", override=False)


def get_secret(name: str, required: bool = True) -> str | None:
    """Return an API key by name, e.g. get_secret("NPS_API_KEY")."""
    value = os.environ.get(name, "").strip()
    if value:
        return value
    if required:
        raise RuntimeError(
            f"{name} isn't set. Add it at github.com → Settings → Codespaces → Secrets "
            f"(give this repo access), then stop and restart the codespace. "
            f"Or paste it into the .env file in this project."
        )
    return None
