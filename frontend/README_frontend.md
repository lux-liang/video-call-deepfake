# Frontend P0

## 当前状态

前端已实现 Phase 1 / P0 可演示闭环，不再只是占位目录。

当前页面目标是“会议真实性巡检控制台”，不是聊天页面：

- 首页 `/`
  - 产品定位
  - Harness 三件套说明
  - demo 入口
  - 工作流概览
- 工作台 `/workspace`
  - 上传与开始分析区
  - demo 样例入口
  - 任务进度 / 分析状态
  - 参会者风险卡片区
  - 事件列表区
  - 可疑时间段 / 时间轴区
  - 工具调用日志区
  - 报告摘要区
  - Context Management / Tool Use / Feedback Loop 显式可视化

## 技术栈

- Next.js App Router
- TypeScript
- Tailwind CSS
- 原生 `fetch` + 客户端轮询

## 启动方式

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动前端

```bash
cd frontend
npm run dev
```

默认访问：

- `http://localhost:3000/`
- `http://localhost:3000/workspace`
- `http://localhost:3000/workspace?mode=demo`

### 3. 可选：接本地 backend

默认前端通过 Next Route Handler 代理到：

```bash
http://127.0.0.1:8000
```

可通过环境变量覆盖：

```bash
MEETTRUTH_API_BASE_URL=http://127.0.0.1:8000
```

## 数据模式

### Demo / Mock 模式

- 进入 `/workspace?mode=demo`
- 使用前端内置 sample task sequence、sample result、sample report
- 可直接演示完整结果页
- 不依赖 backend 是否启动

适合：

- 录屏
- 课堂展示
- 信息架构验收

### Live API 模式

工作台上传区会按合同调用：

- `POST /api/upload`
- `POST /api/analyze`
- `GET /api/task/{task_id}`
- `GET /api/result/{task_id}`
- `GET /api/report/{task_id}`

前端只消费合同稳定字段：

- `participants`
- `events`
- `responses`
- `risk_scores`
- `suspicious_segments`
- `tool_logs`
- `report_summary`

`validation` 和 `fallback` 作为增强展示：

- 如果存在，显式显示 schema 校验、warnings、fallback reason、degraded fields
- 如果不存在，页面按非强依赖降级渲染

## 状态覆盖

工作台包含以下状态：

- `idle`
- `loading`
- `success`
- `empty`
- `error`

并能对应展示：

- `queued`
- `processing`
- `completed`
- `degraded`
- `failed`

## P0 演示建议

推荐录屏顺序：

1. 先开首页，说明这不是聊天 UI。
2. 进入 `/workspace?mode=demo`，展示任务状态推进。
3. 展示风险卡片、事件列表、可疑时间段、工具日志、报告摘要。
4. 指出 Harness 三件套区域：
   - Context Management
   - Tool Use
   - Feedback Loop
5. 点击 `Empty State` 和 `Error State`，展示降级与失败处理。
6. 回到上传区，说明 live API 路径已经按合同接好。

## 文件组织

- `app/`
  - App Router 页面与前端代理路由
- `components/home/`
  - 首页模块
- `components/workspace/`
  - 工作台模块
- `components/ui/`
  - 通用 UI
- `lib/types.ts`
  - 合同类型定义
- `lib/sample-data.ts`
  - sample/mock 数据
- `lib/api.ts`
  - 浏览器侧 API client
- `lib/server-api.ts`
  - 服务端代理层

## 当前限制

- 上传仍为文件名占位，不含真实文件流。
- 结果主要由 sample/mock 驱动，真实 pipeline 仍未接入。
- 报告摘要当前以 markdown 预览形式展示，未做导出。
- 未接入真实视频播放器或片段回放。

## 验证命令

```bash
cd frontend
npx tsc --noEmit
npm run lint
npm run build
```
