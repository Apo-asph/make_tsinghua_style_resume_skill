#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
CLEANUP_SCRIPT="${SCRIPT_DIR}/cleanup_temp_files.sh"

export PATH="/Library/TeX/texbin:${PATH}"

usage() {
  echo "Usage: $0 <target-slug|absolute-variant-dir>" >&2
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

if ! command -v latexmk >/dev/null 2>&1; then
  echo "latexmk not found in PATH." >&2
  exit 1
fi

if ! command -v xelatex >/dev/null 2>&1; then
  echo "xelatex not found in PATH." >&2
  exit 1
fi

if [[ ! -x "${CLEANUP_SCRIPT}" ]]; then
  echo "Cleanup script not executable: ${CLEANUP_SCRIPT}" >&2
  exit 1
fi

INPUT_PATH="$1"
if [[ "${INPUT_PATH}" = /* ]]; then
  VARIANT_DIR="${INPUT_PATH}"
else
  VARIANT_DIR="${REPO_ROOT}/${INPUT_PATH}"
fi

if [[ ! -d "${VARIANT_DIR}" ]]; then
  echo "Variant directory not found: ${VARIANT_DIR}" >&2
  exit 1
fi

SLUG="$(basename "${VARIANT_DIR}")"
TEX_FILE="${VARIANT_DIR}/${SLUG}.tex"
PDF_FILE="${VARIANT_DIR}/${SLUG}.pdf"

if [[ ! -f "${TEX_FILE}" ]]; then
  echo "Expected TeX file not found: ${TEX_FILE}" >&2
  exit 1
fi

(
  cd "${VARIANT_DIR}"
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error "${SLUG}.tex"
)

if [[ ! -f "${PDF_FILE}" ]]; then
  echo "Expected PDF not found after compile: ${PDF_FILE}" >&2
  exit 1
fi

"${CLEANUP_SCRIPT}" "${VARIANT_DIR}"

printf '%s\n' "${PDF_FILE}"
