# Manual Template Package

这个压缩包面向手动编辑 LaTeX 模板的使用场景，不包含任何 agent skill 结构。

## 包内包含

- `latex template/resume_tsinghua_purple.tex`
- `latex template/resume_tsinghua_purple.pdf`
- `resume_master_source.md`
- `profile_photo.png`

说明：

- `resume_tsinghua_purple.tex` 是手动编辑的模板源文件。
- `resume_tsinghua_purple.pdf` 是当前模板示例，便于快速查看排版风格。
- `resume_master_source.md` 可作为你整理事实信息的母版草稿，即使手动模式不强依赖它，也建议保留。

## 开始使用

1. 解压压缩包。
2. 打开 `latex template/resume_tsinghua_purple.tex`。
3. 手动替换其中的占位内容。
4. 准备你的真实照片，命名为 `profile_photo.png` 或 `profile_photo.jpg`，放在模板同目录下。
5. 在 `latex template/` 目录中运行编译命令。

推荐命令：

```bash
cd "latex template"
latexmk -xelatex resume_tsinghua_purple.tex
```

## 环境要求

- `xelatex`
- `latexmk`
- `ctex`

模板会优先尝试 `Avenir Next` / `Hiragino Sans GB`、`Segoe UI` / `Microsoft YaHei`，并在需要时回退到通用字体。

## 当前限制

- 这个包不包含 `Codex` 或 `Claude Code` 所需的 skill 文件。
- 如果你想通过自然语言驱动生成岗位定制简历，请改用对应的 agent 最小启动包。
