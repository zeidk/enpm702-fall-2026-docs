#!/usr/bin/env bash
# Copy the L12 interactive slides (built by make_interactive.py in the slides repo)
# into docs/source/_extra/lectures/lecture12/interactive/, which Sphinx serves as is.
# Replaces only that folder. Run from the docs repo root.
set -euo pipefail
SRC="${1:-../../latex/enpm702-fall-2026-beamer/slides/lectures/lecture12/interactive}"
DST="docs/source/_extra/lectures/lecture12/interactive"
for p in L12_interactive.html L12_interactive_assets katex; do
  [ -e "$SRC/$p" ] || { echo "missing: $SRC/$p" >&2; exit 1; }
done
rm -rf "$DST"
mkdir -p "$DST"
cp -r "$SRC/L12_interactive.html" "$SRC/L12_interactive_assets" "$SRC/katex" "$DST/"
du -sh "$DST"
