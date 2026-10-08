# Milestone 2: Project Proposal Presentation

> 项目：智能体动态记忆管理（Agent Dynamic Memory Management）
> 团队名：SRE小组　｜　Team ID：第六组　｜　成员：`（待填 5 人）`　｜　日期：2026-10-10
> 主题：Vision and Scope & Feature Roadmap

---

## Slide 1 — 封面

- 项目名：**智能体动态记忆管理**
- 副标题：基于 LoCoMo 的结构化记忆构建与动态状态解析 Web 应用
- 团队名 SRE小组 / Team ID 第六组 / 5 位成员 / 日期

---

## Slide 2 — Vision（愿景）

> 让 AI 智能体在长程、多会话对话中，「记住的是最新事实，而不是被过时记忆误导」。

**一句话愿景**：把「静态向量检索」升级为**可追溯、可解析状态演化**的动态记忆系统——不仅召回相关历史，还能判断哪些记忆已过时、被替代或相互冲突，从而给出正确回答。

---

## Slide 3 — 要解决什么问题（Problem & Motivation）

- **问题**：长程、多轮对话中，用户的状态、计划和偏好会持续变化。普通向量检索虽能召回相关问题历史信息，但会**同时召回「当前状态」和「已被后续信息更新掉的旧状态」**，导致错误回答或错误决策。
- **例子**：`Gina 1月失业于 DoorDash` vs `Gina 3月开了网店`——若直接检索，可能把过时职业状态当作当前事实回答。
- **目标用户与场景**：长程对话 Agent 的开发者与研究者；跨会话「我是谁 / 我计划什么 / 我当前什么状态」类问题（长期用户画像、连续项目跟进、角色扮演长线剧情）。
- **数据基础**：LoCoMo（ACL 2024，Maharana et al.），长期多会话对话基准，含 QA、证据轮次、事件摘要标注。

---

## Slide 4 — 项目范围是什么（Scope）

### In-Scope（必做）
1. **长期对话记忆构建与可视化**
   - 导入 LoCoMo 多会话对话，提取人物、事件、时间、状态，构建结构化 Memory；
   - 每条 Memory 至少保留内容、时间、来源会话/轮次，支持统一 JSON 导出；
   - Web 端查看结构化记忆及其原始证据。
2. **动态记忆更新与有效记忆检索**
   - 给定问题，先检索相关 Memory，再判断其 **RETAIN（保留）/ UPDATE（更新）/ SUPERSEDE（替代）/ CONFLICT（冲突）** 关系；
   - 确定在当前问题与时间条件下仍然有效的 Memory，据此回答；
   - Web 端展示相关历史 Memory 及其关系。

### Bonus（可选扩展）
- 更复杂的冲突消解与多版本保留
- Graph Memory / 多跳关系建模
- Memory 合并与压缩
- 自适应检索或更复杂的时间推理

### Out-of-Scope（明确不做）
- 不训练大模型、不构建通用对话系统、不接入真实生产环境。

---

## Slide 5 — 准备实现哪些功能（功能清单）

| 功能 | 说明 | 优先级 |
|---|---|---|
| 结构化记忆构建 | 从 LoCoMo 对话提取人物/事件/时间/状态，生成结构化 Memory（Memory ID · Content · Entity/Event · Timestamp · Source Session/Turn · State） | 必做 |
| 统一 JSON 导出 | 所有 Memory 导出为统一 JSON 格式 | 必做 |
| Web 记忆可视化 | 查看结构化记忆 + 原始证据（会话/轮次） | 必做 |
| 记忆检索 | 给定问题，从长期历史检索相关 Memory | 必做 |
| 状态关系判定 | 判断 RETAIN / UPDATE / SUPERSEDE / CONFLICT | 必做 |
| 有效记忆解析 + 回答 | 确定当前有效 Memory，据此生成答案 | 必做 |
| Web 状态解析展示 | 展示相关历史 Memory 及其关系、解析过程 | 必做 |
| 冲突消解 / 多版本保留 | 更复杂的冲突消解与多版本保留 | Bonus |
| Graph Memory | 图记忆 / 多跳关系建模 | Bonus |
| 记忆合并压缩 | Memory 合并与压缩 | Bonus |
| 自适应检索 / 时间推理 | 自适应检索或复杂时间推理 | Bonus |

