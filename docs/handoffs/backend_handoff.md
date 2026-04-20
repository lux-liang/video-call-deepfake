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

## 非目标

- 不在未更新合同的情况下增删字段。
- 不在 Phase 1 引入复杂队列或持久化系统。
