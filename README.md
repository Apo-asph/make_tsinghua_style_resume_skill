# make_tsinghua_style_resume_skill

一个面向中文求职场景的 LaTeX 简历项目，包含：

- 一套清华紫色调、简约风的简历模板；
- 一个用于维护完整事实信息的信息母版；
- 一套可被 `Codex` 与 `Claude Code` 共同复用的本地 skill 工作流，用自然语言生成、编译、审查和微调岗位定制简历；
- 一个可分发的 release 打包形态。

## 当前状态

当前版本：`v0.3.0`

这是首个同时兼容 `Codex` 与 `Claude Code` 项目 skill 结构的版本。

`v0.3.0` 范围：

- 提供 `resume_tsinghua_purple.tex` LaTeX 模板；
- 提供 `resume_master_source.md` 信息母版模板；
- 提供 `profile_photo.png` 照片占位文件；
- 提供适用于 `Codex + Claude Code + macOS / Windows` 的本地 skill 与脚本工作流。
- 提供跨平台 Python 脚本入口，并保留 `.sh` 包装层兼容 `macOS` / `Linux`。
- 为模板补充跨平台字体回退，降低不同系统下的首次编译门槛。
- 增加 `CLAUDE.md` 与 `.claude/skills/` 兼容层，使共享仓库可直接被 `Claude Code` 识别。

当前已知范围限制：

- 共享工作流仍以仓库内的 `Codex` skill 为单一事实来源，`Claude Code` 通过兼容包装层复用；
- 仍依赖本地安装的 `xelatex`、`latexmk`、`ctex` 与 `ghostscript`；
- 若系统字体不包含推荐字体，将自动回退到可用字体，但不同平台的细微版式仍可能略有差异。
- 当前仓库已补齐 `Claude Code` 结构兼容，但由于当前开发环境未安装 `Claude Code`，尚未完成实机交互测试。

## 后续计划

计划中的后续版本包括：

- 补充 `Claude Code` 的实机验证与细节打磨；
- 继续完善 release 结构与跨平台可用性。

## 项目结构

- `latex template/resume_tsinghua_purple.tex`
  简历模板本体。
- `latex template/resume_tsinghua_purple.pdf`
  当前模板示例 PDF。
- `resume_master_source.md`
  信息母版模板，需替换为你自己的真实信息。
- `profile_photo.png`
  照片占位文件，建议替换为标准 `5:7` 比例的真实照片。
- `CLAUDE.md`
  `Claude Code` 的项目级指令入口，复用 `AGENTS.md`。
- `.claude/skills/make-resume-variant/`
  `Claude Code` 使用的项目 skill 包装层。
- `skills/make-resume-variant/`
  共享的核心 skill、脚本与参考资料，当前仍是单一事实来源。
- `AGENTS.md`
  agent 在项目根目录下工作的规则说明。
- `make_tsinghua_style_resume_skill-release-claude-code-minimal-v0.3.0.zip`
  面向 `Claude Code` 的最小启动包。
- `make_tsinghua_style_resume_skill-release-codex-minimal-v0.3.0.zip`
  面向 `Codex` 的最小启动包。
- `make_tsinghua_style_resume_skill-release-manual-template-v0.3.0.zip`
  面向手动编辑 LaTeX 模板的最小模板包。

## 命名约定

项目默认采用以下命名：

- 信息母版文件：`resume_master_source.md`
- 照片文件基础名：`profile_photo`
- 模板文件：`latex template/resume_tsinghua_purple.tex`

建议手动模式和 agent 模式都保持这些文件名不变，以减少额外配置。

注意：

- 信息母版文件名是工作流中的显式依赖文件名，用户不应自行更改：
  `resume_master_source.md`
- 照片文件的基础文件名固定为 `profile_photo`，支持的完整文件名为：
  `profile_photo.png`
  `profile_photo.jpg`

## 使用方式

### 1. 手动使用模板

如果你只想手动修改 LaTeX 简历：

1. 使用 `latex template/resume_tsinghua_purple.tex`。
2. 替换其中的占位内容。
3. 将你的真实照片放在同目录下，并命名为 `profile_photo.png` 或 `profile_photo.jpg`。
4. 确保 LaTeX 编译环境可用后执行编译。

推荐命令：

```bash
cd "latex template"
latexmk -xelatex resume_tsinghua_purple.tex
```

手动模式的基本要求：

- `xelatex`
- `latexmk`
- `ctex`

说明：

- 模板默认使用 XeLaTeX。
- 模板现在会优先尝试：
  `Avenir Next` / `Hiragino Sans GB`（`macOS`）
  `Segoe UI` / `Microsoft YaHei`（`Windows`）
  `TeX Gyre Heros` / `FandolHei-Regular`（通用回退）
- 因此多数 `macOS` / `Windows` 环境无需先手改字体配置即可完成首次编译。
- 手动模式下，模板支持的照片格式为：
  `profile_photo.png`
  `profile_photo.jpg`
- 若目录中没有 `profile_photo.png` / `profile_photo.jpg`，模板会显示占位框，不会因缺照片而直接编译失败。

### 2. 使用 Codex + Skill

如果你希望通过自然语言自动制作简历：

1. 将 release 包内容拷贝到一个空文件夹。
2. 先用自己的真实信息替换：
   `resume_master_source.md`
   `profile_photo.png` 或 `profile_photo.jpg`
