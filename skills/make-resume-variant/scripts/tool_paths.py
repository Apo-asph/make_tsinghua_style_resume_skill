#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Dict, Iterable, Optional, Sequence, Tuple


WINDOWS_ROOT_ENV_VARS = (
    "PROGRAMW6432",
    "PROGRAMFILES",
    "PROGRAMFILES(X86)",
    "LOCALAPPDATA",
    "APPDATA",
)

LATEXMK_PATH_CANDIDATES = ("latexmk", "latexmk.exe", "latexmk.bat", "latexmk.cmd")
XELATEX_PATH_CANDIDATES = ("xelatex", "xelatex.exe")
GHOSTSCRIPT_PATH_CANDIDATES = (
    "gs",
    "gs.exe",
    "gswin64c",
    "gswin64c.exe",
    "gswin32c",
    "gswin32c.exe",
)

LATEXMK_WINDOWS_PATTERNS = (
    "TeX Live/*/bin/win32/latexmk.exe",
    "TeX Live/*/bin/win32/latexmk.bat",
    "MiKTeX/miktex/bin/x64/latexmk.exe",
    "MiKTeX/miktex/bin/latexmk.exe",
    "Programs/MiKTeX/miktex/bin/x64/latexmk.exe",
    "Programs/MiKTeX/miktex/bin/latexmk.exe",
)

XELATEX_WINDOWS_PATTERNS = (
    "TeX Live/*/bin/win32/xelatex.exe",
    "MiKTeX/miktex/bin/x64/xelatex.exe",
    "MiKTeX/miktex/bin/xelatex.exe",
    "Programs/MiKTeX/miktex/bin/x64/xelatex.exe",
    "Programs/MiKTeX/miktex/bin/xelatex.exe",
)

GHOSTSCRIPT_WINDOWS_PATTERNS = (
    "gs/gs*/bin/gswin64c.exe",
    "gs/gs*/bin/gswin32c.exe",
    "Ghostscript/gs*/bin/gswin64c.exe",
    "Ghostscript/gs*/bin/gswin32c.exe",
)


class CommandResolutionError(RuntimeError):
    pass


def is_windows() -> bool:
    return os.name == "nt"


def resolve_explicit_command(candidate: Optional[str]) -> Optional[str]:
    if not candidate:
        return None

    explicit_path = Path(candidate).expanduser()
    if explicit_path.is_file():
        return str(explicit_path)

    return shutil.which(candidate)


def iter_windows_roots() -> Iterable[Path]:
    seen = set()
    for env_name in WINDOWS_ROOT_ENV_VARS:
        env_value = os.environ.get(env_name)
        if not env_value:
            continue
        root = Path(env_value).expanduser()
        if not root.exists():
            continue
        root_str = str(root)
        if root_str in seen:
            continue
        seen.add(root_str)
        yield root


def search_windows_patterns(patterns: Sequence[str]) -> Optional[str]:
    for root in iter_windows_roots():
        for pattern in patterns:
            matches = sorted(root.glob(pattern), reverse=True)
            for match in matches:
                if match.is_file():
                    return str(match)
    return None


def find_command(
    display_name: str,
    path_candidates: Sequence[str],
    env_vars: Sequence[str],
    windows_patterns: Sequence[str],
) -> str:
    for env_var in env_vars:
        resolved = resolve_explicit_command(os.environ.get(env_var))
        if resolved:
            return resolved

    for path_candidate in path_candidates:
        resolved = shutil.which(path_candidate)
        if resolved:
            return resolved

    if is_windows():
        resolved = search_windows_patterns(windows_patterns)
        if resolved:
            return resolved
        raise CommandResolutionError(
            f"{display_name} not found. Checked {', '.join(env_vars)}, PATH, and common Windows install directories.",
        )

    raise CommandResolutionError(f"{display_name} not found in PATH.")


def find_latexmk() -> str:
    return find_command(
        display_name="latexmk",
        path_candidates=LATEXMK_PATH_CANDIDATES,
        env_vars=("LATEXMK",),
        windows_patterns=LATEXMK_WINDOWS_PATTERNS,
    )


def find_xelatex() -> str:
    return find_command(
        display_name="xelatex",
        path_candidates=XELATEX_PATH_CANDIDATES,
        env_vars=("XELATEX",),
        windows_patterns=XELATEX_WINDOWS_PATTERNS,
    )


def find_ghostscript() -> str:
    return find_command(
        display_name="Ghostscript",
        path_candidates=GHOSTSCRIPT_PATH_CANDIDATES,
        env_vars=("GHOSTSCRIPT", "GS"),
        windows_patterns=GHOSTSCRIPT_WINDOWS_PATTERNS,
    )


def build_command_env(command_paths: Sequence[str]) -> Dict[str, str]:
    env = os.environ.copy()
    existing_path = env.get("PATH", "")
    parent_dirs = []

    for command_path in command_paths:
        parent_dir = str(Path(command_path).resolve().parent)
        if parent_dir not in parent_dirs:
            parent_dirs.append(parent_dir)

    if existing_path:
        env["PATH"] = os.pathsep.join(parent_dirs + [existing_path])
    else:
        env["PATH"] = os.pathsep.join(parent_dirs)

    return env
