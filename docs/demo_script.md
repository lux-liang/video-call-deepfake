# Demo Script

## 目标

用最小样例展示 MeetTruth Agent 的 Phase 1 闭环：视频输入占位、结构化分析结果、风险解释和日志面板合同。

## Demo 路径

1. 打开 README，说明产品定位是“视频输入 -> 结构化分析 -> 风险评分 -> 解释报告”。
2. 展示 `docs/architecture.md`，说明为何系统是 AI 原生 workflow，而不是聊天 UI。
3. 启动 backend 服务。
4. 访问 `GET /healthz`，确认服务在线。
5. 访问 `GET /api/demo/sample-result`，展示 sample 结构化结果。
6. 启动 frontend 服务，打开首页 `/`，说明这是“会议真实性巡检控制台”，不是聊天框。
7. 进入 `/workspace?mode=demo`，展示任务进度推进到结果页。
8. 展示风险卡片、事件列表、可疑时间段、工具日志、报告摘要。
9. 指出 Harness 可视化区域，说明：
   - Context Management：会议被解析成 `participants / events / responses`
   - Tool Use：页面显式展示 `tool_logs`
   - Feedback Loop：页面显式展示 validation、fallback、低置信 response
10. 切换到 empty state 和 error state，说明 fallback 与失败反馈不会让 demo 断链。
11. 展示 `demo/sample_outputs/sample_report.md`，说明报告形态。
12. 展示 handoff 合同，说明后续 backend / pipeline / frontend 将围绕稳定字段协作。

## Demo 讲解重点

- 输入是会议回放视频，不是文本 prompt。
- 中间层是结构化上下文，不是把原视频直接喂给 LLM。
- 工具链依赖是显式的：`ffmpeg`、`opencv`、`mediapipe`、`vad`、rules、reporting。
- 当前结果可用 mock/sample 跑通，但字段和状态语义已经稳定。
- 所有复杂模块都允许 fallback，避免演示断链。