---

## Slide 6 — 系统概述（Pipeline）

```
长对话（多会话）
   ↓ 结构化记忆抽取
Memory（Memory ID · Content · Entity/Event · Timestamp · Source · State）
   ↓ 问题驱动检索
相关候选 Memory
   ↓ 状态关系判定
RETAIN / UPDATE / SUPERSEDE / CONFLICT
   ↓ 有效 Memory 解析
LLM 生成答案 + 证据展示（Web）
```

**技术参考**（可选）：DimMem — 结构化 Memory + 三路检索（BM25 + Dense Embedding + 维度/时间/地点/类型）；MRAgent — Cue–Tag–Content Graph + Agentic 主动重构。对本项目的启发：必做 = 结构化 Memory → Retrieval → RETAIN/UPDATE/SUPERSEDE/CONFLICT → 有效 Memory → QA；Bonus = Graph / 多跳 / 自适应检索。

---

## Slide 7 — Feature Roadmap（版本路线图）

| 版本 | 对应里程碑 | 功能 |
|---|---|---|
| **V1（MVP）** | M3 | 记忆构建 + 基本检索 + JSON 导出 + Web 查看记忆/证据 |
| **V2（核心）** | M4 | 动态状态解析（RETAIN/UPDATE/SUPERSEDE/CONFLICT）+ QA 回答 + Web 展示关系与解析过程 |
| **V3（增强）** | M5 | Bonus（Graph 记忆 / 冲突消解 / 自适应检索）+ 完整对照评测 |

---

## Slide 8 — 数据与评测

**数据来源**
- 从 LoCoMo 官方 10 段长对话中选 6 段：**4 段 dev（开发调试）+ 2 段 test（最终评测）**，其余 4 段作扩展评测。
- 每段平均约 588.2 轮、27.2 个会话、约 1.66 万 Token，含 QA / 证据轮次 / 事件摘要标注。
- 数据与代码：github.com/snap-research/locomo

**评测指标**
- 问题回答 F1
- 证据记忆检索 Recall@K
- 动态状态更新判断准确率

**对照方法（Baseline）**
1. Full Text（全文）
2. Vector RAG（检索相关记忆，但不做状态关系判断）

---

## Slide 9 — 后续如何推进（计划）

**里程碑时间表**

| 里程碑 | 内容 | 占比 | 截止 |
|---|---|---|---|
| M1 | Team Workflow | 15% | 10/10 |
| M2 | Project Proposal Presentation | 5% | 10/10 |
| M3 | Software Requirements Specification | 15% | 10/24 |
| M4 | Mid-term（设计/编码/测试） | 35% | 10/24 |
| M5 | Final Presentation & Final Report | 30% | 11/9 |

**推进方式**
- 每个里程碑至少两轮迭代（初稿 → 评审 → 修订定稿），截止前预留 1–2 天 buffer。
- 阶段一（10/8–10/10）：M1+M2；阶段二（10/11–10/24）：M3+M4；阶段三（10/25–11/9）：M5。

**分工**

| 角色 | 成员 | 职责 |
|---|---|---|
| 组长 / 项目经理 | 王嘉淦（3240102143） | 进度、周会、提交 |
| 需求 / 数据 + 算法 | `（待填）` | 需求、数据、记忆抽取 |
| 后端开发 | `（待填）` | 检索 + 状态判定 + API |
| 前端开发 | `（待填）` | Web 可视化 |
| 测试 / DevOps + 评测 | `（待填）` | 测试、CI、评测 |

**下一步行动**
- 本周：建 `process/` 文件夹与会议纪要模板、选定 4 段 dev + 2 段 test 数据、设计 Memory 字段与 JSON 结构。

---

## Slide 10 — 成功标准 / 风险

**成功标准**
- 可运行 Web 应用 + 完整源代码 + 结构化 Memory JSON + 实验结果与对照分析。
- 三项评测指标（F1 / Recall@K / 状态判定准确率）达到课程要求，并优于 Full Text 基线。

**风险与对策**
- 数据量大（每段 ~588 轮）→ 用 4 段 dev 尽早跑通流水线，再上 test。
- 时间紧 → 每里程碑两轮迭代 + 提前 1–2 天 buffer。
