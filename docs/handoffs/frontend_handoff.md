# Frontend Handoff

## 负责范围

- 消费 backend 稳定字段，完成演示页面与结果面板。
- 页面重点是风险卡片、事件列表、可疑时间段、工具日志、报告摘要。

## 当前输入

- 依赖 `backend_frontend_contract.md` 的稳定字段。
- 可用 `GET /api/demo/sample-result` 作为联调数据源。

## 交付要求

- 不将产品设计成聊天网页。
- 优先实现 workflow 面板：上传、任务状态、结果视图、日志视图。
- 显示 `status`、`confidence` 和 degraded 提示。
- 页面首屏必须能一眼看出这是风险巡检 workspace，而不是普通聊天页面。
- 至少要有 participant 风险卡片、suspicious segment、event 列表、tool logs、report summary 五个信息区块。
- `validation` 与 `fallback` 至少要有明显的状态提示位，不要藏在浏览器控制台。

## 录屏与截图建议

- 首页或 workspace 首屏：展示上传区、任务状态和风险概览。
- 结果页截图一：participant 风险卡片 + suspicious segment。
- 结果页截图二：tool logs + report summary。
- 录屏时优先从整体工作流切入，不要把镜头停在纯样式调试或聊天组件上。

## 非目标

- 不自行发明接口字段。
- 不以复杂视觉效果替代结果可读性。
