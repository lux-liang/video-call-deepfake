# Pipeline Backend Contract

## 目标

定义 pipeline 到 backend 的结构化输出，确保 backend 可以校验、持久化、降级和对外暴露稳定结果。

## 顶层 JSON 结构

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
  "report_summary": {},
  "validation": {},
  "fallback": {}
}
```

## Participant Schema

```json
{
  "participant_id": "p_001",
  "display_name": "Alice",
  "role": "speaker",
  "track_ref": "video_track_1",
  "dominant_risk_level": "medium",
  "notes": "intermittent lip-sync mismatch",
  "metadata": {
    "seat_hint": "top-left"
  }
}
```

## Event Schema

```json
{
  "event_id": "evt_001",
  "participant_id": "p_001",
  "timestamp_start": 42.5,
  "timestamp_end": 49.0,
  "event_type": "lip_sync_mismatch",
  "severity": "high",
  "summary": "visible mouth motion diverges from active speech window",
  "evidence_refs": [
    "frame:001240",
    "audio:seg_014"
  ]
}
```

## Response Schema

`responses[]` 用于承载 agent 或规则层的结构化解释，不是自由文本聊天历史。

```json
{
  "response_id": "resp_001",
  "kind": "explanation",
  "source": "rule_engine",
  "summary": "high-risk event cluster around participant p_001",
  "confidence": 0.74
}
```

## Risk Score Schema

```json
{
  "participant_id": "p_001",
  "score": 0.81,
  "level": "high",
  "reasons": [
    "multiple lip-sync mismatches",
    "face boundary instability"
  ]
}
```

## Suspicious Segment Schema

```json
{
  "segment_id": "seg_002",
  "timestamp_start": 42.5,
  "timestamp_end": 61.0,
  "participant_ids": [
    "p_001"
  ],
  "reason": "clustered visual and audio inconsistency",
  "confidence": 0.79
}
```

## Tool Log Schema

```json
{
  "tool_name": "ffmpeg",
  "status": "success",
  "started_at": "2026-04-20T00:00:00Z",
  "ended_at": "2026-04-20T00:00:12Z",
  "summary": "audio extracted and frames sampled",
  "artifacts": [
    "outputs/meeting_demo_001/audio.wav",
    "outputs/meeting_demo_001/frames/"
  ]
}
```

## Report Summary Schema

```json
{
  "headline": "participant p_001 flagged with elevated synthetic-behavior risk",
  "overview": "analysis detected clustered anomalies in visual-audio alignment and face stability",
  "recommended_actions": [
    "request manual review",
    "compare against known identity sample"
  ]
}
```

## Validation Schema

```json
{
  "schema_valid": true,
  "missing_fields": [],
  "warnings": [],
  "validator_version": "phase1"
}
```

## Fallback / Mock Schema

当真实 pipeline 不可用时，允许返回 fallback 结构，但必须保留顶层字段，并显式说明来源。

```json
{
  "mode": "mock",
  "reason": "real pipeline not connected",
  "degraded_fields": [],
  "used_sample": true
}
```

## 失败时的降级字段

- `status` 可为 `partial_success`、`degraded` 或 `failed`。
- `confidence` 不可缺失；失败时可取低值，例如 `0.2`。
- `participants`、`events`、`responses`、`risk_scores`、`suspicious_segments`、`tool_logs` 必须返回数组，即使为空。
- `validation.missing_fields` 必须列出缺失字段。
- `fallback.reason` 必须解释为何降级。
- `responses[]` 中至少应有一条说明本次结果来自 mock、sample 或部分真实管线。
