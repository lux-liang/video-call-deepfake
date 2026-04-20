# Architecture

## 为什么这是 AI 原生产品，不是普通聊天网页

MeetTruth Agent 的核心不是对话，而是工作流。系统输入是会议视频，输出是结构化风险分析。用户需要的是参会者真实性巡检、可疑时间段、事件证据、报告和日志，而不是一个开放式聊天窗口。LLM 只在解释、报告和结构化摘要环节中扮演受约束的组件，而不是产品本体。

## 为什么当前输入选择会议回放驱动的准实时分析

- 会议回放更适合第一阶段演示和合同固化。
- 回放模式可以稳定复现结果，便于调试、验收和 demo 录制。
- 回放驱动仍可模拟准实时分段处理，为后续实时流扩展保留兼容路径。
- 直接从实时流开始会引入高复杂度状态管理、延迟控制和容错问题，不符合 Phase 1 边界。

## 系统分层

1. `ingestion`
   - 接收会议视频、元数据和任务请求。
   - 生成 `task_id`、`meeting_id` 和原始输入引用。
2. `parsing`
   - 调用 `ffmpeg` 拆分视频/音频、抽帧、切片、对齐时间戳。
3. `event extraction`
   - 基于 OpenCV、MediaPipe、VAD、规则引擎或后续模型，提取人脸、音画不同步、说话轮次、遮挡、异常切换等事件。
4. `behavior features`
   - 将原始事件归并为 participant 级与 segment 级行为特征。
5. `scoring`
   - 生成 participant 风险分数、会议整体置信度、可疑片段列表。
6. `explanation`
   - 使用结构化上下文生成受约束的解释和 evidence summary。
7. `reporting`
   - 输出 JSON 结果、报告摘要、sample markdown 报告和 Harness 日志。

## Harness 三件套

### 1. Context Management / Agent Skill

- 不把整段原始会议视频直接丢给 LLM。
- 先把会议表示为 `participants`、`events`、`responses`、`risk_scores`、`suspicious_segments`、`tool_logs` 等结构化上下文。
- LLM 或代理只消费压缩后的上下文、工具输出与验证后的摘要。

### 2. Tool Use / MCP / External Tools

- 系统依赖 `ffmpeg`、`opencv`、`mediapipe`、`vad`、规则引擎、报告工具等外部工具链。
- 后续可通过 MCP 或 service adapter 统一封装工具调用和日志采集。
- `tool_logs` 是稳定结果字段，而不是调试附属物。

### 3. Feedback Loop / Verification

- pipeline 输出先经过 schema 校验与字段完整性检查。
- 低置信度结果必须显式标记 `confidence` 和 degraded reason。
- 当真实工具链失败时，系统必须可以退回 mock/sample/fallback 输出，保证 demo 闭环不断裂。
- 所有关键阶段都保留状态、错误信息和验证结果，便于回放与复核。

## 统一术语与字段边界

为避免 backend / pipeline / frontend / docs 四个分支各自发明名词，以下术语固定：

- `participant`: 参会者实体
- `event`: 结构化异常事件
- `response`: agent 或规则层输出的结构化解释
- `suspicious_segments`: 需要重点复核的时间段集合
- `tool_logs`: 外部工具执行记录
- `report_summary`: 面向 UI 和导出报告的摘要对象
- `validation`: schema 校验和字段完整性检查结果
- `fallback`: 当前输出是否来自 mock、sample 或 degraded 路径

边界约束：

- `responses[]` 不是聊天历史，不承载随意对话。
- `tool_logs[]` 不是开发调试垃圾桶，而是正式结果的一部分。
- `report_summary` 不是长篇报告全文，而是可在 UI 首屏展示的摘要。
- `validation` 与 `fallback` 必须作为顶层诊断字段显式保留。

## 运行时数据流

1. 用户上传会议视频。
2. `POST /api/upload` 返回文件引用和任务基础信息。
3. `POST /api/analyze` 创建分析任务。
4. backend 调度 pipeline，先跑解析与事件提取，再生成风险结果。
5. pipeline 输出结构化 JSON，backend 做 schema 校验和状态更新。
6. frontend 轮询任务状态，并在完成后拉取结果和报告。
7. frontend 展示风险卡片、事件列表、可疑时间段、日志面板和报告摘要。

## 失败回退路径

- 文件上传失败：返回失败状态与错误码，不创建分析结果。
- 外部工具调用失败：记录 `tool_logs`，将任务标记为 `degraded` 或 `partial_success`。
- schema 校验失败：拒绝进入正式结果态，尝试 fallback 结果。
- 真实 pipeline 未接入：返回 sample/mock 结果，并在 `responses` 与 `report_summary` 中说明来源。
- 前端拿不到完整字段：仅基于稳定字段渲染，并显示缺失/降级提示。

## 产品界面目标

虽然当前 Phase 1 以前后端合同和文档为主，但最终展示界面必须是 inspection workspace，而不是聊天框。首屏至少应包含：

- 上传入口或任务入口
- 任务状态与 `confidence`
- participant 风险卡片
- suspicious segment 列表或时间线
- event 列表
- tool logs
- report summary

如果前端未完成，demo 可以退回 backend + docs 路线；但课程最终提交前，UI 产品感仍是单独验收项。

## MVP 与 Future Work 的界线

### MVP / Phase 1

- 文档、合同、目录骨架。
- 最小 backend 服务。
- sample result 和 sample report。
- 前端页面结构说明与消费字段约束。

### Future Work

- 真实视频管线、任务队列、存储层、用户系统。
- 更细粒度深伪检测与多模态证据。
- 实时会议流分析、并发与成本治理。
