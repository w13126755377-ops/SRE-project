# Milestone 2: Project Proposal Presentation

> 项目：智能体动态记忆管理（Agent Dynamic Memory Management）
> 团队名：SRE小组　｜　Team ID：第六组　｜　成员：`（待填 5 人）`　｜　日期：2026-10-10
> 主题：Vision and Scope & Feature Roadmap

---

## Slide 1 — 封面

- 项目名：**智能体动态记忆管理**
- 副标题：基于 LoCoMo 的结构化记忆构建与动态状态解析 Web 应用
- 团队名 / 5 位成员 / 日期

---

## Slide 2 — Vision（愿景）

> 让 AI 智能体在长程、多会话对话中，「记住的是最新事实，而不是被过时记忆误导」。

**一句话愿景**：把「静态向量检索」升级为**可追溯、可解析状态演化**的动态记忆系统——不仅召回相关历史，还能判断哪些记忆已经过时、被替代或相互冲突，从而给出正确回答。

---

## Slide 3 — Problem & Motivation（问题与动机）

- **问题**：长程、多轮对话中，用户的状态、计划和偏好会持续变化。
- **痛点**：普通向量检索虽能召回相关问题历史信息，但会**同时召回「当前状态」和「已被后续信息更新掉的旧状态」**，导致错误回答或错误决策。
- **例子**：`Gina 1月失业于 DoorDash` vs `Gina 3月开了网店`——若直接检索可能把过时职业状态当作当前事实回答。
- **数据基础**：LoCoMo（ACL 2024，Maharana et al.），长期多会话对话基准，含 QA、证据轮次、事件摘要标注。

---

## Slide 4 — Scope（范围）【重点页】

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

## Slide 5 — 目标用户与场景

- **目标用户**：长程对话 Agent 的开发者与研究者。
- **典型场景**：跨会话「我是谁 / 我计划什么 / 我当前什么状态」类问题（如长期用户画像、连续项目跟进、角色扮演长线剧情）。

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

---

## Slide 7 — Feature Roadmap（功能路线图）【重点页】

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

## Slide 9 — 团队分工

（与 M1 Team Workflow 一致）

| 角色 | 成员（待填） | 职责 |
|---|---|---|
| 组长 / 项目经理 | `（待填）` | 进度、周会、提交 |
| 需求 / 数据 + 算法 | `（待填）` | 需求、数据、记忆抽取 |
| 后端开发 | `（待填）` | 检索 + 状态判定 + API |
| 前端开发 | `（待填）` | Web 可视化 |
| 测试 / DevOps + 评测 | `（待填）` | 测试、CI、评测 |

---

## Slide 10 — 成功标准 / 风险 / 时间表

**成功标准**
- 可运行 Web 应用 + 完整源代码 + 结构化 Memory JSON + 实验结果与对照分析。
- 三项评测指标（F1 / Recall@K / 状态判定准确率）达到课程要求，并优于 Full Text 基线。

**风险与对策**
- 数据量大（每段 ~588 轮）→ 用 4 段 dev 尽早跑通流水线，再上 test。
- 时间紧 → 每里程碑两轮迭代 + 提前 1–2 天 buffer。

**时间表**
- M1+M2：10/10 提交；M3+M4：10/24 提交；M5：11/9 提交。

---

## Slide 11 — 参考方法（可选补充页）

- **DimMem** — Dimensional Structuring for Efficient Long-Term Agent Memory：结构化 Memory + 三路检索（BM25 词法 + Dense Embedding + 维度/时间/地点/类型），显式 Memory 维度直接参与检索。
- **MRAgent** — Memory is Reconstructed, Not Retrieved：Cue–Tag–Content Graph + Agentic 主动重构，中间证据动态决定下一步沿图找什么。
- **对本项目的启发**：必做 = 结构化 Memory → Retrieval → RETAIN/UPDATE/SUPERSEDE/CONFLICT → 有效 Memory → QA；Bonus = Graph / 多跳 / 自适应检索。
