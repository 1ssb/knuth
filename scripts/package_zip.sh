#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 OUTPUT_ZIP_PATH"
  exit 1
fi

OUTPUT_ZIP="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_NAME="$(basename "${REPO_ROOT}")"
PARENT_DIR="$(cd "${REPO_ROOT}/.." && pwd)"

cd "${PARENT_DIR}"
zip -r "${OUTPUT_ZIP}" "${REPO_NAME}"   -x "${REPO_NAME}/__pycache__/*"   -x "${REPO_NAME}/.pytest_cache/*"   -x "${REPO_NAME}/.git/*"
