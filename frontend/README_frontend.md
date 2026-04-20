# Frontend Bootstrap

## 当前策略

Phase 1 先建立前端目录、页面结构和数据消费约束，不让完整 Next.js 初始化阻塞仓库 bootstrap。

## 推荐技术栈

- Next.js App Router
- TypeScript
- Tailwind CSS
- React Query 或原生 fetch 轮询

## 推荐页面结构

- `/`
  - 产品简介
  - demo 入口
- `/workspace`
  - 上传区
  - 任务状态
  - 风险卡片
  - 事件列表
  - 可疑时间段
  - 工具日志面板
  - 报告摘要

## 推荐后续初始化命令

```bash
cd frontend
npx create-next-app@latest . --ts --app --eslint
```

## Phase 1 约束

- 不做聊天框主界面。
- 只消费合同中声明的稳定字段。
- 先跑通 sample/mock 数据展示。
