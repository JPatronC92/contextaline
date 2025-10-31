#!/usr/bin/env bash
set -e

CLEAN=${1:-""}
ONEFILE=${2:-""}

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python scripts/preload_model.py

if [ "$CLEAN" = "clean" ]; then
  rm -rf build dist __pycache__ || true
fi

if [ "$ONEFILE" = "onefile" ]; then
  pyinstaller --noconfirm --onefile --windowed src/app.py --name IntelligentDocumentFinder
else
  pyinstaller idf.spec
fi

echo "✅ Build listo en dist/"
