export function DashboardHeader() {
  return (
    <header className="grid gap-5 rounded-[2rem] border border-line/15 bg-white/75 p-6 shadow-panel md:grid-cols-[1.2fr_0.8fr] md:p-8">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.28em] text-rust">Workspace</p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-ink md:text-4xl">
          Playback-first meeting inspection workflow
        </h1>
        <p className="mt-4 max-w-3xl text-sm leading-7 text-line md:text-base">
          工作台以任务状态和结果板块为中心组织，不做聊天入口。上传后先看解析与分析进度，再进入 participant 风险、事件证据、可疑时间段、工具日志和报告摘要。
        </p>
      </div>
      <div className="grid gap-3 rounded-[1.75rem] bg-sand/30 p-5">
        <div className="rounded-3xl border border-line/15 bg-white/60 p-4">
          <p className="text-xs uppercase tracking-[0.24em] text-line">Demo Goal</p>
          <p className="mt-2 text-sm leading-6 text-ink">支持 3 分钟录屏，显式呈现 Harness 三件套与 fallback 流程。</p>
        </div>
        <div className="rounded-3xl border border-line/15 bg-white/60 p-4">
          <p className="text-xs uppercase tracking-[0.24em] text-line">Contract Rule</p>
          <p className="mt-2 text-sm leading-6 text-ink">页面只消费合同字段，`validation` 和 `fallback` 作为增强可视化，有则展示，无则降级。</p>
        </div>
      </div>
    </header>
  );
}
