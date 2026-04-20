# Sub Codex Workplan

## Pipeline Codex

- 负责将 `demo/sample_json/sample_result.json` 对齐为可由真实 pipeline 产生的结构。
- 建立 parsing -> event extraction -> scoring 的最小 mock-to-real 入口。
- 输出必须严格遵守 `pipeline_backend_contract.md`。
- 优先实现 schema-valid、可降级、可回放的 JSON 结果，而不是追求模型复杂度。

## Backend Codex

- 负责把当前 FastAPI 骨架扩展为稳定任务服务。
- 落实 `POST /api/upload`、`POST /api/analyze`、任务轮询、结果和报告接口。
- 加入 schema 校验、统一错误结构、fallback 路径和 sample/mock 切换。
- 以 `backend_frontend_contract.md` 为唯一对外字段标准。

## Frontend Codex

- 负责把结果工作流做成可演示界面，而不是聊天框。
- 页面至少包含上传区、任务状态、风险卡片、事件列表、可疑时间段、工具日志和报告摘要。
- 优先围绕稳定字段渲染，不允许私自定义结果字段。
- 先消费 sample result，再切换到真实 backend。

## Docs / QA Codex

- 负责维护 README、架构文档、验收清单、demo 脚本和 PR 说明材料。
- 建立字段命名、术语、截图和 demo 叙事的一致性。
- 负责校验课程要求中的 Harness Engineering 是否被明确写出。
- 负责验收 Phase 1 与后续阶段的 Definition of Done。
