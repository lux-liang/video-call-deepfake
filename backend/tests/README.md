# Backend Tests

当前提供最小 P0 测试套件，覆盖：

- `GET /health`
- `GET /api/demo/sample-result`
- `POST /api/upload` 的输入校验和错误返回
- `POST /api/analyze` -> `GET /api/task` -> `GET /api/result` -> `GET /api/report` 的最小闭环
- `pipeline_real` 未接入时的 degraded/sample fallback 路径

运行方式：

```bash
cd backend
python -m unittest discover -s tests -v
```
