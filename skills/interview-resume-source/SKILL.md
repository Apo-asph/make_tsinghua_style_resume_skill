---
name: interview-resume-source
description: Conduct a structured interview to fill, repair, or clarify `resume_master_source.md`, then update the file with verified facts and explicit pending items. Use when Codex needs to ask the user questions in rounds, supplement missing resume facts, or turn free-form answers into a cleaner master resume source.
---

# Interview Resume Source

## 概览

通过分轮采访补全项目中的 `resume_master_source.md`。先定位缺口，再按优先级提问；每轮收到回答后立即更新母版，而不是等全部问题都问完再统一整理。

## 硬约束

- 默认目标文件是项目根目录的 `resume_master_source.md`；只有用户明确指定其他路径时才改到别处。
- 只写用户明确提供、明确确认、或明确纠正过的事实信息；不要补写猜测内容。
- 开始前先读取当前母版，并优先运行：
  `python skills/interview-resume-source/scripts/audit_resume_source.py [path]`
- 每轮问题控制在 `3-6` 个，优先级是：基础信息与定位 > 教育 > 高价值经历 > 论文/荣誉/服务。
- 用户说“不确定”“回头补”“需要查一下”时，不要强行填值；在母版中保留明确的待补项，例如：
  `[待补充：具体 GPA]`
  `[待补充：论文正式状态]`
- 用户明确说“没有”“不适用”“学校不提供”时，直接写清楚，不要继续保留泛化占位符。
- 保持现有模板结构、章节顺序和字段风格，优先填空与局部润色，不重写整份母版。
- 采访得到的项目、实习、论文内容，先整理为可复用事实，再写回母版；避免把原始口语回答原样塞进文件。

## 工作流

### 1. 盘点现状

- 读取 `resume_master_source.md`。
- 运行审计脚本，找出仍是模板占位、默认示例值、或明显待补的条目。
- 如需设计提问顺序，读取 `references/interview-outline.md`。

### 2. 组织采访轮次

- 第一轮优先补：姓名、联系方式、地点意向、核心定位、最高优先级教育信息。
- 如果教育信息已完整，尽快转入“最强经历”采访，而不是在低价值可选字段上停留太久。
- 一次不要倾倒整张问卷。应像短采访一样连续推进，每轮只问当前最影响简历质量的几个问题。

### 3. 每轮回答后立刻回写母版

- 收到回答后，立刻把对应字段写进 `resume_master_source.md`。
- 对经历类内容，优先补齐这些最小要素：
  - 时间
  - 角色
  - 做了什么
  - 用了什么方法 / 系统 / 工具
  - 结果 / 指标 / 影响
- 若指标暂缺但经历很重要，可先写成：
  `[待补充：效率提升比例]`
  `[待补充：服务规模 / 数据规模]`

### 4. 收尾与缺口复盘

- 在用户暂停或核心内容已足够时，再跑一次审计脚本。
- 汇总还缺哪些关键信息，并说明这些缺口会影响哪些后续简历版本。
- 如果母版已经足够支持生成岗位子版，明确说明可以切换到 `make-resume-variant` 工作流。

## 参考资料

- 采访顺序、追问重点与缺口记录方式，读取：
  `references/interview-outline.md`

## 脚本

- `scripts/audit_resume_source.py`：扫描 `resume_master_source.md` 中仍未补全的模板占位与默认示例值，帮助决定下一轮问什么。

## 输出约定

完成一次采访轮次后，至少返回：

- 已更新的母版路径；
- 本轮补上的章节或字段；
- 仍待补充的高优先级信息；
- 建议下一轮继续采访的主题。
