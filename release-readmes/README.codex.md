# Codex Minimal Startup Package

这个压缩包面向 `Codex` 的最小启动场景，目标是让你解压后即可在项目根目录直接使用本地 skill 采访补全信息母版，并生成、编译和审查岗位定制简历。

## 包内包含

- `AGENTS.md`
- `skills/interview-resume-source/`
- `skills/make-resume-variant/`
- `resume_master_source.md`
- `profile_photo.png`
- `latex template/resume_tsinghua_purple.tex`

说明：

- `AGENTS.md` 提供项目级规则与路由。
- `skills/interview-resume-source/` 用于分轮采访并补全 `resume_master_source.md`。
- `skills/make-resume-variant/` 用于基于母版生成岗位定制简历。

## 开始使用

1. 解压压缩包。
2. 用你的真实信息替换 `resume_master_source.md`。
3. 用你的真实证件照替换 `profile_photo.png` 或改为 `profile_photo.jpg`。
4. 在解压目录根部启动 `Codex`。
5. 直接下达自然语言指令，调用项目内 skill。

母版采访说明：

- 如果你还没有完整的 `resume_master_source.md`，可以先让 `Codex` 采访你。
- skill 会优先盘点母版里仍未补完的占位内容，再按轮次提问。
- 每轮回答后，agent 会直接回写 `resume_master_source.md`，并告诉你还缺哪些高优先级信息。

照片说明：

- 模板会自动保持照片原始纵横比。
- 常见的 `2:3`、`3:4`、`4:5`、`5:7`、`1:1` 比例通常都可直接使用。
- 如果照片比例过于极端，先运行 `python skills/make-resume-variant/scripts/prepare_photo.py <variant-photo-path>` 检查；只有在你同意后，再对解压目录内的照片副本执行居中裁取。

示例指令：

- “请采访我，分轮补全 `resume_master_source.md`，每轮先问最关键的 4 个问题。”
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
