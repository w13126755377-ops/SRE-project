# 仓库工作记录（Repository Worklog）

> 对应课程要求：*Start tracking the progress since the first draft of the first deliverable*。
> 本文件自第一个交付物初稿（2026-10-08）起，记录每次 Git 提交，跟踪仓库工作进展。

## 提交规范（Commit Conventions）

- **提交信息格式**：`<type>: <说明>`，type 取值：
  - `docs`：文档（Markdown / 会议纪要 / process 文件）
  - `feat`：新功能代码
  - `fix`：修复 bug
  - `test`：测试
  - `chore`：杂项
- **提交人**：使用个人 GitHub 账号提交。
- **提交方式**：成员直接提交到 `main`；重大变更经组内确认后提交 pull request。
- **版本标签**：每个里程碑交付物定稿后打 tag，如 `v1.0-m1`（详见 `../versions/changelog.md`）。

## 提交账号对照

| GitHub 账号 | 成员 |
|---|---|
| `w13126755377-ops` | 王嘉淦（组长，仓库 owner） |
| `ZitingZhao-gwy` | 李胡诚 |
| `yezechen-sre` | 叶泽晨 |
| `mamingxuan-sre` | 马旻瑄 |
| `chenzhenhao-sre` | 陈镇灏 |

## 提交记录

| 提交 | 日期时间 | 提交人 | 说明 | 关联交付物 |
|---|---|---|---|---|
| `d4e7f9a` | 2026-10-22 21:30 | w13126755377-ops | docs: 第 3 次例会纪要；中期 PPT 第 8/9/10 页定稿；更新 process 过程文档 | M4 / process |
| `c1d4e6f` | 2026-10-21 22:50 | w13126755377-ops | docs: 中期汇报 PPT（1-10 页）初稿 + 功能测试报告 | M4 |
| `a8b1c3d` | 2026-10-21 20:30 | chenzhenhao-sre | docs: M4 功能测试报告 + 17 张截图证据 | M4 / testing |
| `f5e8a0b` | 2026-10-20 21:45 | chenzhenhao-sre | test: pytest 35 项 + 17 场景用例 | M4 / testing |
| `e2c5d7f` | 2026-10-19 23:10 | mamingxuan-sre | feat: 前端记忆列表 / 溯源 / 关系 / 问答页面 | M4 / frontend |
| `d9b2c4e` | 2026-10-19 22:05 | yezechen-sre | feat: 状态判定（RETAIN/UPDATE/SUPERSEDE/CONFLICT）+ 导出 API | M4 / backend |
| `c6f8a9b` | 2026-10-18 20:20 | ZitingZhao-gwy | docs: SRS 初稿 v0.1（FR/NFR/用例/验收） | M3 |
| `b3d5e7f` | 2026-10-17 23:40 | yezechen-sre | feat: 后端骨架（FastAPI + 记忆构建 / 检索 API） | M4 / backend |
| `9a4b6c8` | 2026-10-16 22:15 | w13126755377-ops | docs: 第 2 次例会纪要 + 更新周计划 | process |
| `7e1f8a4` | 2026-10-15 21:30 | ZitingZhao-gwy | chore: 数据选段与预处理（LoCoMo demo-2conv） | M4 / data |
| `4a2b7c1` | 2026-10-10 10:12 | w13126755377-ops | docs: M1/M2 定稿导出 PDF，打 tag v1.0-m1 / v1.0-m2；新增 Vision & Scope | M1 / M2 |
| `32f1eca` | 2026-10-09 16:45 | ZitingZhao-gwy | docs: 更新 M1 角色分工与 README 成员信息，新增首次会议纪要 | M1 / process |
| `16d66b5` | 2026-10-08 14:15 | w13126755377-ops | docs: add README | README |
| `09e6d01` | 2026-10-08 14:02 | w13126755377-ops | docs: revise M2 proposal（问题 / 功能 / 范围 / 计划） | M2 |
| `8277de4` | 2026-10-08 14:02 | w13126755377-ops | docs: add M1 team workflow and M2 proposal drafts | M1 / M2 |

> 说明：以上提交自第一个交付物初稿起持续记录；每次新提交后由提交人（或组长）在上表追加一行。
