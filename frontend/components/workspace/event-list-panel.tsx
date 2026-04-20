import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { Panel } from "@/components/ui/panel";
import { formatSeconds, toTitleLabel } from "@/lib/format";
import type { AnalysisResult, Participant } from "@/lib/types";

interface EventListPanelProps {
  result: AnalysisResult;
  participantMap: Map<string, Participant>;
}

export function EventListPanel({ result, participantMap }: EventListPanelProps) {
  return (
    <Panel eyebrow="Evidence Events" title="事件列表区">
      {result.events.length === 0 ? (
        <EmptyState title="当前没有事件列表" description="没有 `events[]` 时，这里会显式保持空状态。" />
      ) : (
        <div className="space-y-3">
          {result.events.map((event) => (
            <article key={event.event_id} className="rounded-3xl border border-line/15 bg-white p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="text-lg font-semibold text-ink">{toTitleLabel(event.event_type)}</h3>
                    <Badge value={event.severity} variant="risk" />
                  </div>
                  <p className="mt-2 text-sm text-line">
                    {participantMap.get(event.participant_id)?.display_name ?? event.participant_id} · {formatSeconds(event.timestamp_start)} to{" "}
                    {formatSeconds(event.timestamp_end)}
                  </p>
                </div>
                <p className="text-xs uppercase tracking-[0.24em] text-line">{event.event_id}</p>
              </div>
              <p className="mt-4 text-sm leading-6 text-ink">{event.summary}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {event.evidence_refs.map((ref) => (
                  <span key={ref} className="rounded-full bg-sand/35 px-3 py-1 text-xs font-medium text-line">
                    {ref}
                  </span>
                ))}
              </div>
            </article>
          ))}
        </div>
      )}
    </Panel>
  );
}
