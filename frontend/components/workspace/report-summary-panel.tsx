import { Panel } from "@/components/ui/panel";
import type { ReportResponse, ReportSummary } from "@/lib/types";

interface ReportSummaryPanelProps {
  reportSummary: ReportSummary;
  report: ReportResponse | null;
}

export function ReportSummaryPanel({ reportSummary, report }: ReportSummaryPanelProps) {
  return (
    <Panel eyebrow="Report" title="报告摘要区">
      <div className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
        <article className="rounded-3xl border border-line/15 bg-sand/20 p-5">
          <p className="text-xs uppercase tracking-[0.24em] text-line">Headline</p>
          <h3 className="mt-3 text-2xl font-semibold tracking-tight text-ink">{reportSummary.headline}</h3>
          <p className="mt-4 text-sm leading-7 text-ink">{reportSummary.overview}</p>
          <div className="mt-5 space-y-3">
            {reportSummary.recommended_actions.map((action) => (
              <div key={action} className="rounded-2xl border border-line/10 bg-white/70 px-4 py-3 text-sm text-ink">
                {action}
              </div>
            ))}
          </div>
        </article>
        <article className="rounded-3xl border border-line/15 bg-white p-5">
          <p className="text-xs uppercase tracking-[0.24em] text-line">Report Markdown</p>
          <pre className="mt-4 overflow-x-auto whitespace-pre-wrap rounded-3xl bg-ink p-5 text-sm leading-7 text-sand">
            {report?.report_markdown ?? "Report not loaded"}
          </pre>
        </article>
      </div>
    </Panel>
  );
}
