import { Panel } from "@/components/ui/panel";

const cards = [
  {
    title: "演示闭环",
    body: "上传会议视频或直接进入 demo，看到任务状态，再进入结果主控制台。",
  },
  {
    title: "结构化结果",
    body: "风险卡片、事件列表、可疑时间段、工具日志、报告摘要同时存在于同一工作台。",
  },
  {
    title: "非聊天产品",
    body: "这里不承载开放式问答，不把关键结果藏进对话历史，而是按巡检任务组织信息架构。",
  },
];

export function PositioningGrid() {
  return (
    <Panel eyebrow="Product Framing" title="为什么它是巡检控制台">
      <div className="grid gap-4 md:grid-cols-3">
        {cards.map((card) => (
          <article key={card.title} className="rounded-3xl border border-line/20 bg-sand/25 p-5">
            <h3 className="text-lg font-semibold text-ink">{card.title}</h3>
            <p className="mt-3 text-sm leading-6 text-line">{card.body}</p>
          </article>
        ))}
      </div>
    </Panel>
  );
}
