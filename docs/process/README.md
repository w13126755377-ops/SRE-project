# process / 过程管理

> 本目录用于保存项目的过程管理记录，对应课程要求（见 [课程项目说明](../Project-Specification.pdf)）中的
> 「Project Management」与「Version Control」：**会议纪要、仓库工作记录、版本记录**，
> 以及周计划与 action items 跟踪。

## 目录结构

```
docs/process/
├── README.md                         # 本文件：过程管理总说明与索引
├── meeting-minutes/                  # 会议纪要
│   ├── template.md                   # 会议纪要模板
│   ├── 2026-10-08-第1次例会.md        # 第 1 次例会纪要
│   ├── 2026-10-16-第2次例会.md        # 第 2 次例会纪要
│   └── 2026-10-22-第3次例会.md        # 第 3 次例会纪要
├── plans/                            # 周计划与风险跟踪
│   ├── weekly-action-items.md        # 每周计划与行动项跟踪表
│   └── 风险与问题跟踪.md              # 风险登记与遗留问题清单
├── design/                           # 设计文档
│   └── 系统设计文档.md                # M4 系统设计（架构 / 数据模型 / 模块 / API）
├── reviews/                          # SRS / 设计评审记录
│   ├── SRS-评审记录.md                # SRS 评审记录与待确认项
│   └── 设计评审记录.md                # 设计评审记录
├── testing/                          # 功能测试报告与页面截图
│   ├── M4-功能测试报告.md
│   └── screenshots/
├── worklog/                          # 仓库工作记录
│   └── repository-worklog.md         # Git 提交记录与工作日志
└── versions/                         # 版本记录
    └── changelog.md                  # 交付物版本与 tag 变更记录
```

## 各子目录说明

| 目录 | 内容 | 维护人 | 更新时机 |
|---|---|---|---|
| `meeting-minutes/` | 每次例会纪要（含模板） | 轮值记录人 | 会后 24 小时内 |
| `plans/` | 每周计划、action items 与风险跟踪 | 组长 | 每次例会前后 |
| `design/` | 系统设计文档 | 后端 / 架构 | 设计评审后 |
| `reviews/` | SRS / 设计评审记录与待确认项 | 评审人 | 评审会后 |
| `testing/` | 功能测试报告、验收矩阵与页面截图 | 测试 / 前端 | 每轮测试后 |
| `worklog/` | Git 提交记录工作日志 | 组长 / 全员 | 每次提交后 |
| `versions/` | 交付物版本与 tag 记录 | 组长 | 每个里程碑定稿后 |

## 维护规范

- **会议纪要**：记录人轮值，会后 24 小时内按模板提交到 `meeting-minutes/`。
- **周计划 / action items**：每次例会更新 `plans/weekly-action-items.md`，标记完成状态（done / in progress / blocked / todo）。
- **风险跟踪**：例会同步更新 `plans/风险与问题跟踪.md`，及时标记缓解措施与关闭状态。
- **仓库工作记录**：自第一个交付物初稿起持续跟踪 Git 提交（对应课程「Start tracking the progress since the first draft of the first deliverable」）。
- **版本记录**：每个里程碑交付物定稿后在 GitHub 打 tag（如 `v1.0-m1`），并同步更新 `versions/changelog.md`。

## 会议纪要索引

| 会议 | 日期 | 主要议题 |
|---|---|---|
| [第 1 次例会](meeting-minutes/2026-10-08-第1次例会.md) | 2026-10-08 | 项目总览、角色分工、里程碑计划 |
| [第 2 次例会](meeting-minutes/2026-10-16-第2次例会.md) | 2026-10-16 | M1/M2 复盘、SRS 评审、数据结构设计、M4 启动 |
| [第 3 次例会](meeting-minutes/2026-10-22-第3次例会.md) | 2026-10-22 | M4 测试结果确认、中期 PPT 定稿、M5 计划 |
