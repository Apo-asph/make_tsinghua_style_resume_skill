---
name: make-resume-variant
description: Tailor a target-specific LaTeX resume variant in this project from `resume_master_source.md`, `profile_photo.png` or `profile_photo.jpg`, and `latex template/resume_tsinghua_purple.tex`, then compile the PDF, review layout, and refine after user approval. Use when Codex needs to create, update, or inspect a Chinese resume variant for research, R&D, algorithm, AI for Science, or high-potential applications.
---

# Make Resume Variant

## 概览

制作当前项目中的岗位定制简历子版。先锁定投递目标与不确定信息，再从母版筛选内容、复制 LaTeX 模板到根目录子版文件夹、编译 PDF、审查版式，并在用户确认后继续微调排版。交付时默认同时保留子版目录中的工作 PDF，并复制一份成品 PDF 到项目根目录。

## 硬约束

- 默认信息母版文件统一使用 `resume_master_source.md`；照片文件的基础文件名统一使用 `profile_photo`，支持 `profile_photo.png` 与 `profile_photo.jpg`。共享仓库中可直接替换为用户自己的已核验材料，除非用户明确提供更新材料。
- 仅将 `latex template/resume_tsinghua_purple.tex` 视为模板源文件。
- 如目标公司、岗位、内容取舍、时间线表述、论文状态或投递重点存在不确定项，先提问再起草。
- 保持小改动；未经确认，不新增依赖。
- 完成工作前运行相关验证：对 skill 本身跑校验，对简历子版至少完成编译与 PDF 审查。
- 默认以一页为硬目标，并尽量让内容自然占满这一页；通常不能明显填不满一页。
- “占满一页”不只看页数；还要看正文区在视觉上基本铺满页面，上下留白尽量接近，不能出现明显的上紧下空、上空下挤或底部留白远大于顶部留白。
- 当版面偏空时，先按相关性由强到弱补充信息，再考虑样式层面的放大或拉开。
- 只有当用户明确要求忽略一页限制、接受详尽版或允许多页时，才可以超过一页。
- 默认自动清理临时文件；除非用户明确要求保留排障产物，否则不要把日志、预览图或中间文件留在项目里。
- 将编译产物保留在子版文件夹中；进入交付阶段时，默认将当前成品 PDF 复制一份到项目根目录，命名为 `<target-slug>-resume.pdf`。

## 工作流

### 1. 锁定投递目标

- 先确认目标公司、目标岗位、以及需要强调的叙事重点。
- 如果用户的请求不够具体，停下来补问，不要直接猜测。
- 如果岗位可归入常见类型，读取 `references/content-selection.md` 并使用最接近的筛选策略。

### 2. 创建子版目录

- 在项目根目录创建 `<target-slug>/`。
- 将 `latex template/resume_tsinghua_purple.tex` 复制到该目录，并重命名为 `<target-slug>.tex`。
- 不要复制 `latex template` 中的 `.aux`、`.log`、`.out`、`.fls`、`.fdb_latexmk`、`missfont.log`、`synctex` 等编译产物。
- 若根目录存在 `profile_photo.png`，复制到子版目录并保持文件名 `profile_photo.png`；否则若存在 `profile_photo.jpg`，复制到子版目录并保持文件名 `profile_photo.jpg`。
- 复制完照片后，优先运行 `python skills/make-resume-variant/scripts/prepare_photo.py <variant-photo-path>` 检查照片比例。
- 共享模板会自动等比适配照片；常见纵向或方形比例只要落在大致 `2:3` 到 `1:1` 的范围内，通常无需手动裁剪。
- 如果脚本提示照片比例过高或过宽，先向用户说明情况；只有在用户同意后，才对“子版目录中的照片副本”执行居中裁取：
  `python skills/make-resume-variant/scripts/prepare_photo.py <variant-photo-path> --crop-center`
- 不要直接修改项目根目录中的原始照片，除非用户明确要求。

### 3. 定制内容

- 只从 `resume_master_source.md` 中取材，不编造事实。
- 为目标岗位选择最强的教育、项目、技能、论文、荣誉与服务信息。
- 默认推荐模块为：教育背景、项目经历、实习经历、核心技能与成果；可根据岗位要求与材料强弱做个性化调整，例如替换或增补论文、荣誉、课程、校园服务等模块。
- 默认以一页简历为目标；只有用户明确要求忽略一页限制时，才切换到可超过一页的模式。
- 默认追求“内容尽量自然占满一页，不多不少”，不要为了省事留下大块空白，也不要为了硬塞信息溢出到第二页。判断是否“占满”时，要同时看页数、正文块高度、以及页面顶部与底部留白是否大致均衡。
- 如果版面不满，按相关性由强到弱补充信息，优先顺序通常为：
  1. 与目标岗位最贴近的补充 bullet、量化结果与代表成果；
  2. 强相关项目、论文、课程、技能或工具细节；
  3. 能增强叙事完整性的次强相关荣誉、会议、组织经历。
- 只有当强相关与次强相关信息都已合理用上、页面仍明显偏空时，才考虑适度增大字号、放松行距或加大模块间距，让版面更自然地铺满一页。
- 优先删除弱相关或重复内容，而不是机械压缩所有模块。
- 严格遵守母版中的外发规则：
  - 不得使用 “TOP5%”。
  - 身份证号仅保留内部使用。
  - 外发前复核 `under review` 论文的最新状态。
- 保持措辞具体、可核验、与岗位强相关。

### 4. 编译

