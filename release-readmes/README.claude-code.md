# Claude Code Minimal Startup Package

这个压缩包面向 `Claude Code` 的最小启动场景，目标是让你解压后即可在项目根目录直接使用项目 skill 采访补全信息母版，并生成、编译和审查岗位定制简历。

## 包内包含

- `CLAUDE.md`
- `AGENTS.md`
- `.claude/skills/interview-resume-source/`
- `.claude/skills/make-resume-variant/`
- `skills/interview-resume-source/`
- `skills/make-resume-variant/`
- `resume_master_source.md`
- `profile_photo.png`
- `latex template/resume_tsinghua_purple.tex`

说明：

- `CLAUDE.md` 是 `Claude Code` 的项目入口。
- `.claude/skills/interview-resume-source/` 是 `Claude Code` 可识别的母版采访补全 skill 包装层。
- `.claude/skills/make-resume-variant/` 是 `Claude Code` 可识别的项目 skill 包装层。
- `skills/interview-resume-source/` 与 `skills/make-resume-variant/` 是共享的核心工作流、脚本与参考资料，仍是单一事实来源。

## 开始使用

1. 解压压缩包。
2. 用你的真实信息替换 `resume_master_source.md`。
3. 用你的真实证件照替换 `profile_photo.png` 或改为 `profile_photo.jpg`。
4. 在解压目录根部启动 `Claude Code`。
5. 让 `Claude Code` 先使用 `interview-resume-source` 补全母版，再按需要切换到 `make-resume-variant`。

母版采访说明：

- 如果你还没有完整的 `resume_master_source.md`，可以先让 `Claude Code` 采访你。
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

- 该包的目录结构已按 `Claude Code` 官方项目 skill 结构准备完成。
- 当前仓库没有安装 `Claude Code`，因此这份包未做实机交互测试。
- 共享工作流依然由 `skills/interview-resume-source/` 与 `skills/make-resume-variant/` 维护，不建议在 `.claude/skills/` 下另行分叉逻辑。
