# Parks Capstone Workspace

A ready-to-go data workspace that runs in your browser: Python 3.12, R, DuckDB, Jupyter notebooks, and the usual stats, modeling, and mapping libraries, already installed.

It lives on a small Linux machine GitHub hosts for you (a *codespace*). Nothing installs on your laptop, nothing needs admin rights, and nothing you do in here can break in a way a rebuild won't fix.

## Open it

1. On this repo's GitHub page, click the green **Code** button → **Codespaces** tab.
2. Click **⋯** → **New with options**. Keep the defaults. At the bottom you can paste API keys (optional; see below). Click **Create codespace**.
   - The plain **Create codespace on main** button works too; it just skips the API key boxes.
3. The first setup takes about 5–10 minutes. After that it reopens in under a minute.
4. When it opens, open `notebooks/00_start_here.ipynb` and click **Run All**. If it asks for a kernel, pick the one with **.venv** in the name.

Prefer the desktop app? Install VS Code on Windows plus the **GitHub Codespaces** extension, and connect to the same codespace.

## Buttons instead of commands

Menu (☰) → **Terminal** → **Run Task…**

| Task | When |
|---|---|
| **Check my setup** (also Ctrl+Shift+B) | Anytime something feels off. Prints a ✅/❌ checklist. |
| **Install packages from requirements.txt** | After you add a package name to `requirements.txt`. |
| **Run tests** | Runs everything in `tests/`. |
| **Tidy code (format + lint)** | Cleans up formatting across the project. |

## Where things go

| Folder | What |
|---|---|
| `notebooks/` | Exploration and analysis. |
| `src/capstone/` | Code you reuse. Anything here imports into any notebook: `from capstone.config import RAW_DIR`. |
| `data/raw/` | Untouched pulls from APIs and downloads. |
| `data/processed/` | Cleaned, joined, model-ready data. |
| `data/warehouse.duckdb` | A local DuckDB database (created on first use). |
| `tests/` | Checks for your `src/` code. |

Data files never go to GitHub (size and licensing); code and notebooks do. To save work to GitHub: **Source Control** icon on the left → type a message → **Commit** → **Sync Changes**.

## API keys

| Source | What it has | Key |
|---|---|---|
| Open-Meteo | Weather forecasts and history | None needed |
| National Park Service API | Parks, alerts, closures, campgrounds | Free, instant: [nps.gov/subjects/developer/get-started.htm](https://www.nps.gov/subjects/developer/get-started.htm) |
| Recreation.gov (RIDB) | Facilities, campsites, recreation areas | Free with a Recreation.gov account: [ridb.recreation.gov](https://ridb.recreation.gov/) |

To add a key later: github.com → your profile picture → **Settings** → **Codespaces** → **New secret**. Name it `NPS_API_KEY` (or `RIDB_API_KEY`), paste the key, give this repo access, then stop and restart the codespace. In code:

```python
from capstone.config import get_secret

nps_key = get_secret("NPS_API_KEY")
```

Keys stay out of your code and out of git. (Pasting them into the `.env` file in this project also works; that file is never committed.)

## Adding packages

- **Python:** add a line to `requirements.txt`, then run the task **Install packages from requirements.txt**. Quick one-off from a notebook: `%pip install package-name`.
- **R:** `install.packages("package-name")` in an R notebook. It pulls prebuilt binaries, so it's quick.

No `sudo`, ever. Python packages install into this project's own `.venv`, R packages into your personal R library.

## When something's weird

- Run **Check my setup** first; it says what's wrong and how to fix it.
- Full reset: Ctrl+Shift+P → **Codespaces: Rebuild Container**. Your files in the repo survive. Packages you installed by hand don't, so put them in `requirements.txt`.
- Codespaces stop themselves after 30 idle minutes by default. A free GitHub account includes about 60 hours a month on this machine size; stop it from [github.com/codespaces](https://github.com/codespaces) when you're done for the day.

## If you open the terminal anyway

| Windows habit | Here |
|---|---|
| `dir` | `ls` |
| `cls` | `clear` |
| `type file.txt` | `cat file.txt` |
| `cd folder` | `cd folder` (same) |
| `python script.py` | `python script.py` (same, already uses `.venv`) |

---

## For whoever sets up the repo

```bash
cd parks-capstone-workspace
git init -b main
git add .
git commit -m "Capstone workspace"
gh repo create parks-capstone-workspace --private --source . --push   # or create it on github.com and push
```

Optional: repo **Settings** → check **Template repository**, so it can be copied with **Use this template**. Codespaces **prebuilds** (repo Settings → Codespaces) cut the first-open wait if it's opened often.

The environment is defined in `.devcontainer/devcontainer.json` (Ubuntu 24.04, R with binary CRAN packages via r2u, VS Code extensions, recommended secrets) and `.devcontainer/post-create.sh` (Python `.venv`, R kernel). The same config opens locally with Docker Desktop + VS Code's Dev Containers extension.
