import { Panel } from "@/components/ui/panel";
import { formatConfidence } from "@/lib/format";
import type { AnalysisResult, Participant, TaskStatusResponse } from "@/lib/types";

interface OverviewStripProps {
  result: AnalysisResult;
  status: TaskStatusResponse;
  participantMap: Map<string, Participant>;
}

export function OverviewStrip({ result, status }: OverviewStripProps) {
  const highRiskCount = result.risk_scores.filter((score) => score.level === "high").length;

  return (
    <Panel eyebrow="Result Summary" title="主控制台概览">
      <div className="grid gap-4 md:grid-cols-4">
        <StatBlock label="Meeting" value={result.meeting_id} />
        <StatBlock label="Participants" value={String(result.participants.length)} />
        <StatBlock label="High Risk" value={String(highRiskCount)} />
        <StatBlock label="Task Confidence" value={formatConfidence(status.confidence)} />
      </div>
    </Panel>
  );
}

function StatBlock({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-3xl border border-line/15 bg-sand/20 p-5">
      <p className="text-xs uppercase tracking-[0.24em] text-line">{label}</p>
      <p className="mt-2 break-all text-xl font-semibold text-ink">{value}</p>
    </div>
  );
}
