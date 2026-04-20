import { EmptyState } from "@/components/ui/empty-state";
import { Panel } from "@/components/ui/panel";
import { formatConfidence, formatSeconds } from "@/lib/format";
import type { AnalysisResult, Participant } from "@/lib/types";

interface SegmentTimelinePanelProps {
  result: AnalysisResult;
  participantMap: Map<string, Participant>;
}

export function SegmentTimelinePanel({ result, participantMap }: SegmentTimelinePanelProps) {
  return (
    <Panel eyebrow="Suspicious Timeline" title="可疑时间段 / 时间轴区">
      {result.suspicious_segments.length === 0 ? (
        <EmptyState title="当前没有可疑时间段" description="无 `suspicious_segments[]` 时，这里保持空面板而非隐藏。" />
      ) : (
        <div className="space-y-4">
          {result.suspicious_segments.map((segment) => (
            <article key={segment.segment_id} className="rounded-3xl border border-line/15 bg-sand/20 p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h3 className="text-lg font-semibold text-ink">
                    {formatSeconds(segment.timestamp_start)} to {formatSeconds(segment.timestamp_end)}
                  </h3>
                  <p className="mt-2 text-sm text-line">
                    Participants:{" "}
                    {segment.participant_ids
                      .map((participantId) => participantMap.get(participantId)?.display_name ?? participantId)
                      .join(", ")}
                  </p>
                </div>
                <div className="rounded-full bg-white px-4 py-2 text-sm font-semibold text-ink">
                  Confidence {formatConfidence(segment.confidence)}
                </div>
              </div>
              <p className="mt-4 text-sm leading-6 text-ink">{segment.reason}</p>
              <div className="mt-4 h-3 w-full overflow-hidden rounded-full bg-white">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-rust to-teal"
                  style={{
                    width: `${Math.max(12, Math.min(100, (segment.timestamp_end - segment.timestamp_start) * 4))}%`,
                  }}
                />
              </div>
            </article>
          ))}
        </div>
      )}
    </Panel>
  );
}
