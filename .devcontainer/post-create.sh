#!/usr/bin/env bash
# Runs once, automatically, when the codespace is created. Nobody needs to run this by hand.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Python: creating the project environment in .venv"
python3 -m venv .venv
.venv/bin/python -m pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt
.venv/bin/pip install --quiet -e .

echo "==> R: personal package library + fast binary installs from Posit Package Manager"
R_USER_LIB="$(Rscript -e 'cat(Sys.getenv("R_LIBS_USER"))')"
mkdir -p "$R_USER_LIB"
cat > "$HOME/.Rprofile" <<'EOF'
local({
  options(repos = c(CRAN = "https://packagemanager.posit.co/cran/__linux__/noble/latest"))
  options(HTTPUserAgent = sprintf("R/%s R (%s)", getRversion(),
    paste(getRversion(), R.version["platform"], R.version["arch"], R.version["os"])))
})
EOF

echo "==> Jupyter: registering the R kernel"
PATH="$PWD/.venv/bin:$PATH" Rscript -e 'IRkernel::installspec(user = TRUE, name = "ir", displayname = "R")'

echo "==> Folders and local settings"
mkdir -p data/raw data/processed
[ -f .env ] || cp .env.example .env

echo
echo "All set. Run the 'Check my setup' task (Ctrl+Shift+B) to confirm everything."
