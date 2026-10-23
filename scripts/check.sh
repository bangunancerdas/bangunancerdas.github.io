#!/usr/bin/env bash
# Runs every quality check CI runs. Usage: ./scripts/check.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Python checks (links, assets, SEO, sitemap, WhatsApp, structure)"
python3 -m unittest discover -s tests -t . -v

echo "==> JavaScript tests (theme, analytics)"
node --test tests/js

echo "==> HTML validation (Nu HTML Checker)"
./scripts/validate-html.sh

echo "All checks passed."
