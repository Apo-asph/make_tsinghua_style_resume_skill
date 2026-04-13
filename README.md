# make_tsinghua_style_resume_skill

一个面向中文求职场景的 LaTeX 简历项目，包含：

- 一套清华紫色调、简约风的简历模板；
- 一个用于维护完整事实信息的信息母版；
- 一个供 `Codex` 识别的本地 skill，用自然语言生成、编译、审查和微调岗位定制简历；
- 一个可分发的 release 打包形态。

## 当前状态

当前版本：`v0.1.0`

这是首个公开版本。

`v0.1.0` 范围：

- 提供 `resume_tsinghua_purple.tex` LaTeX 模板；
- 提供 `resume_master_source.md` 信息母版模板；
- 提供 `profile_photo.png` 照片占位文件；
- 提供适用于 `Codex + macOS` 的本地 skill 与脚本工作流。

当前已知范围限制：

- agent 工作流按 `Codex` 设计；
- 脚本与默认字体配置按 `macOS` 环境设计与验证；
- 原生 `Windows` 环境下暂不保证开箱即用。

## 后续计划

计划中的后续版本包括：

- 增加面向 `Claude Code` 的适配与使用说明；
- 增加原生 `Windows` 环境支持，减少对 `.sh` 脚本与 macOS 字体/路径假设的依赖；
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
- `skills/make-resume-variant/`
  `Codex` 使用的本地 skill、脚本与参考资料。
- `AGENTS.md`
  agent 在项目根目录下工作的规则说明。
- `make_tsinghua_style_resume_skill-release-codex-macos-v0.1.0.zip`
  当前 `v0.1.0` release 包。

## 命名约定

项目默认采用以下命名：

- 信息母版文件：`resume_master_source.md`
- 照片文件：`profile_photo.png`
- 模板文件：`latex template/resume_tsinghua_purple.tex`

建议手动模式和 agent 模式都保持这些文件名不变，以减少额外配置。

注意：

- 这两个文件名是工作流中的显式依赖文件名，用户不应自行更改：
  `resume_master_source.md`
  `profile_photo.png`

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
- 模板默认字体为 `Avenir Next` 与 `Hiragino Sans GB`。这套配置更偏向 `macOS`；如果不在 `macOS` 上，通常需要先修改字体设置再编译。
- 手动模式下，模板支持的照片格式为：
  `profile_photo.png`
  `profile_photo.jpg`
- 若目录中没有 `profile_photo.png` / `profile_photo.jpg`，模板会显示占位框，不会因缺照片而直接编译失败。

### 2. 使用 Codex + Skill

如果你希望通过自然语言自动制作简历：

1. 将 release 包内容拷贝到一个空文件夹。
2. 先用自己的真实信息替换：
   `resume_master_source.md`
   `profile_photo.png`
3. 以该文件夹为根目录启动 `Codex`。
4. `Codex` 识别到 `AGENTS.md` 和 `skills/make-resume-variant/` 后，即可按自然语言指令工作。

示例指令：

- “请为 xx 公司的算法工程师岗位生成一页版简历。”
- “请根据 `resume_master_source.md` 生成一版 AI for Science 方向简历，并编译检查版式。”
- “请把当前版本压缩到一页，并保留科研与 Agent 相关项目。”

## release / Codex 模式环境要求

当前 release 为 `Codex + macOS` 的 `v0.1.0` 版本，脚本按 macOS 环境设计与验证。

若要完整使用 skill 的自动编译、审查和清理能力，建议环境中至少具备：

- `macOS`
- `bash`
- `xelatex`
- `latexmk`
- `ctex`
- `ghostscript`
- `find`
- `mktemp`
- `mkdir`
- `rm`
- `wc`
- `tr`

脚本层面的具体假设：

- `skills/make-resume-variant/scripts/compile_resume.sh`
  依赖 `latexmk`、`xelatex`，并显式使用 `/Library/TeX/texbin`。
- `skills/make-resume-variant/scripts/inspect_resume_pdf.sh`
  依赖 `gs`，并显式把 `/opt/homebrew/bin` 加入 `PATH`。
- `skills/make-resume-variant/scripts/cleanup_temp_files.sh`
  依赖 `bash`、`find`、`rm` 等 Unix 命令。

因此：

- 当前 release 推荐在 `macOS` 下使用；
- 原生 `Windows` 的 `CMD` / `PowerShell` 不能直接运行这些 `.sh` 脚本；
- 若在 `Windows` 上使用，通常需要 `WSL` 或其他兼容 shell 环境，并自行处理字体、路径与依赖问题。

## 开始前必须替换的文件

按使用方式区分：

- 手动模式：
  不要求先替换 `resume_master_source.md`；你只需要直接修改 `resume_tsinghua_purple.tex` 的内容，并准备好同目录下的真实照片文件。
- `Codex` / release 模式：
  开始前应先替换以下两个文件，并保持文件名不变：
  `resume_master_source.md`
  `profile_photo.png`

其中：

- `resume_master_source.md` 应填写你的真实教育、项目、论文、技能、荣誉等信息；
- `profile_photo.png` 应替换为你的真实照片，建议使用 `5:7` 比例。

## 适合什么场景

这个项目适合以下工作方式：

- 用一份信息母版维护完整事实；
- 用同一套 LaTeX 模板生成不同岗位版本；
- 用 `Codex` 在项目根目录下直接调度 skill 自动产出岗位定制简历。
