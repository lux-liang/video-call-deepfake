# Acceptance Checklist

## Phase 1 必须满足

- 存在完整基础目录结构。
- `AGENT.md` 明确项目目标、边界、协同规则、DoD 和 fallback 原则。
- `TASKS.md` 以 P0 / P1 / P2 拆分任务。
- `RUNLOG.md` 包含阶段目标、已完成、进行中、阻塞、决策与下一步建议。
- `docs/architecture.md` 明确 AI 原生定位、分层、Harness 三件套、运行时数据流和失败回退路径。
- `docs/handoffs/backend_frontend_contract.md` 明确 API 路径和稳定字段。
- `docs/handoffs/pipeline_backend_contract.md` 明确 pipeline JSON 输出结构和降级字段。
- backend 最小 FastAPI 服务可启动。
- 存在健康检查接口。
- 存在 sample result 接口。
- frontend 目录和 `README_frontend.md` 存在。
- demo 目录下存在 sample result、sample report 和视频说明。
- README 初稿完整说明定位、架构、能力和限制。
- 至少完成 2 到 4 次清晰 commit。

## 演示验收

- 能说明为什么产品不是聊天网页。
- 能展示 mock/sample 结构化结果。
- 能展示风险分数、事件列表、可疑时间段、工具日志和报告摘要。
- 能说明真实 pipeline 尚未接入但合同已稳定。
- 能说明 fallback 与低置信度标记策略。
