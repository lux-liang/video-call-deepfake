import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { Panel } from "@/components/ui/panel";
import { formatConfidence } from "@/lib/format";
import type { AnalysisResult } from "@/lib/types";

interface RiskCardGridProps {
  result: AnalysisResult;
}

export function RiskCardGrid({ result }: RiskCardGridProps) {
  if (result.participants.length === 0) {
    return (
      <Panel eyebrow="Participants" title="参会者风险卡片区">
        <EmptyState
          title="暂无 participant 风险卡片"
          description="degraded 结果仍然保留合同顶层字段，但 participant 级数据为空。"
        />
      </Panel>
    );
  }

  return (
    <Panel eyebrow="Participants" title="参会者风险卡片区">
      <div className="grid gap-4 lg:grid-cols-2">
        {result.participants.map((participant) => {
          const score = result.risk_scores.find((item) => item.participant_id === participant.participant_id);

          return (
            <article key={participant.participant_id} className="rounded-3xl border border-line/15 bg-sand/20 p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h3 className="text-xl font-semibold text-ink">{participant.display_name}</h3>
                  <p className="mt-1 text-sm uppercase tracking-[0.2em] text-line">{participant.role}</p>
                </div>
                <Badge value={participant.dominant_risk_level} variant="risk" />
              </div>
              <div className="mt-5 grid gap-4 sm:grid-cols-2">
                <div className="rounded-2xl border border-line/10 bg-white/70 p-4">
                  <p className="text-xs uppercase tracking-[0.24em] text-line">Risk Score</p>
                  <p className="mt-2 text-2xl font-semibold text-ink">{score ? formatConfidence(score.score) : "N/A"}</p>
                </div>
                <div className="rounded-2xl border border-line/10 bg-white/70 p-4">
                  <p className="text-xs uppercase tracking-[0.24em] text-line">Primary Level</p>
                  <p className="mt-2 text-2xl font-semibold text-ink">{score?.level ?? participant.dominant_risk_level}</p>
                </div>
              </div>
              <p className="mt-5 text-sm leading-6 text-ink">{participant.notes}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {(score?.reasons ?? []).map((reason) => (
                  <span key={reason} className="rounded-full border border-line/15 bg-white px-3 py-1 text-xs font-medium text-line">
                    {reason}
                  </span>
                ))}
              </div>
            </article>
          );
        })}
      </div>
    </Panel>
  );
}
