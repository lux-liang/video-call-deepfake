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

## 非目标

- 不在 Phase 1 追求复杂模型训练。
- 不跳过验证直接返回不完整字段。
