"""One-click health check for the workspace. Run via the task "Check my setup" (Ctrl+Shift+B)."""

import importlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

OK, WARN, FAIL = "✅", "⚠️ ", "❌"
problems: list[str] = []
notes: list[str] = []

PY_PACKAGES = [
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("pyarrow", "pyarrow"),
    ("duckdb", "duckdb"),
    ("scipy", "scipy"),
    ("sklearn", "scikit-learn"),
    ("statsmodels", "statsmodels"),
    ("matplotlib", "matplotlib"),
    ("plotly", "plotly"),
    ("geopandas", "geopandas"),
    ("requests", "requests"),
    ("dotenv", "python-dotenv"),
    ("capstone.config", "capstone (your src/ code)"),
]
R_PACKAGES = ["dplyr", "ggplot2", "duckdb", "arrow", "sf", "httr2", "IRkernel"]
SECRETS = {
    "NPS_API_KEY": "https://www.nps.gov/subjects/developer/get-started.htm",
    "RIDB_API_KEY": "https://ridb.recreation.gov/",
}


def line(icon: str, label: str, detail: str = "") -> None:
    print(f"  {icon} {label:<28} {detail}")


def section(title: str) -> None:
    print(f"\n{title}")


section("Python")
in_venv = sys.prefix != sys.base_prefix
line(
    OK if in_venv else WARN,
    f"Python {sys.version.split()[0]}",
    "project .venv" if in_venv else "not the project .venv",
)
if not in_venv:
    notes.append("Pick the interpreter/kernel that has .venv in its name.")
for module, label in PY_PACKAGES:
    try:
        mod = importlib.import_module(module)
        line(OK, label, getattr(mod, "__version__", ""))
    except Exception as exc:  # noqa: BLE001 - report anything that stops an import
        line(FAIL, label, f"won't import ({type(exc).__name__})")
        problems.append(
            f"Python package {label} is missing; run the task "
            "'Install packages from requirements.txt'."
        )

section("R")
rscript = shutil.which("Rscript")
if not rscript:
    line(WARN, "R", "not installed here")
    notes.append("R isn't installed in this environment (fine if you're only using Python).")
else:
    version = subprocess.run(
        [rscript, "-e", "cat(format(getRversion()))"], check=False, capture_output=True, text=True
    ).stdout.strip()
    line(OK, f"R {version}")
    pkgs = ", ".join(f'"{p}"' for p in R_PACKAGES)
    probe = (
        f"pk <- c({pkgs}); ok <- vapply(pk, requireNamespace, logical(1), quietly = TRUE); "
        "cat(paste(pk, ok, sep='='), sep='\\n')"
    )
    out = subprocess.run([rscript, "-e", probe], check=False, capture_output=True, text=True).stdout
    for row in out.split():
        name, _, ok = row.partition("=")
        line(OK if ok == "TRUE" else FAIL, name, "" if ok == "TRUE" else "missing")
        if ok != "TRUE":
            problems.append(f"R package {name} is missing; rebuild the codespace.")

section("Notebook kernels")
jupyter = Path(sys.executable).with_name("jupyter")
try:
    specs = json.loads(
        subprocess.run(
            [str(jupyter), "kernelspec", "list", "--json"],
            check=False,
            capture_output=True,
            text=True,
        ).stdout
    )["kernelspecs"]
    line(OK, "Python", "use the .venv interpreter")
    if "ir" in specs:
        line(OK, "R", "registered")
    elif rscript:
        line(FAIL, "R", "not registered")
        problems.append("R kernel isn't registered; rebuild the codespace.")
except Exception:  # noqa: BLE001
    line(WARN, "Kernels", "couldn't list them")

section("API keys (values never shown)")
for name, url in SECRETS.items():
    if os.environ.get(name, "").strip():
        line(OK, name, "set")
    else:
        line(WARN, name, "not set (optional)")
        notes.append(f"{name}: get one at {url}, then add it as a Codespaces secret.")

section("Internet")
try:
    import requests

    requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 37.75,
            "longitude": -119.59,
            "daily": "temperature_2m_max",
            "forecast_days": 1,
        },
        timeout=8,
    ).raise_for_status()
    line(OK, "Open-Meteo weather API", "reachable")
except Exception as exc:  # noqa: BLE001
    line(WARN, "Open-Meteo weather API", f"not reachable ({type(exc).__name__})")
    notes.append("Couldn't reach the weather API; check your connection and try again.")

where = "GitHub Codespaces" if os.environ.get("CODESPACES") == "true" else "a local container"
print(f"\nRunning in {where}.")
if notes:
    print("\nNotes:")
    for n in notes:
        print(f"  - {n}")
if problems:
    print(f"\n{FAIL} Something needs fixing:")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)
print(f"\n{OK} Everything required is working.")
