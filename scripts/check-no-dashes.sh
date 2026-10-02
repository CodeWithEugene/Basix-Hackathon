#!/usr/bin/env bash
# Fail if any user-facing copy contains an em dash or en dash.
# Scope: web/app, web/components/mizani, web/lib.
set -euo pipefail
cd "$(dirname "$0")/.."

hits=$(grep -RnP '[\x{2014}\x{2013}]' \
  web/app web/components/mizani web/lib 2>/dev/null \
  --include='*.ts' --include='*.tsx' --include='*.json' \
  | grep -v '^\S*globals.css' || true)

if [[ -n "$hits" ]]; then
  echo "em/en dashes found in UI copy:" >&2
  echo "$hits" >&2
  exit 1
fi
echo "no em/en dashes in UI copy"
