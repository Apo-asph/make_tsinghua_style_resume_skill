#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

export PATH="/opt/homebrew/bin:${PATH}"

usage() {
  echo "Usage: $0 <pdf-path> [preview-dir]" >&2
  echo "If preview-dir is omitted, previews are created under /tmp as temporary files." >&2
  echo "If preview-dir is provided, it is caller-owned and must be cleaned up before final delivery." >&2
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

if ! command -v gs >/dev/null 2>&1; then
  echo "Ghostscript (gs) not found in PATH." >&2
  exit 1
fi

PDF_INPUT="$1"
if [[ "${PDF_INPUT}" = /* ]]; then
  PDF_PATH="${PDF_INPUT}"
else
  PDF_PATH="${REPO_ROOT}/${PDF_INPUT}"
fi

if [[ ! -f "${PDF_PATH}" ]]; then
  echo "PDF not found: ${PDF_PATH}" >&2
  exit 1
fi

PDF_DIR="$(cd "$(dirname "${PDF_PATH}")" && pwd)"
PDF_NAME="$(basename "${PDF_PATH}")"
PDF_STEM="${PDF_NAME%.pdf}"

if [[ $# -eq 2 ]]; then
  PREVIEW_INPUT="$2"
  if [[ "${PREVIEW_INPUT}" = /* ]]; then
    PREVIEW_DIR="${PREVIEW_INPUT}"
  else
    PREVIEW_DIR="${PDF_DIR}/${PREVIEW_INPUT}"
  fi
  mkdir -p "${PREVIEW_DIR}"
else
  SAFE_STEM="${PDF_STEM// /_}"
  PREVIEW_DIR="$(mktemp -d "/tmp/${SAFE_STEM}-preview-XXXXXX")"
fi

gs \
  -dSAFER \
  -dBATCH \
  -dNOPAUSE \
  -sDEVICE=pngalpha \
  -r144 \
  -o "${PREVIEW_DIR}/page-%02d.png" \
  "${PDF_PATH}" >/dev/null

PAGE_COUNT="$(find "${PREVIEW_DIR}" -maxdepth 1 -type f -name 'page-*.png' | wc -l | tr -d ' ')"

if [[ "${PAGE_COUNT}" = "0" ]]; then
  echo "No preview images were generated for ${PDF_PATH}" >&2
  exit 1
fi

printf 'pdf=%s\n' "${PDF_PATH}"
printf 'page_count=%s\n' "${PAGE_COUNT}"
printf 'preview_dir=%s\n' "${PREVIEW_DIR}"
