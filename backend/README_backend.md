# Backend Bootstrap

## 当前目标

提供 MeetTruth Agent 的最小 FastAPI 骨架，支撑 Phase 1 演示与前后端联调。

## 当前已包含

- `GET /healthz`
- `GET /api/demo/sample-result`
- `POST /api/upload`
- `POST /api/analyze`
- `GET /api/task/{task_id}`
- `GET /api/result/{task_id}`
- `GET /api/report/{task_id}`

## 运行方式

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Phase 1 约束

- 以 sample/mock 数据为主。
- 不引入复杂持久化。
- 所有返回字段遵守 handoff contract。
