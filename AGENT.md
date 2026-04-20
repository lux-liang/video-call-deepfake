# MeetTruth Agent / Video Call Deepfake Inspector

## 项目目标

MeetTruth Agent 是一个面向多人视频会议回放场景的交互真实性巡检系统。系统的目标不是生成泛化对话，而是把会议视频输入转换为结构化分析结果，输出参会者风险分数、可疑时间段、异常事件、证据解释、自动巡检报告和 Harness 可视化日志。

## 产品边界

- 当前输入边界：会议回放视频，采用回放驱动的准实时分析模式。
- 当前输出边界：结构化 JSON 结果、风险卡片、事件列表、报告摘要、工具日志。
- 明确不做：训练模型、复杂实时流编排、无合同定义的接口扩展、聊天式产品交互。
- 产品不是“上传视频然后和 AI 聊天”的网页，而是“视频输入 -> 结构化分析 -> 风险评分 -> 解释报告”的 AI 工作流系统。

## 第一阶段与后续阶段

### Phase 1 / Bootstrap only

- 建立仓库骨架、目录结构和协作规则。
- 定义 API 合同、pipeline 输出合同和演示路径。
- 提供最小 backend 脚手架与 frontend 占位方案。
- 使用 mock/sample 数据跑通最小可演示闭环。

### 后续阶段

- 接入真实视频解析、VAD、OpenCV、MediaPipe、规则引擎与报告生成。
- 完成任务队列、异步状态机、结果回放、日志面板与 UI 打磨。
- 扩展到更接近实时流的处理和多会议并发。

## 工程约束

- API 合同先行，字段必须先在 handoff 文档中定义，再进入实现。
- Mock 先行，真实算法后接。
- 所有复杂模块必须提供 fallback 或降级路径。
- 任何低置信度结果必须显式打标，不能伪装成高置信结论。
- 不允许将整段原始会议视频直接丢给 LLM；必须先转成 participants、events、responses、tool_logs 等结构化上下文。
- 外部工具链视为一等公民：`ffmpeg`、`opencv`、`mediapipe`、`vad`、rules engine、reporting tools 会进入系统设计。
- 必须包含反馈闭环：schema 校验、字段完整性检查、失败回退、mock/fallback 策略、低置信度标记。

## 编码与提交规范

- 优先小步提交，保持 2 到 4 个清晰 commit。
- commit message 使用 Conventional Commits 风格。
- backend 与 docs 改动应保持合同一致，不允许实现先漂移。
- 目录、文件名、字段命名保持稳定，避免在 Phase 1 频繁重命名。
- 新增复杂逻辑时必须同步补文档或 handoff。

## 多 Codex 协同规则

- Staff / 总控 Codex 负责主干规则、合同边界、分支管理和整体验收。
- Backend Codex 只能在 API 合同范围内落地后端服务、任务状态与报告接口。
- Pipeline Codex 只能在 pipeline 合同范围内定义输出 JSON、mock/fallback 与处理阶段。
- Frontend Codex 只能消费稳定字段，不得私自发明结果字段。
- Docs / QA Codex 负责 README、演示脚本、验收清单、术语统一与 demo 校对。
- 任一子 Codex 需要新增字段时，必须先修改 handoff contract，再进行实现。

## 目录说明

- `docs/`: 架构、验收标准、demo 脚本、handoff 合同。
- `backend/`: FastAPI 最小服务、schemas、services、tests、pipeline 接入位。
- `frontend/`: 前端占位骨架、页面规划、API 对接说明。
- `demo/`: 样例视频说明、样例 JSON、样例输出报告。
- `outputs/`: 本地分析产物与导出结果。

## API 先行原则

- 先定义请求、响应、状态字段和错误语义，再实现路由。
- demo/sample 输出要复用未来正式 API 的稳定字段。
- 任何 breaking change 都必须先更新 `docs/handoffs/` 下合同文档。

## Definition of Done

第一阶段完成标准：

- 目录结构齐全并可供后续分工使用。
- `AGENT.md`、`TASKS.md`、`RUNLOG.md`、`README.md`、架构文档、验收清单、demo 脚本完整存在。
- backend 最小服务可启动，至少包含健康检查和 sample result 接口。
- demo 目录下存在样例结果模板和报告模板。
- handoff 合同明确稳定字段、状态字段、fallback 和降级规则。
- 至少完成 2 到 4 个清晰 commit。

## 总原则

- 先 MVP，后增强。
- 先可演示，后更真实。
- 先结构化上下文，后模型推理。
- 复杂模块必须有 fallback。
