# Claude Code Minimal Startup Package

这个压缩包面向 `Claude Code` 的最小启动场景，目标是让你解压后即可在项目根目录直接使用项目 skill 生成、编译和审查岗位定制简历。

## 包内包含

- `CLAUDE.md`
- `AGENTS.md`
- `.claude/skills/make-resume-variant/`
- `skills/make-resume-variant/`
- `resume_master_source.md`
- `profile_photo.png`
- `latex template/resume_tsinghua_purple.tex`

说明：

- `CLAUDE.md` 是 `Claude Code` 的项目入口。
- `.claude/skills/make-resume-variant/` 是 `Claude Code` 可识别的项目 skill 包装层。
- `skills/make-resume-variant/` 是共享的核心工作流、脚本与参考资料，仍是单一事实来源。

## 开始使用

1. 解压压缩包。
2. 用你的真实信息替换 `resume_master_source.md`。
3. 用你的真实证件照替换 `profile_photo.png` 或改为 `profile_photo.jpg`。
4. 在解压目录根部启动 `Claude Code`。
5. 让 `Claude Code` 使用 `make-resume-variant` 项目 skill。

示例指令：

- “请为 xx 公司的算法工程师岗位生成一页版简历。”
- “请根据 `resume_master_source.md` 生成一版 AI for Science 方向简历，并编译检查版式。”

## 环境要求

- `python3` 或可用的 `python`
- `xelatex`
- `latexmk`
- `ctex`
- `ghostscript`

若 `latexmk`、`xelatex`、Ghostscript 未加入 `PATH`，脚本会优先尝试常见的 Windows 安装目录；仍失败时，可通过 `LATEXMK`、`XELATEX`、`GHOSTSCRIPT` 环境变量显式指定路径。

## 当前限制

- 该包的目录结构已按 `Claude Code` 官方项目 skill 结构准备完成。
- 当前仓库没有安装 `Claude Code`，因此这份包未做实机交互测试。
- 共享工作流依然由 `skills/make-resume-variant/` 维护，不建议在 `.claude/skills/` 下另行分叉逻辑。
