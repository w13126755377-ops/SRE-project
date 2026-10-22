# 周计划与 Action Items 跟踪

> 对应课程要求：*Make plan for the project, and track weekly action items*。
> 总体时间线见 M1 文档「4. Plan」，本文件用于逐周跟踪 action items 的完成情况。

## 总体里程碑时间线

| 里程碑 | 内容 | 占比 | 截止 |
|---|---|---|---|
| M1 | Team Workflow | 15% | 2026-10-10 |
| M2 | Project Proposal Presentation | 5% | 2026-10-10 |
| M3 | Software Requirements Specification | 15% | 2026-10-24 |
| M4 | Mid-term（设计 / 编码 / 测试） | 35% | 2026-10-24 |
| M5 | Final Presentation & Final Report | 30% | 2026-11-09 |

## 状态图例

`done` 已完成 · `in progress` 进行中 · `blocked` 受阻 · `todo` 待办

---

## Week 1（10/8 – 10/10）：M1 + M2

### 本周目标

完成 M1 Team Workflow 与 M2 Project Proposal 的初稿、评审与定稿提交。

### Action Items 跟踪

| # | 事项 | 负责人 | 截止 | 状态 | 备注 |
|---|---|---|---|---|---|
| 1 | 建立 GitHub 仓库与 process 文件夹 | 王嘉淦 | 10/8 | done | 仓库 https://github.com/w13126755377-ops/SRE-project |
| 2 | M1 文档初稿（Team Workflow） | 王嘉淦 | 10/9 | done | 见 [M1 工作流](../../PROJECT-MILESTONE1-第六组-SRE小组.md) |
| 3 | M2 大纲（Vision & Scope / Feature Roadmap） | 全员 | 10/9 | done | 见 [M2 愿景与范围](../../PROJECT-MILESTONE2-Vision&Scope-第六组-SRE小组.md) |
| 4 | 内部评审（第 2 轮） | 全员 | 10/9 | done | 微信群内评审通过 |
| 5 | 修订定稿、导出 PDF、打 tag、按时提交 | 王嘉淦 | 10/10 | done | 打 tag `v1.0-m1` / `v1.0-m2` |

---

## Week 2（10/11 – 10/17）：M3 + M4 启动

### 本周目标

需求分析与 SRS 初稿；确定数据集与记忆 JSON 结构；启动 M4 编码与前端。

### Action Items 跟踪

| # | 事项 | 负责人 | 截止 | 状态 | 备注 |
|---|---|---|---|---|---|
| 1 | SRS 大纲（FR/NFR/用例/验收） | 李胡诚 | 10/16 | done | 第 2 次例会评审 |
| 2 | 数据集选段与预处理（LoCoMo demo-2conv） | 李胡诚 | 10/15 | done | 38 会话 / 788 轮 / 304 QA |
| 3 | 记忆 JSON 结构设计 | 李胡诚 | 10/15 | done | 字段统一 + schema_version 0.1 |
| 4 | 后端骨架 + 记忆构建 API | 叶泽晨 | 10/17 | done | FastAPI + 导入 / 构建 |
| 5 | 前端骨架 + 页面划分 | 马旻瑄 | 10/17 | done | 记忆 / 溯源 / 关系 / 问答 |
| 6 | 17 场景用例 + pytest 框架 | 陈镇灏 | 10/17 | in progress | 用例初稿完成 |

---

## Week 3（10/18 – 10/24）：M3 定稿 + M4 编码测试

### 本周目标

SRS 定稿 v1.0；M4 六项必做全部实现；功能测试与证据；中期汇报 PPT 定稿提交。

### Action Items 跟踪

| # | 事项 | 负责人 | 截止 | 状态 | 备注 |
|---|---|---|---|---|---|
| 1 | SRS 修订定稿 v1.0、打 tag `v1.0-m3` | 李胡诚 | 10/21 | done | 见 [SRS 评审记录](../reviews/SRS-评审记录.md) |
| 2 | 后端：检索 + 状态判定 + 导出 API | 叶泽晨 | 10/20 | done | RETAIN/UPDATE/SUPERSEDE/CONFLICT |
| 3 | 前端：记忆 / 溯源 / 关系 / 问答页面 | 马旻瑄 | 10/20 | done | tsc + build 通过 |
| 4 | 功能测试：17 场景 + pytest + 截图证据 | 陈镇灏 | 10/21 | done | 15/17 通过 · 35 pytest · 369/369 证据 |
| 5 | 功能测试报告 | 陈镇灏 | 10/21 | done | 见 [M4-功能测试报告](../testing/M4-功能测试报告.md) |
| 6 | 中期汇报 PPT（1-10 页） | 王嘉淦 | 10/22 | done | 第 8/9/10 页按真实数据定稿 |
| 7 | 中期 PPT 定稿、导出 PDF、打 tag `v1.0-m4`、提交 | 王嘉淦 | 10/24 | in progress | 提交前定稿 |

---

## Week 4（10/25 – 10/31）：M5 冲刺（评测 + 召回）

### 本周目标

批量评测落地；向量召回替换 TF-IDF；图记忆与冲突消解。

### Action Items 跟踪

| # | 事项 | 负责人 | 截止 | 状态 |
|---|---|---|---|---|
| 1 | 批量评测脚本（F1 / Recall@K / 状态准确率） | 陈镇灏 | 10/28 | todo |
| 2 | Full Text / Vector RAG 双基线对照实验 | 陈镇灏 | 10/30 | todo |
| 3 | 向量召回（Sentence Transformers）+ 查询扩展验证 | 叶泽晨 | 10/30 | todo |
| 4 | 图记忆多跳关系 + CONFLICT 自动消解设计 | 李胡诚 | 10/28 | todo |
| 5 | Final Report / Final Presentation 框架 | 王嘉淦 | 10/31 | todo |

---

## Week 5（11/1 – 11/9）：M5 定稿

### 本周目标

Final Presentation 与 Final Report 定稿、导出、打 tag、按时提交。

### Action Items 跟踪

| # | 事项 | 负责人 | 截止 | 状态 |
|---|---|---|---|---|
| 1 | Final Report 定稿（含评测结果与消融分析） | 全员 | 11/8 | todo |
| 2 | Final Presentation PPT 定稿 | 王嘉淦 | 11/8 | todo |
| 3 | 打 tag `v1.0-m5`、导出 PDF、按时提交 | 王嘉淦 | 11/9 | todo |
