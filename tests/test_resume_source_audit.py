from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = REPO_ROOT / "skills" / "interview-resume-source" / "scripts" / "audit_resume_source.py"


class ResumeSourceAuditTests(unittest.TestCase):
    def test_audit_reports_actionable_placeholders(self) -> None:
        content = """# 示例

## 二、基础信息
- 姓名：[候选人姓名]
- 联系电话：[+86 138-0000-0000]

## 四、教育背景
### 1）[学校名称] [学位]
- 时间：[YYYY-MM ~ YYYY-MM]

## 十二、子版生成建议
- 保留：[教育背景]

## 十三、快速抽取字段（供后续生成子版）
```yaml
{"name": "[候选人姓名]"}
```
"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_path = Path(tmp_dir) / "resume_master_source.md"
            target_path.write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(AUDIT_SCRIPT), str(target_path)],
                text=True,
                capture_output=True,
                check=True,
            )

        self.assertIn("unresolved_count=4", result.stdout)
        self.assertIn("section=二、基础信息|count=2", result.stdout)
        self.assertIn("section=四、教育背景|count=2", result.stdout)
        self.assertNotIn("十二、子版生成建议", result.stdout)
        self.assertNotIn("十三、快速抽取字段", result.stdout)

    def test_audit_returns_zero_for_resolved_actionable_sections(self) -> None:
        content = """# 示例

## 二、基础信息
- 姓名：张三
- 联系电话：+86 139-1234-5678

## 三、个人定位与关键词
**核心定位**：面向算法研发岗位的硕士候选人。
"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_path = Path(tmp_dir) / "resume_master_source.md"
            target_path.write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(AUDIT_SCRIPT), str(target_path)],
                text=True,
                capture_output=True,
                check=True,
            )

        self.assertIn("unresolved_count=0", result.stdout)
        self.assertIn("section_count=0", result.stdout)
