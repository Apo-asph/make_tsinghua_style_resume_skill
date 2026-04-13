# Codex Minimal Startup Package

这个压缩包面向 `Codex` 的最小启动场景，目标是让你解压后即可在项目根目录直接使用本地 skill 生成、编译和审查岗位定制简历。

## 包内包含

- `AGENTS.md`
- `skills/make-resume-variant/`
- `resume_master_source.md`
- `profile_photo.png`
- `latex template/resume_tsinghua_purple.tex`

说明：

- `AGENTS.md` 提供项目级规则与路由。
- `skills/make-resume-variant/` 包含 `Codex` 使用的技能说明、脚本、参考资料，以及 `agents/openai.yaml` 元数据。

## 开始使用

1. 解压压缩包。
2. 用你的真实信息替换 `resume_master_source.md`。
3. 用你的真实证件照替换 `profile_photo.png` 或改为 `profile_photo.jpg`。
4. 在解压目录根部启动 `Codex`。
5. 直接下达自然语言指令，调用项目内 skill。

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

- 这是最小启动包，只保留运行 `Codex` skill 所需的核心文件。
- 如果你需要同时兼容 `Claude Code`，请使用单独的 Claude Code 最小启动包。
