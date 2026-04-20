# Backend Frontend Contract

## 目标

定义前后端稳定接口，保证 frontend 只依赖已声明字段，backend 只返回已合同化结构。Phase 1 可以返回 sample/mock 数据，但字段形状必须稳定。

## API 路径草案

- `POST /api/upload`
- `POST /api/analyze`
- `GET /api/task/{task_id}`
- `GET /api/result/{task_id}`
- `GET /api/report/{task_id}`
- `GET /api/demo/sample-result`
- `GET /healthz`

## 任务状态字段

`status` 可选值：

- `queued`
- `processing`
- `completed`
- `partial_success`
- `degraded`
- `failed`

## 接口定义

### `POST /api/upload`

用途：上传会议视频或创建上传占位记录。

请求体：

```json
{
  "filename": "team-sync.mp4",
  "content_type": "video/mp4",
  "source": "local_upload"
}
```

响应体：

```json
{
  "task_id": "task_demo_001",
  "meeting_id": "meeting_demo_001",
  "upload_id": "upload_demo_001",
  "status": "queued",
  "message": "upload accepted"
}
```

### `POST /api/analyze`

用途：基于上传结果触发分析任务。

请求体：

```json
{
  "meeting_id": "meeting_demo_001",
  "upload_id": "upload_demo_001",
  "mode": "playback_mock",
  "use_mock": true
}
```

响应体：

```json
{
  "task_id": "task_demo_001",
  "meeting_id": "meeting_demo_001",
  "status": "processing",
  "estimated_mode": "playback_mock"
}
```

### `GET /api/task/{task_id}`

用途：轮询任务状态。

响应体：

```json
{
  "task_id": "task_demo_001",
  "meeting_id": "meeting_demo_001",
  "status": "completed",
  "progress": 100,
  "stage": "reporting",
  "confidence": 0.78,
  "error": null
}
```

### `GET /api/result/{task_id}`

用途：获取结构化分析结果。

响应体稳定字段：

```json
{
  "meeting_id": "meeting_demo_001",
  "status": "completed",
  "confidence": 0.78,
  "participants": [],
  "events": [],
  "responses": [],
  "risk_scores": [],
  "suspicious_segments": [],
  "tool_logs": [],
  "report_summary": {
    "headline": "string",
    "overview": "string",
    "recommended_actions": []
  }
}
```

### `GET /api/report/{task_id}`

用途：获取可渲染报告。

响应体：

```json
{
  "task_id": "task_demo_001",
  "meeting_id": "meeting_demo_001",
  "status": "completed",
  "report_markdown": "# Sample Report",
  "generated_at": "2026-04-20T00:00:00Z"
}
```

### `GET /api/demo/sample-result`

用途：返回前端联调使用的 sample 数据。

响应体：与 `GET /api/result/{task_id}` 同 schema。

## 结果展示所需稳定字段

### `participants[]`

- `participant_id`
- `display_name`
- `role`
- `dominant_risk_level`
- `notes`

### `events[]`

- `event_id`
- `participant_id`
- `timestamp_start`
- `timestamp_end`
- `event_type`
- `severity`
- `summary`
- `evidence_refs[]`

### `responses[]`

- `response_id`
- `kind`
- `source`
- `summary`
- `confidence`

### `risk_scores[]`

- `participant_id`
- `score`
- `level`
- `reasons[]`

### `suspicious_segments[]`

- `segment_id`
- `timestamp_start`
- `timestamp_end`
- `participant_ids[]`
- `reason`
- `confidence`

### `tool_logs[]`

- `tool_name`
- `status`
- `started_at`
- `ended_at`
- `summary`
- `artifacts[]`

## 前端兼容要求

- 前端只依赖已列出的稳定字段。
- 若数组字段缺失，backend 必须返回空数组而不是省略。
- 若结果是降级或 mock，`status` 与 `responses` 中必须显式说明。
- `confidence` 必须始终存在，哪怕仅为低置信 mock 值。
