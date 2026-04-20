# Backend Handoff

## 负责范围

- 实现 FastAPI 路由、任务状态、结果聚合、schema 校验和报告接口。
- 严格遵守 `backend_frontend_contract.md`。

## 当前输入

- Phase 1 已提供稳定 API 路径和字段。
- demo sample result 可作为联调基线。

## 交付要求

- 健康检查、上传、分析、任务查询、结果查询、报告查询路由。
- schema 校验与统一错误返回。
- mock 与 fallback 结果路径保持稳定。

## 当前后端实现状态

- 已实现 `GET /health`，并保留 `GET /healthz` 作为兼容别名。
- 已实现进程内轻量任务状态：`queued -> processing -> completed/degraded`。
- 已实现 `sample/mock/real-placeholder` 三层结构。
- `pipeline_real` 在 Phase 1 中不会崩溃；若结果缺字段或 schema 不合法，会自动回退到 sample/mock fallback。
- `GET /api/result/{task_id}` 在任务未完成时也会返回稳定 JSON，不要求前端猜字段。
- `GET /api/report/{task_id}` 在任务未完成时会返回可渲染的 pending report。

## 给后续对接方的说明

- 前端可以继续使用合同中的稳定字段，不需要额外兼容分支。
- 如需把 `/health` 写回合同主文档，建议在下一次合同更新时把它定义为 canonical path，并保留 `/healthz` 作为 legacy alias。
- 真实 pipeline 接入时，应优先替换 backend service 内部 adapter，不要直接改 route 返回结构。

## 非目标

- 不在未更新合同的情况下增删字段。
- 不在 Phase 1 引入复杂队列或持久化系统。
