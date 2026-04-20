import Link from "next/link";

export function Hero() {
  return (
    <section className="relative overflow-hidden rounded-[2.5rem] border border-line/15 bg-ink px-6 py-10 text-white shadow-panel md:px-10 md:py-12">
      <div className="absolute inset-0 bg-grid bg-[size:32px_32px] opacity-10" />
      <div className="absolute -right-16 top-8 h-48 w-48 rounded-full bg-rust/25 blur-3xl" />
      <div className="absolute left-0 top-0 h-44 w-44 rounded-full bg-teal/30 blur-3xl" />
      <div className="relative grid gap-10 lg:grid-cols-[1.15fr_0.85fr]">
        <div className="space-y-6">
          <p className="text-xs font-semibold uppercase tracking-[0.32em] text-sand">
            Meeting Authenticity Inspection Console
          </p>
          <div className="space-y-4">
            <h1 className="max-w-3xl text-4xl font-semibold tracking-tight md:text-6xl">
              会议真实性巡检控制台，不是上传视频后问 AI 的聊天页。
            </h1>
            <p className="max-w-2xl text-base leading-7 text-sand/90 md:text-lg">
              MeetTruth Agent 把会议回放解析为参与者、事件、响应和工具日志，再输出风险分数、可疑时间段与报告摘要，显式展示 Context
              Management、Tool Use、Feedback Loop。
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/workspace?mode=demo"
              className="rounded-full bg-rust px-6 py-3 text-sm font-semibold text-white transition hover:bg-rust/90"
            >
              进入 Demo 工作台
            </Link>
            <Link
              href="/workspace"
              className="rounded-full border border-white/25 px-6 py-3 text-sm font-semibold text-white/90 transition hover:border-white/40 hover:text-white"
            >
              打开上传与分析流程
            </Link>
          </div>
        </div>
        <div className="grid gap-4 rounded-[2rem] border border-white/10 bg-white/8 p-5 backdrop-blur">
          <div className="rounded-3xl border border-white/10 bg-white/5 p-4">
            <p className="text-xs uppercase tracking-[0.24em] text-sand/80">Context Management</p>
            <p className="mt-3 text-sm leading-6 text-white/85">
              会议不是整段视频黑盒输入，而是解析成 `participants`、`events`、`responses`、`risk_scores`。
            </p>
          </div>
          <div className="rounded-3xl border border-white/10 bg-white/5 p-4">
            <p className="text-xs uppercase tracking-[0.24em] text-sand/80">Tool Use</p>
            <p className="mt-3 text-sm leading-6 text-white/85">
              前端显式显示 `tool_logs`，让老师一眼看到 `ffmpeg`、`mediapipe`、规则引擎和 fallback 链路。
            </p>
          </div>
          <div className="rounded-3xl border border-white/10 bg-white/5 p-4">
            <p className="text-xs uppercase tracking-[0.24em] text-sand/80">Feedback Loop</p>
            <p className="mt-3 text-sm leading-6 text-white/85">
              校验结果、缺失字段、warnings、mock/fallback 和低置信度都独立可见，不把降级结果伪装成确定结论。
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
