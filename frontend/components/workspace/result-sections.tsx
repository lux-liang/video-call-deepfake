import { EventListPanel } from "@/components/workspace/event-list-panel";
import { RiskCardGrid } from "@/components/workspace/risk-card-grid";
import { SegmentTimelinePanel } from "@/components/workspace/segment-timeline-panel";
import { ToolLogPanel } from "@/components/workspace/tool-log-panel";
import type { AnalysisResult, Participant } from "@/lib/types";

interface ResultSectionsProps {
  result: AnalysisResult;
  participantMap: Map<string, Participant>;
}

export function ResultSections({ result, participantMap }: ResultSectionsProps) {
  return (
    <div className="grid gap-6">
      <RiskCardGrid result={result} />
      <div className="grid gap-6 xl:grid-cols-2">
        <EventListPanel result={result} participantMap={participantMap} />
        <SegmentTimelinePanel result={result} participantMap={participantMap} />
      </div>
      <ToolLogPanel result={result} />
    </div>
  );
}
