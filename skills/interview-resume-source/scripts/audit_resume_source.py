#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TARGET = REPO_ROOT / "resume_master_source.md"
PLACEHOLDER_PATTERN = re.compile(r"\[[^\[\]]+\]")
ACTIONABLE_TOP_LEVEL_SECTIONS = {
    "二、基础信息",
    "三、个人定位与关键词",
    "四、教育背景",
    "五、主修课程（可按岗位裁剪）",
    "六、技能与工具栈",
    "七、实习 / 工作 / 项目经历",
    "八、论文与学术成果",
    "九、学术会议",
    "十、奖励与荣誉",
    "十一、组织与服务经历",
}
DEFAULT_LITERAL_TOKENS = (
    "候选人姓名",
    "+86 138-0000-0000",
    "name@example.com",
    "github.com/username",
    "homepage.example.com",
    "城市 1",
    "城市 2",
)


@dataclass(frozen=True)
class Finding:
    section: str
    line_no: int
    text: str


def resolve_target_path(raw_path: Optional[str]) -> Path:
    if not raw_path:
        return DEFAULT_TARGET
    path = Path(raw_path)
    return path if path.is_absolute() else REPO_ROOT / path


def line_has_unresolved_marker(line: str) -> bool:
    if PLACEHOLDER_PATTERN.search(line):
        return True
    return any(token in line for token in DEFAULT_LITERAL_TOKENS)


def iter_findings(lines: Iterable[str]) -> List[Finding]:
    findings: List[Finding] = []
    current_top_level: Optional[str] = None
    in_code_block = False

    for line_no, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped.startswith("## "):
            current_top_level = stripped[3:].strip()
            continue
        if current_top_level not in ACTIONABLE_TOP_LEVEL_SECTIONS:
            continue
        if not stripped or stripped == "---" or stripped.startswith(">"):
            continue
        if line_has_unresolved_marker(stripped):
            findings.append(Finding(section=current_top_level, line_no=line_no, text=stripped))

    return findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit unresolved placeholders and default sample values in resume_master_source.md.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Target markdown file. Relative paths are resolved from the repo root.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    target_path = resolve_target_path(args.target)

    if not target_path.is_file():
        raise SystemExit(f"Target file not found: {target_path}")

    findings = iter_findings(target_path.read_text(encoding="utf-8").splitlines())
    grouped: "OrderedDict[str, List[Finding]]" = OrderedDict()
    for finding in findings:
        grouped.setdefault(finding.section, []).append(finding)

    print(f"path={target_path}")
    print(f"unresolved_count={len(findings)}")
    print(f"section_count={len(grouped)}")
    for section, section_findings in grouped.items():
        print(f"section={section}|count={len(section_findings)}")
        for finding in section_findings:
            print(f"finding={finding.line_no}|{finding.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