3. 以该文件夹为根目录启动 `Codex`。
4. `Codex` 识别到 `AGENTS.md` 和 `skills/make-resume-variant/` 后，即可按自然语言指令工作。

示例指令：

- “请为 xx 公司的算法工程师岗位生成一页版简历。”
- “请根据 `resume_master_source.md` 生成一版 AI for Science 方向简历，并编译检查版式。”
- “请把当前版本压缩到一页，并保留科研与 Agent 相关项目。”

### 3. 使用 Claude Code + Project Skill

如果你希望通过 `Claude Code` 使用同一套项目工作流：

1. 将 release 包内容拷贝到一个空文件夹。
2. 先用自己的真实信息替换：
   `resume_master_source.md`
   `profile_photo.png` 或 `profile_photo.jpg`
3. 以该文件夹为根目录启动 `Claude Code`。
4. `Claude Code` 会读取根目录的 `CLAUDE.md`，并发现项目 skill：
   `.claude/skills/make-resume-variant/SKILL.md`
5. 该 Claude Code skill 会继续复用仓库中的共享工作流：
   `skills/make-resume-variant/SKILL.md`

示例指令：

- “请为 xx 公司的算法工程师岗位生成一页版简历。”
- “请根据 `resume_master_source.md` 生成一版 AI for Science 方向简历，并编译检查版式。”
- “请把当前版本压缩到一页，并保留科研与 Agent 相关项目。”

### 4. 如何选择 release

- 如果你准备在 `Claude Code` 中直接使用项目 skill，并希望包内自带 `CLAUDE.md` 与 `.claude/skills/` 结构，使用：
  `make_tsinghua_style_resume_skill-release-claude-code-minimal-v0.3.0.zip`
- 如果你准备在 `Codex` 中直接使用项目 skill，并希望包内自带 `AGENTS.md` 与 `skills/make-resume-variant/`，使用：
  `make_tsinghua_style_resume_skill-release-codex-minimal-v0.3.0.zip`
- 如果你只想手动编辑 LaTeX，不使用任何 agent skill，只需要模板、示例 PDF 与基础素材，使用：
  `make_tsinghua_style_resume_skill-release-manual-template-v0.3.0.zip`

## release / agent 模式环境要求

当前 release 为 `Codex + Claude Code + macOS / Windows` 的 `v0.3.0` 版本，默认脚本入口为 Python。

若要完整使用 skill 的自动编译、审查和清理能力，建议环境中至少具备：

- `macOS` 或 `Windows`
- `python3`（或可用的 `python` 命令）
- `xelatex`
- `latexmk`
- `ctex`
- `ghostscript`

脚本层面的具体假设：

- `skills/make-resume-variant/scripts/compile_resume.py`
  依赖 `python3`、`latexmk` 与 `xelatex`；若它们不在 `PATH` 中，会继续探测常见的 `TeX Live` / `MiKTeX` Windows 安装目录。
- `skills/make-resume-variant/scripts/inspect_resume_pdf.py`
  依赖 `python3` 与 Ghostscript，兼容 `gs`、`gswin64c`、`gswin32c`；若它们不在 `PATH` 中，会继续探测常见的 Windows 安装目录。
- `skills/make-resume-variant/scripts/cleanup_temp_files.py`
  依赖 `python3`，不再依赖 `bash`、`find`、`rm` 等 Unix 命令。
- 同名 `.sh` 包装脚本继续保留，方便 `macOS` / `Linux` 用户沿用旧命令。

因此：

- 当前 release 可在原生 `Windows` 的 `PowerShell` / `CMD` 中使用 Python 入口脚本；
- `macOS` / `Linux` 用户可继续使用 `.sh` 命令，也可统一改用 Python 入口；
- 即使 `latexmk`、`xelatex`、Ghostscript 未加入 `PATH`，脚本也会优先尝试常见 Windows 安装目录；若仍失败，可通过 `LATEXMK`、`XELATEX`、`GHOSTSCRIPT` 环境变量显式指定可执行文件路径。
- `Codex` 与 `Claude Code` 现在可以在同一仓库中共享同一套模板、脚本与信息母版，无需拆分分支；若后续要发布不同面向的压缩包，可在 release 阶段再按 agent 形态拆分。

## 开始前必须替换的文件

按使用方式区分：

- 手动模式：
  不要求先替换 `resume_master_source.md`；你只需要直接修改 `resume_tsinghua_purple.tex` 的内容，并准备好同目录下的真实照片文件。
- `Codex` / release 模式：
  开始前应先替换以下依赖文件，并保持命名规则不变：
  `resume_master_source.md`
  `profile_photo.png` 或 `profile_photo.jpg`

其中：

- `resume_master_source.md` 应填写你的真实教育、项目、论文、技能、荣誉等信息；
- `profile_photo.png` 或 `profile_photo.jpg` 应替换为你的真实照片，建议使用 `5:7` 比例。

## 适合什么场景

这个项目适合以下工作方式：

- 用一份信息母版维护完整事实；
- 用同一套 LaTeX 模板生成不同岗位版本；
- 用 `Codex` 或 `Claude Code` 在项目根目录下直接调度 skill 自动产出岗位定制简历。
