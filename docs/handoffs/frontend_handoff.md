# Frontend Handoff

## 已交付内容

- 已完成 Next.js + TypeScript + Tailwind 的 P0 前端工作流。
- 已实现首页 `/` 与工作台 `/workspace`。
- 已实现 demo/mock 驱动的完整结果展示。
- 已接好面向 backend 合同的前端代理路由。
- 已覆盖 `loading / empty / error / demo / success` 状态。

## 页面结构

### 首页 `/`

- 产品定位说明
- 非聊天式交互边界
- demo 入口
- 工作流概览
- Harness 三件套说明

### 工作台 `/workspace`

- 上传与开始分析区
- demo 样例入口
- 任务进度 / 分析状态
- 参会者风险卡片区
- 事件列表区
- 可疑时间段 / 时间轴区
- 工具调用日志区
- 报告摘要区
- Harness 可视化区

## 数据依赖

前端严格依赖 `backend_frontend_contract.md` 的稳定字段：

- `participants[]`
- `events[]`
- `responses[]`
- `risk_scores[]`
- `suspicious_segments[]`
- `tool_logs[]`
- `report_summary`
- 顶层 `status`
- 顶层 `confidence`

增强展示但非强依赖：

- `validation`
- `fallback`

策略：

- 有 `validation` 时，展示 schema 校验、missing fields、warnings。
- 有 `fallback` 时，展示降级原因、mock 模式、degraded fields。
- 没有这两个字段时，页面仍然可渲染，不会阻塞主流程。

## 已接的 API 路径

前端通过 Next Route Handler 代理到 backend：

- `POST /api/meettruth/upload` -> `/api/upload`
- `POST /api/meettruth/analyze` -> `/api/analyze`
- `GET /api/meettruth/task/[taskId]` -> `/api/task/{task_id}`
- `GET /api/meettruth/result/[taskId]` -> `/api/result/{task_id}`
- `GET /api/meettruth/report/[taskId]` -> `/api/report/{task_id}`
- `GET /api/meettruth/demo-sample` -> `/api/demo/sample-result`

## Demo 路径

推荐录屏入口：

- `http://localhost:3000/`
- `http://localhost:3000/workspace?mode=demo`

推荐讲解点：

1. 页面不是聊天框，而是巡检控制台。
2. Context Management：会议被解析为 `participants / events / responses`。
3. Tool Use：`tool_logs` 显式列出工具执行结果。
4. Feedback Loop：validation、fallback、low-confidence response 会单独展示。
5. 工作台含风险卡片、事件列表、可疑时间段、工具日志、报告摘要。

## 截图建议

建议至少保留以下截图用于 handoff / PR / 演示材料：

1. 首页首屏：突出“不是聊天页”的定位。
2. demo 工作台：任务状态 + 风险卡片首屏。
3. 结果中段：事件列表 + 可疑时间轴。
4. 结果下段：工具日志 + 报告摘要。
5. empty state：证明空结果不会断页面。
6. error state：证明后端失败有显式反馈。

## 非目标

- 不修改 backend 路由设计。
- 不修改合同主文档。
- 不发明未声明字段。
- 不引入聊天式主界面。
