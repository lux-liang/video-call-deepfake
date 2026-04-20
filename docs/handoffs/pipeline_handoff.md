# Pipeline Handoff

## 负责范围

- 负责 ingestion 后的 parsing、event extraction、behavior features、scoring 原型。
- 严格遵守 `pipeline_backend_contract.md` 输出 JSON。

## 当前输入

- Phase 1 已定义 participant、event、response、risk score、fallback、validation 结构。

## 交付要求

- 先提供 mock-to-real 可切换的 pipeline entry。
- 任意阶段失败都要输出 `tool_logs`、`validation` 和 `fallback` 信息。
- 保证 `confidence` 与 `status` 始终存在。

## 当前实现状态

- 已补齐 `backend/pipelines/extract_frames.py`
- 已补齐 `backend/pipelines/detect_events.py`
- 已补齐 `backend/pipelines/extract_behavior.py`
- 已补齐 `backend/pipelines/score_risk.py`
- 已补齐 `backend/pipelines/run_pipeline.py`
- `demo/sample_json/sample_result.json` 已升级为稳定前端演示输入

## 当前行为

- `run_pipeline.py --use-sample` 或未提供 `--video-path` 时，直接返回稳定 sample 结果
- 提供存在的视频路径时，走确定性 heuristic pipeline，并写出阶段产物到 `outputs/<meeting_id>/`
- 阶段失败时，按模块注入 fallback 结果，保留 `tool_logs`、`responses`、`validation`、`fallback`

## P0 事件与行为特征

- 事件：`speaker_switch`、`named_response`、`screen_share_change`
- 行为特征：`mouth onset`、`head pose change`、`response latency`

## 自检

- 已增加 `backend/tests/test_pipeline_contract.py`
- 自检覆盖 sample JSON 顶层字段、P0 事件覆盖、sample mode CLI、heuristic mode CLI

## 非目标

- 不在 Phase 1 追求复杂模型训练。
- 不跳过验证直接返回不完整字段。
