# MeetTruth Agent / Video Call Deepfake Inspector

MeetTruth Agent 是一个面向多人视频会议回放场景的交互真实性巡检系统。它不是“上传视频后跟 AI 聊天”的网页，而是把会议视频输入转换为结构化巡检结果，输出 participant 风险分数、event 列表、suspicious segment、tool logs 和 report summary。

## 提交视角

这个仓库当前要交付的不是单一模型效果，而是一个可验收的 AI 原生产品骨架：

- 一份对外可读的 README
- 一套稳定的 backend / pipeline / frontend 合同
- 一条可直接录制的 3 分钟 demo 路径
- 一份能逐项打勾的 acceptance checklist
- 一套统一术语，避免四个分支各自发明名字
- 一个可放到 GitHub 直接提交课程作业的仓库结构

## 痛点定义

多人视频会议中的深伪风险不是一句“像不像假脸”能解决的。真实使用场景需要同时回答：

- 哪个 participant 风险最高
- 哪个时间段最可疑
- 哪些 event 触发了系统判断
- 当前结论来自真实工具链还是 mock / fallback
- 工具到底做了什么，哪里失败，哪里降级

普通聊天网页很难稳定承载这些需求，因为输入是视频工作流，输出是结构化巡检结果，而不是开放式对话。

## 为什么这是 AI 原生产品

MeetTruth Agent 的核心是 workflow，不是 chat。

1. 输入是会议视频和任务状态，不是自然语言 prompt。
2. 中间层是结构化上下文，不是把整段视频直接丢给 LLM。
3. 结果需要经过工具链、验证、降级和报告生成，不是直接吐一段自由文本。
4. 产物是 participant 风险卡片、event 列表、suspicious segment、tool logs、report summary 和报告，而不是聊天记录。

## 为什么它不是普通聊天网页

普通聊天网页通常以“用户问一句，模型答一句”为中心。MeetTruth Agent 则以“视频输入 -> 任务创建 -> pipeline 处理 -> 结构化结果 -> 验证 -> 报告”作为主路径。LLM 或 agent 只负责受约束的 explanation / summary，不负责替代整条分析链路。

因此，课程要求中的“不要只是聊天网页”在本项目里通过三个层面被显式满足：

- 工作流入口不是聊天框，而是上传、任务状态和结果面板
- 数据主载体是结构化 schema，而不是自由文本历史
- 系统显式依赖外部工具与反馈闭环，而不是单个模型黑盒输出

## Harness Engineering

本项目在 README 与架构文档里显式覆盖三类 Harness Engineering。

### 1. Context Management / Agent Skill

- 不把整段原始会议视频直接丢给 LLM
- 先把会议压缩成 `participants`、`events`、`responses`、`risk_scores`、`suspicious_segments`、`tool_logs`
- agent 只消费验证后的结构化上下文和摘要

### 2. Tool Use / MCP / External Tools

- 系统显式依赖 `ffmpeg`、`opencv`、`mediapipe`、`vad`、rules engine、reporting tools
- `tool_logs` 是稳定字段，不是调试附属物
- 后续可用 MCP 或 service adapter 统一封装工具调用

### 3. Feedback Loop / Verification

- pipeline 输出必须经过 schema 校验和字段完整性检查
- 低置信度必须显式显示 `confidence`
- 工具失败时必须保留 `validation` 与 `fallback`
- demo 不能因为真实 pipeline 未接入而断链，必须允许 sample / mock / degraded 路径

## 课程要求映射

| 课程要求 | README / 文档位置 | 当前状态 |
| --- | --- | --- |
| 痛点定义 | 本 README 的“痛点定义” | 已写明 |
| 为什么是 AI 原生产品 | 本 README 的“为什么这是 AI 原生产品”与 [docs/architecture.md](docs/architecture.md) | 已写明 |
| 为什么不是普通聊天网页 | 本 README 的“为什么它不是普通聊天网页”与 [docs/demo_script.md](docs/demo_script.md) | 已写明 |
| Context Management / Agent Skill | 本 README 的 “Harness Engineering / Context Management” | 已写明 |
| Tool Use / MCP / External Tools | 本 README 的 “Harness Engineering / Tool Use” 与 [docs/architecture.md](docs/architecture.md) | 已写明 |
| Feedback Loop / Verification | 本 README 的 “Harness Engineering / Feedback Loop” 与 [docs/acceptance_checklist.md](docs/acceptance_checklist.md) | 已写明 |
| 3 分钟 demo 路径 | [docs/demo_script.md](docs/demo_script.md) | 已写明 |
| GitHub 代码仓库交付 | 本 README 的“GitHub 交付物” | 已写明 |
| UI 有产品感，不粗糙 | [docs/acceptance_checklist.md](docs/acceptance_checklist.md) 与 [docs/handoffs/frontend_handoff.md](docs/handoffs/frontend_handoff.md) | 待前端补位 |

## 系统架构概览

系统按以下层次组织：

1. `ingestion`
   - 接收会议视频、元数据和任务请求。
2. `parsing`
   - 使用 `ffmpeg` 等工具拆轨、抽帧、切片、对齐时间戳。
