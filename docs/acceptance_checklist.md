# Acceptance Checklist

状态说明：

- `PASS`: 当前仓库已经满足，可直接验收
- `PENDING`: 已写入文档或合同，但相关分支实现仍待补位
- `FAIL`: 当前仓库缺失，提交前必须修复

## 课程要求总检查

| 验收项 | 如何检查 | 通过标准 | 当前状态 |
| --- | --- | --- | --- |
| 痛点定义清楚 | 打开 `README.md` 前半部分 | 能在 30 秒内说明用户痛点、输入、输出 | PASS |
| 明确是 AI 原生产品 | 打开 `README.md` 与 `docs/architecture.md` | 明确写出 workflow、结构化上下文、工具链与验证 | PASS |
| 明确不是普通聊天网页 | 打开 `README.md` 与 `docs/demo_script.md` | 明确写出 chat 不是主交互，主路径是任务工作流 | PASS |
| Context Management / Agent Skill | 检查 README Harness 小节 | 明确写出 `participants`、`events`、`responses`、`suspicious_segments`、`tool_logs` | PASS |
| Tool Use / MCP / External Tools | 检查架构文档与 sample JSON | 明确写出 `ffmpeg`、`opencv`、`mediapipe`、`vad`、rules、reporting，并有 `tool_logs` | PASS |
| Feedback Loop / Verification | 检查架构文档、sample JSON、合同 | 明确出现 `confidence`、`validation`、`fallback`、degraded 策略 | PASS |
| 3 分钟 demo 路径 | 打开 `docs/demo_script.md` | 有时间切分、讲稿提示、录屏顺序、fallback 路径 | PASS |
| GitHub 代码仓库交付 | 检查 README 的“GitHub 交付物” | 明确列出提交仓库需要包含的核心内容 | PASS |
| UI 有产品感，不粗糙 | 检查前端页面或前端 handoff | 当前至少应有明确 UI 目标；最终提交前需要真实页面截图或录屏 | PENDING |

## 文档与仓库包装

| 验收项 | 如何检查 | 通过标准 | 当前状态 |
| --- | --- | --- | --- |
| `AGENT.md` 完整 | 打开文件 | 包含目标、边界、协同规则、DoD、fallback 原则 | PASS |
| `TASKS.md` 完整 | 打开文件 | 至少按 `P0 / P1 / P2` 拆分 | PASS |
| `RUNLOG.md` 完整 | 打开文件 | 包含阶段目标、完成项、阻塞、决策和验收巡检记录 | PASS |
| README 对外可读 | 用非项目成员视角通读 README | 不依赖口头解释也能理解项目定位、限制和演示路径 | PASS |
| 关键 docs 齐全 | 检查 `docs/` | 至少包含 architecture、acceptance、demo_script、handoffs | PASS |
| Git 历史清晰 | `git log --oneline` | commit 语义清楚，不是杂乱临时提交 | PASS |

## Harness 与合同验收

| 验收项 | 如何检查 | 通过标准 | 当前状态 |
| --- | --- | --- | --- |
| Backend / Frontend 合同稳定 | 检查 `docs/handoffs/backend_frontend_contract.md` | API 路径、状态字段、稳定结果字段都被列清楚 | PASS |
| Pipeline / Backend 合同稳定 | 检查 `docs/handoffs/pipeline_backend_contract.md` | 顶层 schema、降级字段、validation 规则都存在 | PASS |
| Sample JSON 与合同一致 | 对比 `demo/sample_json/sample_result.json` 与 handoff | `participants`、`events`、`responses`、`risk_scores`、`suspicious_segments`、`tool_logs`、`report_summary`、`validation`、`fallback` 不漂移 | PASS |
| 低置信度与降级被显式保留 | 检查 sample JSON | `confidence` 必须存在，`fallback.reason` 必须可读 | PASS |
| 术语统一 | 搜索 README、docs、sample JSON | 使用 `participant / event / response / suspicious segment / tool logs / report summary` | PASS |

## API 与样例验收

| 验收项 | 如何检查 | 通过标准 | 当前状态 |
| --- | --- | --- | --- |
| Backend 可启动 | 在 `backend/` 执行 `uvicorn app.main:app --reload` | 服务正常启动，无导入错误 | PASS |
| 健康检查存在 | 访问 `GET /healthz` | 返回服务在线信息 | PASS |
| Sample result 接口存在 | 访问 `GET /api/demo/sample-result` | 返回 sample 结构化 JSON | PASS |
| 任务状态接口存在 | 访问 `GET /api/task/task_demo_001` | 至少返回 `status`、`progress`、`stage`、`confidence` | PASS |
| 报告接口存在 | 访问 `GET /api/report/task_demo_001` | 返回 Markdown 报告字符串与 `generated_at` | PASS |
| Sample 报告可读 | 打开 `demo/sample_outputs/sample_report.md` | 能和 `report_summary` 对上主结论 | PASS |
| Sample 视频说明存在 | 打开 `demo/sample_videos/README.md` | 明确当前无真实视频样本，演示依赖 sample 文件 | PASS |

## Demo 与录屏验收

| 验收项 | 如何检查 | 通过标准 | 当前状态 |
| --- | --- | --- | --- |
| demo 路径可直录 | 按 `docs/demo_script.md` 逐步操作 | 不需要临场发明讲法，不会在录屏中卡住 | PASS |
| 结构化结果可讲清 | 打开 sample result | 能现场指出 participant、event、response、suspicious segment、tool logs | PASS |
| mock / fallback 可讲清 | 打开 sample result 的 `responses` 与 `fallback` | 能明确说出当前结果来自 sample/mock，不冒充真实能力 | PASS |
| 验证闭环可讲清 | 打开 `validation` 与 acceptance checklist | 能说明 schema 校验、字段完整性检查和 degraded 策略 | PASS |
| 前端演示有替代方案 | 检查 `docs/demo_script.md` | 当前 UI 未完成时，有 backend + docs 的 fallback demo 路径 | PASS |

## UI 产品感验收

这一部分当前是跨分支待补位项。文档已经写清方向，但最终课程提交前必须由 `feat/frontend` 实际落地。

| 验收项 | 如何检查 | 通过标准 | 当前状态 |
| --- | --- | --- | --- |
| 主界面不是聊天框 | 查看前端首页 / workspace | 以上传、任务状态、结果面板为主，而不是对话气泡 | PENDING |
| 结果页有产品感 | 查看页面截图或录屏 | 至少包含 participant 卡片、suspicious segment、event 列表、tool logs、report summary，并有清晰层级 | PENDING |
| 风险信息一眼可读 | 查看页面截图或录屏 | `status`、`confidence`、高风险 participant 能在首屏被识别 | PENDING |
| 日志和报告不是藏在控制台 | 查看页面截图或录屏 | tool logs 与 report summary 在 UI 中可见 | PENDING |

## 待补位说明

- `feat/frontend`: 需要把 handoff 中定义的 inspection workspace 实际做出来，提供录屏截图位。
- `feat/pipeline`: 需要把 mock-to-real pipeline entry 与 `validation` / `fallback` 的真实生成逻辑接上。
- `demo/sample_videos/`: 最终若课程需要更完整演示，建议补一个短会议回放片段。
