# Demo Script

## 目标

在 3 分钟内把 MeetTruth Agent 讲成一个“可提交作业”的 AI 原生产品，而不是一堆源码文件。当前优先使用 backend + sample artifacts 的稳定路线；如果 `feat/frontend` 已补齐页面，可把第 4 到第 6 步替换成 workspace 演示。

## 录屏前准备

1. 打开以下文件或页面备用：
   - `README.md`
   - `docs/architecture.md`
   - `docs/acceptance_checklist.md`
   - `demo/sample_outputs/sample_report.md`
2. 在 `backend/` 启动服务：

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

3. 浏览器准备三个地址：
   - `http://127.0.0.1:8000/healthz`
   - `http://127.0.0.1:8000/api/demo/sample-result`
   - `http://127.0.0.1:8000/api/report/task_demo_001`

## 3 分钟镜头顺序

| 时间 | 画面 | 你要说什么 |
| --- | --- | --- |
| 00:00 - 00:25 | `README.md` 顶部 | “MeetTruth Agent 解决的是多人视频会议中的交互真实性巡检问题，输入是会议视频，输出不是聊天回复，而是结构化风险结果。” |
| 00:25 - 00:50 | `README.md` 的痛点与 AI 原生部分 | “我们关心的是哪个 participant 有风险、哪个时间段可疑、哪些 event 触发判断，以及工具链到底做了什么。” |
| 00:50 - 01:15 | `docs/architecture.md` 的 Harness 部分 | “这个产品是 AI native workflow，不把原视频直接喂给模型，而是先转成 participants、events、responses、suspicious segments、tool logs，再做 explanation。” |
| 01:15 - 01:30 | `/healthz` | “后端骨架已可启动，先看健康检查。” |
| 01:30 - 02:10 | `/api/demo/sample-result` | “这里可以看到 sample 结果已经按稳定合同输出，包括 participant、event、response、risk_scores、suspicious_segments、tool_logs、validation 和 fallback。” |
| 02:10 - 02:35 | `demo/sample_outputs/sample_report.md` 或 `/api/report/task_demo_001` | “结构化结果会继续落到 report summary 和 Markdown 报告，方便人工复核或后续导出。” |
| 02:35 - 02:50 | `docs/acceptance_checklist.md` | “课程要求里的 Harness、3 分钟 demo、GitHub 交付、UI 产品感都已经被显式列成验收项。” |
| 02:50 - 03:00 | 回到 README 的待补位说明 | “当前真实 pipeline 和前端产品化界面还在补位，但合同、样例、验收和 demo 路径已经稳定，可以继续并行开发。” |

## 讲解时必须点名的字段

录屏时不要只说“这里是 JSON”，要至少点名以下字段：

- `participants`
- `events`
- `responses`
- `suspicious_segments`
- `tool_logs`
- `report_summary`
- `validation`
- `fallback`

推荐点名样例值：

- `participants[0].display_name = Alice`
- `events[0].event_type = lip_sync_mismatch`
- `tool_logs[0].tool_name = ffmpeg`
- `tool_logs[1].status = mocked`
- `fallback.mode = mock`

## 必讲结论

- 输入是会议视频，不是文本 prompt。
- 产品主界面目标是 inspection workspace，不是聊天网页。
- LLM 或 agent 只消费结构化上下文，不直接吞整段视频。
- 工具链是显式的，不是隐藏在模型黑盒里。
- 当前 demo 是 sample / mock，但合同和验收口径已经稳定。
- 结果必须经过 verification，失败时允许 degraded / fallback，演示不会断链。

## 可选增强镜头

如果 `feat/frontend` 已完成 workspace 页面，可把 `/api/demo/sample-result` 的 JSON 演示替换为 UI 演示，但仍需保留 10 到 15 秒说明 `tool_logs`、`validation` 和 `fallback`，否则课程要求里的 Harness 会讲弱。

## 当前 fallback demo 路线

若前端还没完成，不要临时切聊天式演示。直接按本脚本走 backend + docs 路线即可，因为这条路径已经把：

- 痛点定义
- AI 原生定位
- 非聊天网页边界
- Harness 三件套
- sample result
- report summary
- 验证与降级

全部覆盖了。
