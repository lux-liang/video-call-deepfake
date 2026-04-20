# Backend P0

MeetTruth Agent backend 现在提供可跑的 Phase 1 P0 API 服务。当前目标不是接入真实检测流水线，而是先把稳定 API、稳定 schema、稳定错误处理和 sample/mock fallback 打通。

## 当前接口

- `GET /health`
- `GET /healthz`
- `GET /api/demo/sample-result`
- `POST /api/upload`
- `POST /api/analyze`
- `GET /api/task/{task_id}`
- `GET /api/result/{task_id}`
- `GET /api/report/{task_id}`

## 当前行为

- `POST /api/upload` 只创建上传占位和任务状态，不保存真实文件。
- `POST /api/analyze` 会基于 `mode` 和 `use_mock` 选择 sample/mock 或 real-placeholder 路径。
- `mode=playback_mock` 或 `mode=sample` 时，返回合同化 sample 结果。
- `mode=pipeline_real` 且 `use_mock=false` 时，会先走 real pipeline 占位，再因字段不完整自动降级到 sample/mock fallback。
- 所有错误都会返回统一 JSON：

```json
{
  "status": "failed",
  "error": {
    "code": "request_validation_error",
    "message": "request validation failed",
    "details": []
  }
}
```

## Feedback Loop

后端层已显式实现以下闭环：

- `pydantic` schema validation
- 上传输入文件名和 `content_type` 校验
- pipeline 结果缺字段时自动降级
- pipeline schema 无法通过时自动降级
- 任务未完成时返回稳定 placeholder result
- real pipeline 未接入或执行失败时返回低置信度 sample/mock fallback，而不是直接报 500

## 项目结构

- `app/api/`: 路由和依赖注入
- `app/schemas/`: 稳定 Pydantic schema
- `app/services/`: 任务状态、分析调度、报告生成、sample 数据
- `tests/`: P0 最小回归测试

## 运行方式

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

服务默认地址：

```text
http://127.0.0.1:8000
```

## 最小联调示例

```bash
curl http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/api/upload \
  -H 'Content-Type: application/json' \
  -d '{"filename":"team-sync.mp4","content_type":"video/mp4","source":"local_upload"}'
```

```bash
curl -X POST http://127.0.0.1:8000/api/analyze \
  -H 'Content-Type: application/json' \
  -d '{"meeting_id":"meeting_xxx","upload_id":"upload_xxx","mode":"playback_mock","use_mock":true}'
```

## 测试

```bash
cd backend
python -m unittest discover -s tests -v
```

## 限制

- 当前任务状态使用进程内内存存储，重启后不会保留。
- 当前不处理真实 multipart 文件上传。
- 当前报告来自 sample/result aggregation，不代表真实检测结论。
- 合同字段保持稳定，真实 pipeline 只允许在合同范围内替换内部实现。
