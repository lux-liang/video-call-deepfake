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

## 非目标

- 不自行发明接口字段。
- 不以复杂视觉效果替代结果可读性。
