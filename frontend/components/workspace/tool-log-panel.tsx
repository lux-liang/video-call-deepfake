import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { Panel } from "@/components/ui/panel";
import { formatDateTime, formatElapsedSeconds } from "@/lib/format";
import type { AnalysisResult } from "@/lib/types";

interface ToolLogPanelProps {
  result: AnalysisResult;
}

export function ToolLogPanel({ result }: ToolLogPanelProps) {
  return (
    <Panel eyebrow="Tool Use" title="工具调用日志区">
      {result.tool_logs.length === 0 ? (
        <EmptyState title="当前没有工具日志" description="如果 backend 返回空数组，前端仍会保留日志面板位置。" />
      ) : (
        <div className="space-y-3">
          {result.tool_logs.map((log) => (
            <article key={`${log.tool_name}-${log.started_at}`} className="rounded-3xl border border-line/15 bg-white p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="text-lg font-semibold text-ink">{log.tool_name}</h3>
                    <Badge value={log.status} variant="status" />
                  </div>
                  <p className="mt-2 text-sm text-line">
                    {formatDateTime(log.started_at)} to {formatDateTime(log.ended_at)} · Duration{" "}
                    {formatElapsedSeconds(log.started_at, log.ended_at)}
                  </p>
                </div>
              </div>
              <p className="mt-4 text-sm leading-6 text-ink">{log.summary}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {log.artifacts.length > 0 ? (
                  log.artifacts.map((artifact) => (
                    <span key={artifact} className="rounded-full border border-line/15 bg-sand/25 px-3 py-1 text-xs font-medium text-line">
                      {artifact}
                    </span>
                  ))
                ) : (
                  <span className="rounded-full border border-dashed border-line/20 px-3 py-1 text-xs font-medium text-line">
                    No artifacts
                  </span>
                )}
              </div>
            </article>
          ))}
        </div>
      )}
    </Panel>
  );
}
