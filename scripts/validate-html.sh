#!/usr/bin/env bash
# Validates every published HTML page with the Nu HTML Checker (the W3C validator engine).
# Requires Java and npm. The checker jar is downloaded once into a cache directory.
set -euo pipefail

VNU_VERSION="24.10.17"
cache_dir="${VNU_DIR:-${TMPDIR:-/tmp}/bangunancerdas-vnu-${VNU_VERSION}}"
jar="${cache_dir}/node_modules/vnu-jar/build/dist/vnu.jar"

if [ ! -f "${jar}" ]; then
  npm install --prefix "${cache_dir}" --no-save --no-audit --no-fund "vnu-jar@${VNU_VERSION}" >/dev/null
fi

cd "$(dirname "$0")/.."
# Warnings are fatal. The ignored message is a style note about the existing "<meta ... />" syntax.
java -jar "${jar}" --Werror --filterpattern 'Trailing slash on void elements.*' \
  index.html 404.html blog/*.html
