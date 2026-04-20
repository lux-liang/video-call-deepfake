# MeetTruth Agent / Video Call Deepfake Inspector

MeetTruth Agent 是一个面向多人视频会议场景的交互真实性巡检系统。它的目标不是把视频上传后变成聊天网页，而是将会议视频输入转换为结构化分析结果，输出风险分数、可疑时间段、异常事件、证据解释、自动巡检报告和 Harness 可视化日志。

## 痛点定义

多人视频会议中的深伪风险并不只是“有没有假脸”这么简单。业务真正需要的是：

- 哪个参会者风险更高
- 哪个时间段最可疑
- 哪些结构化事件触发了风险判断
- 系统的结论依据是什么
- 工具链实际做了哪些处理

传统聊天式 AI 界面无法稳定承载这些需求，因为输入是视频工作流，输出是结构化巡检结果，而不是开放式对话。

## 产品定位

这是一个“视频输入 -> 结构化分析 -> 风险评分 -> 解释报告”的 AI 工作流系统。

不是：

- 上传视频后和 AI 聊天
- 单纯的视频播放器
- 一次性端到端黑盒模型展示

是：

- 面向会议回放的准实时分析工作流
- 以结构化上下文驱动的 AI 原生系统
- 可逐步扩展到真实 pipeline、实时流和人工复核闭环的工程底座

## 系统架构概览

系统按以下层次组织：

1. `ingestion`
   - 接收会议视频与任务请求。
2. `parsing`
   - 使用外部工具进行拆轨、抽帧、时间切片。
3. `event extraction`
   - 提取异常事件，例如口型不同步、边界不稳定、说话轮次异常等。
4. `behavior features`
   - 将片段级事件聚合为 participant 级特征。
5. `scoring`
   - 计算风险分数与可疑时间段。
6. `explanation`
   - 基于结构化上下文生成证据解释。
7. `reporting`
   - 输出 JSON、报告和工具日志面板。

详见 [docs/architecture.md](/mnt/c/Users/luxli/video-call-deepfake/docs/architecture.md)。

## Harness Engineering

本项目在 README 与架构设计中显式满足至少三项 Harness Engineering：

### 1. Context Management / Agent Skill

- 不把整段原始会议视频直接丢给 LLM。
- 先把会议表示为 `participants`、`events`、`responses`、`risk_scores`、`suspicious_segments`、`tool_logs` 等结构化上下文。
- LLM 只消费经过压缩和验证的结构化信息。

### 2. Tool Use / MCP / External Tools

- 系统明确依赖 `ffmpeg`、`opencv`、`mediapipe`、`vad`、rules engine、reporting tools 等外部工具链。
- `tool_logs` 是稳定字段，用于记录工具执行情况、产物和降级原因。

### 3. Feedback Loop / Verification

- 所有 pipeline 输出都需要经过 schema 校验和字段完整性检查。
- 低置信度必须显式标记。
- 真实工具链失败时必须允许 fallback、mock 或 degraded 路径继续返回可演示结果。

## 技术栈

- Backend: FastAPI
- Frontend: Next.js App Router + TypeScript + Tailwind CSS（推荐，Phase 1 仅保留骨架说明）
- Pipeline: `ffmpeg`、OpenCV、MediaPipe、VAD、规则引擎、后续模型模块
- Docs / Demo: Markdown、sample JSON、sample report

## 当前阶段能力

当前为 `Phase 1 / Bootstrap only`，重点是骨架、规则、合同和最小脚手架：

- 已建立目录结构和协作规则
- 已定义 backend/frontend contract 与 pipeline/backend contract
- 已建立最小 FastAPI 骨架
- 已提供 sample result 与 sample report
- 已提供 mock-to-real 的最小 pipeline CLI 和阶段脚本
- 已建立 frontend 占位说明
- 已提供验收清单与 demo 脚本

当前不包含：

- 真实深伪检测算法
- 模型训练
- 实时流分析
- 完整前端应用

## 快速启动

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

可用接口：

- `GET /healthz`
- `GET /api/demo/sample-result`
- `POST /api/upload`
- `POST /api/analyze`
- `GET /api/task/{task_id}`
- `GET /api/result/{task_id}`
- `GET /api/report/{task_id}`

### Pipeline CLI

稳定 sample 输出：

```bash
python3 backend/pipelines/run_pipeline.py --use-sample
```

最小 heuristic 流水线：

```bash
python3 backend/pipelines/run_pipeline.py --video-path /path/to/meeting.mp4 --meeting-id meeting_demo_real
```

各阶段脚本说明见 `backend/pipelines/README.md`。

### Frontend

Phase 1 暂未初始化完整 Next.js 项目，见 [frontend/README_frontend.md](/mnt/c/Users/luxli/video-call-deepfake/frontend/README_frontend.md)。

## Demo 路径

- sample 结构化结果：[demo/sample_json/sample_result.json](/mnt/c/Users/luxli/video-call-deepfake/demo/sample_json/sample_result.json)
- sample 报告：[demo/sample_outputs/sample_report.md](/mnt/c/Users/luxli/video-call-deepfake/demo/sample_outputs/sample_report.md)
- demo 脚本：[docs/demo_script.md](/mnt/c/Users/luxli/video-call-deepfake/docs/demo_script.md)

## 目录结构

```text
.
├─ README.md
├─ AGENT.md
├─ TASKS.md
├─ RUNLOG.md
├─ docs/
├─ backend/
├─ frontend/
├─ demo/
└─ outputs/
```

## Roadmap

### P0

- 上传会议视频
- 返回 mock/sample 结构化结果
- 显示风险卡片、事件列表、可疑时间段和工具日志
- demo 可录

### P1

- 接入真实 pipeline
- 增加任务轮询、报告视图和 UI 打磨
- 增加 schema 校验和 fallback 执行逻辑

### P2

- 实时流接入
- 多视频并行处理
- 增强分析与人工复核闭环

## Limitations

- 当前结果为 sample/mock，不代表真实检测能力。
- 当前仅接入 mock/heuristic 视频处理管线，尚未接入真实 `ffmpeg`、OpenCV、MediaPipe 或 VAD。
- 当前前端仅提供骨架说明，不提供完整页面实现。
- 当前无持久化、任务队列或用户系统。

## 关键文档

- [AGENT.md](/mnt/c/Users/luxli/video-call-deepfake/AGENT.md)
- [TASKS.md](/mnt/c/Users/luxli/video-call-deepfake/TASKS.md)
- [RUNLOG.md](/mnt/c/Users/luxli/video-call-deepfake/RUNLOG.md)
- [docs/architecture.md](/mnt/c/Users/luxli/video-call-deepfake/docs/architecture.md)
- [docs/handoffs/backend_frontend_contract.md](/mnt/c/Users/luxli/video-call-deepfake/docs/handoffs/backend_frontend_contract.md)
- [docs/handoffs/pipeline_backend_contract.md](/mnt/c/Users/luxli/video-call-deepfake/docs/handoffs/pipeline_backend_contract.md)