3. `event extraction`
   - 使用 OpenCV、MediaPipe、VAD、规则引擎或后续模型提取异常 event。
4. `behavior features`
   - 将 segment 级 event 聚合为 participant 级行为特征。
5. `scoring`
   - 生成 participant 风险分数和 suspicious segment。
6. `explanation`
   - 基于结构化上下文生成 response。
7. `reporting`
   - 产出 JSON、report summary、Markdown 报告与 tool logs。

更多细节见 [docs/architecture.md](docs/architecture.md)。

## 统一术语

以下术语在 README、handoff、sample JSON、验收清单和 demo 中统一使用：

- `participant`: 参会者实体，不再混用 member / speaker / user
- `event`: 结构化异常事件，不再混用 signal / anomaly item
- `response`: agent 或规则层的结构化解释，不是聊天回复
- `suspicious segment`: 可疑时间段，不再混用 clip / slice / interval
- `tool logs`: 外部工具执行记录，不再混用 debug logs / pipeline traces
- `report summary`: 面向 UI 和报告页的摘要对象，不再混用 conclusion / final answer

## Phase 1 当前可交付内容

### Backend

- `GET /healthz`
- `POST /api/upload`
- `POST /api/analyze`
- `GET /api/task/{task_id}`
- `GET /api/result/{task_id}`
- `GET /api/report/{task_id}`
- `GET /api/demo/sample-result`

### 文档与样例

- [docs/architecture.md](docs/architecture.md)
- [docs/acceptance_checklist.md](docs/acceptance_checklist.md)
- [docs/demo_script.md](docs/demo_script.md)
- [docs/handoffs/backend_frontend_contract.md](docs/handoffs/backend_frontend_contract.md)
- [docs/handoffs/pipeline_backend_contract.md](docs/handoffs/pipeline_backend_contract.md)
- [demo/sample_json/sample_result.json](demo/sample_json/sample_result.json)
- [demo/sample_outputs/sample_report.md](demo/sample_outputs/sample_report.md)

## 快速启动

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

启动后可验证：

- `GET /healthz`
- `GET /api/demo/sample-result`
- `GET /api/report/task_demo_001`

### Frontend

当前 `frontend/` 仍是 Phase 1 占位结构，尚未初始化完整页面实现。约束和 UI 目标见 [frontend/README_frontend.md](frontend/README_frontend.md) 与 [docs/handoffs/frontend_handoff.md](docs/handoffs/frontend_handoff.md)。

## 3 分钟 Demo 路径

推荐录屏顺序：

1. 打开本 README，先讲痛点、AI 原生定位和非聊天网页边界
2. 打开 [docs/architecture.md](docs/architecture.md)，强调 Harness 三件套
3. 启动 backend，验证 `GET /healthz`
4. 打开 `GET /api/demo/sample-result`，展示 `participants`、`events`、`responses`、`suspicious_segments`、`tool_logs`、`validation`、`fallback`
5. 打开 [demo/sample_outputs/sample_report.md](demo/sample_outputs/sample_report.md)，展示 report summary 如何落到报告
6. 打开 [docs/acceptance_checklist.md](docs/acceptance_checklist.md)，说明课程要求如何被验收
7. 结尾强调 GitHub 仓库交付、当前待补位项与下一阶段扩展

完整讲稿与时间切分见 [docs/demo_script.md](docs/demo_script.md)。

## GitHub 交付物

课程提交时，仓库至少应包含：

- 可直接阅读的 `README.md`
- `docs/architecture.md`
- `docs/acceptance_checklist.md`
- `docs/demo_script.md`
- `docs/handoffs/` 下的合同文档
- 最小 backend scaffold
- sample result 与 sample report
- 清晰 commit 历史

如果课程要求展示 UI，建议在最终提交前补充：

- 一张 workspace 总览截图
- 一张 participant 风险卡片与 suspicious segment 视图截图
- 一张 tool logs / report summary 截图

## 当前待补位说明

以下项目已经在文档中被显式标注，但仍待其他分支落地：

- 前端产品化界面尚未完成，当前只能通过 README、sample JSON 与 API 演示 workflow
- 真实 pipeline 尚未接入，当前结果来自 sample / mock
- 仓库尚未提交真实会议视频样本，演示依赖 sample result 与 sample report

这些缺口不会阻断本轮 docs/QA 交付，但会影响课程最终演示完整度，因此已在验收清单中标为 `PENDING`。

## 关键文档

- [AGENT.md](AGENT.md)
- [TASKS.md](TASKS.md)
- [RUNLOG.md](RUNLOG.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/acceptance_checklist.md](docs/acceptance_checklist.md)
- [docs/demo_script.md](docs/demo_script.md)
- [docs/handoffs/backend_frontend_contract.md](docs/handoffs/backend_frontend_contract.md)
- [docs/handoffs/pipeline_backend_contract.md](docs/handoffs/pipeline_backend_contract.md)

## Limitations

- 当前结果为 sample / mock，不代表真实深伪检测精度
- 当前未接入真实视频处理 pipeline
- 当前前端 UI 仍是占位，不代表最终产品完成度
- 当前无持久化、任务队列或用户系统
