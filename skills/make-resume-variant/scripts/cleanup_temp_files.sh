#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

usage() {
  echo "Usage: $0 [path ...]" >&2
  echo "If no path is provided, cleanup runs on the repo root." >&2
}

normalize_path() {
  local input="$1"
  if [[ "${input}" = /* ]]; then
    printf '%s\n' "${input}"
  else
    printf '%s\n' "${REPO_ROOT}/${input}"
  fi
}

cleanup_target() {
  local target="$1"
  local target_name

  target_name="$(basename "${target}")"

  if [[ ! -e "${target}" ]]; then
    echo "Cleanup target not found, skipping: ${target}" >&2
    return 0
  fi

  case "${target_name}" in
    preview|preview_v2|.ocr-tmp|*-preview-*)
      rm -rf "${target}"
      return 0
      ;;
  esac

  while IFS= read -r -d '' dir_path; do
    rm -rf "${dir_path}"
  done < <(
    find "${target}" -depth -type d \
      \( -name 'preview' -o -name 'preview_v2' -o -name '.ocr-tmp' -o -name '*-preview-*' \) \
      -print0
  )

  if [[ ! -e "${target}" ]]; then
    return 0
  fi

  while IFS= read -r -d '' file_path; do
    rm -f "${file_path}"
  done < <(
    find "${target}" -type f \
      \( -name '.DS_Store' \
      -o -name '*.aux' \
      -o -name '*.log' \
      -o -name '*.out' \
      -o -name '*.fls' \
      -o -name '*.fdb_latexmk' \
      -o -name '*.xdv' \
      -o -name '*.synctex*' \
      -o -name 'missfont.log' \) \
      -print0
  )
}

if [[ $# -gt 0 && ( "$1" = "-h" || "$1" = "--help" ) ]]; then
  usage
  exit 0
fi

if [[ $# -eq 0 ]]; then
  cleanup_target "${REPO_ROOT}"
else
  for raw_target in "$@"; do
    cleanup_target "$(normalize_path "${raw_target}")"
  done
fi
