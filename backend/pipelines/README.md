# Pipelines

当前目录提供一个 mock-to-real 的最小可演示 pipeline，把“会议回放 -> 结构化分析 JSON”跑通到 contract 对齐结果。

## P0 范围

- 稳定输出 `meeting_id`、`participants`、`events`、`responses`、`risk_scores`、`suspicious_segments`、`tool_logs`、`report_summary`、`confidence`、`status`
- P0 事件仅覆盖 `speaker_switch`、`named_response`、`screen_share_change`
- P0 行为特征仅覆盖 `mouth onset`、`head pose change`、`response latency`
- 无真实视频时直接返回 `demo/sample_json/sample_result.json`
- 阶段失败时只降级，不让整个 pipeline 崩掉

## 脚本

- `backend/pipelines/extract_frames.py`
  - 输入视频路径或空输入
  - 输出最小 frame manifest、speaker turns、screen-share windows
- `backend/pipelines/detect_events.py`
  - 从 frame manifest 生成 P0 事件
- `backend/pipelines/extract_behavior.py`
  - 从事件和 turn 数据提取最小行为特征
- `backend/pipelines/score_risk.py`
  - 用简单规则权重生成 `risk_scores` 和 `suspicious_segments`
- `backend/pipelines/run_pipeline.py`
  - 串联全部阶段并返回最终 contract JSON

## 运行方式

返回稳定 sample 结果：

```bash
python3 backend/pipelines/run_pipeline.py --use-sample
```

从视频路径跑最小 heuristic pipeline：

```bash
python3 backend/pipelines/run_pipeline.py --video-path /path/to/meeting.mp4 --meeting-id meeting_demo_real
```

单独运行某一阶段：

```bash
python3 backend/pipelines/extract_frames.py --video-path /path/to/meeting.mp4 --output outputs/meeting_demo_real/frames.json
python3 backend/pipelines/detect_events.py --input outputs/meeting_demo_real/frames.json --output outputs/meeting_demo_real/events.json
python3 backend/pipelines/extract_behavior.py --frames outputs/meeting_demo_real/frames.json --events outputs/meeting_demo_real/events.json --output outputs/meeting_demo_real/behavior.json
python3 backend/pipelines/score_risk.py --frames outputs/meeting_demo_real/frames.json --events outputs/meeting_demo_real/events.json --behavior outputs/meeting_demo_real/behavior.json --output outputs/meeting_demo_real/risk.json
```

## 降级策略

- 缺少视频路径：直接返回稳定 sample JSON
- 视频路径存在但没有复杂依赖：使用确定性 heuristic 生成阶段结果
- 某阶段异常：记录 `tool_logs` 与 `fallback`，必要时注入 sample 或简化 heuristic 结果
- 最终输出始终包含 contract 顶层字段和 `validation`

## 当前限制

- 尚未接入真实 `ffmpeg`、OpenCV、MediaPipe 或 VAD
- 行为特征来自规则和确定性 heuristics，不代表真实检测精度
- `tool_logs` 反映的是当前阶段的 mock / heuristic / degraded 状态，而不是完整生产环境执行轨迹