- 优先使用 `python skills/make-resume-variant/scripts/compile_resume.py <target-slug>` 或 `python skills/make-resume-variant/scripts/compile_resume.py <absolute-variant-dir>`。
- 若当前环境支持 Bash，可继续使用同名 `.sh` 包装脚本。
- 通过 `latexmk -xelatex` 编译，因为模板依赖 `ctex` 与系统字体。
- 编译成功后，默认自动清理该子版目录中的 LaTeX 中间产物，仅保留 `.tex`、`.pdf`、`profile_photo.*` 与用户明确要求保留的资产。
- 如果编译失败，先修复 LaTeX 问题，再进入版式审查。

### 5. 先审查 PDF，再改排版

- 优先使用 `python skills/make-resume-variant/scripts/inspect_resume_pdf.py <pdf-path>` 渲染预览图并报告页数。
- 若当前环境支持 Bash，可继续使用同名 `.sh` 包装脚本。
- 若未显式指定预览目录，预览图默认生成在 `/tmp`，不应写回项目目录。
- 若显式指定了项目内预览目录，则该目录视为临时目录，必须在最终交付前清理。
- 读取 `references/pdf-review-checklist.md`，据此审查编译结果。
- 先判断当前是否处于“默认一页模式”还是“显式忽略一页限制模式”；除非用户已明确授权，否则一律按默认一页模式审查。
- 若出现以下问题，先汇报，再等待用户是否批准继续微调：
  - 页数超过目标；
  - 虽然只有一页，但正文整体偏短，未自然铺满页面；
  - 页面上下留白明显失衡，例如底部留白显著大于顶部留白；
  - 联系方式行或节标题换行；
  - 明显的大块留白或局部过挤；
  - 孤行、寡行；
  - 文本、链接或项目符号溢出；
  - 证件照位置生硬或与页眉不齐。
- 如果 PDF 已达可投递状态，明确说明并进入备份或交付阶段。

### 6. 经用户确认后再微调版式

- 获得用户批准后，按以下顺序修正版式问题：
  1. 如果超页，先删除较弱内容，再切换到更紧凑的模块密度档位，并收紧措辞与断行；
  2. 如果未满页，先继续补充相关信息，按照“强相关 -> 次强相关 -> 叙事补强信息”的顺序填充；
  3. 只有当所有合理信息都已用上且仍未满页时，再适度增大字号、放松行距或拉开模块间距，并优先把上下留白调到更接近；
  4. 仅在仍然需要时再调模板中的全局间距常量。
- 除非用户明确要求，不做大规模视觉重设计。

## 例外窗口

- 若用户明确提出“忽略一页限制”“做详细版”“允许超过一页”“做学术长版/完整版”，可切换到多页模式。
- 进入多页模式后，可以超过一页，但仍要保持每一页尤其最后一页的版面自然，不要出现明显空页或稀疏尾页。
- 若用户没有明确这样说，就不要自行放宽一页限制。

## 临时文件处理

- 优先使用 `python skills/make-resume-variant/scripts/cleanup_temp_files.py [path ...]`；若当前环境支持 Bash，也可使用同名 `.sh` 包装脚本。若脚本不存在，也必须用等效方式完成递归清理，不能因为缺少脚本而跳过清理。
- 临时文件默认包括：`*.aux`、`*.log`、`*.out`、`*.fls`、`*.fdb_latexmk`、`*.xdv`、`*.synctex*`、`missfont.log`、`.DS_Store`、审查预览目录或产物（如 `preview`、`preview_v2`、`*-preview-*`、`*_preview-*`、`*preview*.png`、`*preview*.pdf`）以及 OCR 暂存目录（如 `.ocr-tmp`）。
- 永远不要把 `latex template` 里的临时文件复制进子版目录。
- 在开始前可先做一次基线清理；PDF 审查结束且用户接受版面后，在最终回复前必须再次清理，确保项目目录中不残留日志、预览图、预览 PDF 或其他中间产物。
- 如果编译失败，可短暂保留日志用于定位问题；问题说明完成后应立即清理，除非用户明确要求保留这些诊断文件。

### 7. 收尾

- 将工作 PDF 保留在子版目录中。
- 将最终接受版或当前确认可投递的成品 PDF 复制到项目根目录，命名为 `<target-slug>-resume.pdf`。
- 在最终回复前完成临时文件清理。
- 汇总说明：保留了什么、删掉了什么、还有哪些待确认项、以及是否仍有版式风险。

## 参考资料

- 需要判断不同岗位该保留什么时，读取 `references/content-selection.md`。
- 需要审查 PDF 版式时，读取 `references/pdf-review-checklist.md`。

## 脚本

- `scripts/cleanup_temp_files.py`：递归清理项目或指定目录中的临时文件，兼容 `macOS` 与 `Windows`。
- `scripts/compile_resume.py`：稳定编译某个子版目录，并输出生成的 PDF 路径。
- `scripts/inspect_resume_pdf.py`：使用 Ghostscript 渲染 PDF 预览图并报告页数，供人工审查。
- `scripts/prepare_photo.py`：检测照片比例，并在用户批准后对超出推荐范围的照片做居中裁取。
- 同名 `.sh` 文件仅作为 `macOS` / `Linux` 包装层保留。

## 输出约定

在真实执行一次子版生成任务后，至少返回：

- 投递目标与本次强调重点；
- 子版目录路径；
- `.tex` 文件路径；
- 编译得到的 PDF 路径；
- 根目录备份 PDF 路径（如已创建）；
- 一段简短的 PDF 审查结论；
- 所有仍需用户拍板的问题。
