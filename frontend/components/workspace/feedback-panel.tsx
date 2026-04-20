import { Badge } from "@/components/ui/badge";
import { Panel } from "@/components/ui/panel";
import { formatConfidence } from "@/lib/format";
import type { AnalysisResult } from "@/lib/types";

interface FeedbackPanelProps {
  result: AnalysisResult;
}

export function FeedbackPanel({ result }: FeedbackPanelProps) {
  const validation = result.validation;
  const fallback = result.fallback;
  const lowConfidenceResponses = result.responses.filter((response) => response.confidence < 0.6);

  return (
    <Panel eyebrow="Harness Visualization" title="Context / Tool / Feedback Loop">
      <div className="grid gap-4 xl:grid-cols-3">
        <article className="rounded-3xl border border-line/15 bg-sand/20 p-5">
          <p className="text-xs uppercase tracking-[0.24em] text-line">Context Management</p>
          <p className="mt-3 text-sm leading-6 text-ink">
            已解析为 {result.participants.length} 个 `participants`、{result.events.length} 条 `events`、{result.responses.length} 条
            `responses`。
          </p>
          <p className="mt-3 text-sm leading-6 text-line">
            页面展示的是结构化上下文，不是整段视频直接交给 LLM 后吐出的自由文本。
          </p>
        </article>

        <article className="rounded-3xl border border-line/15 bg-sand/20 p-5">
          <p className="text-xs uppercase tracking-[0.24em] text-line">Tool Use</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {result.tool_logs.map((log) => (
              <Badge key={`${log.tool_name}-${log.started_at}`} value={log.status} variant="status" />
            ))}
          </div>
          <p className="mt-3 text-sm leading-6 text-line">
            显式暴露 `tool_logs`，记录外部工具是否成功、mocked、failed 以及对应 artifacts。
          </p>
        </article>

        <article className="rounded-3xl border border-line/15 bg-sand/20 p-5">
          <p className="text-xs uppercase tracking-[0.24em] text-line">Feedback Loop</p>
          <div className="mt-3 space-y-2 text-sm leading-6 text-ink">
            <p>Schema valid: {validation ? String(validation.schema_valid) : "unknown"}</p>
            <p>Low-confidence responses: {lowConfidenceResponses.length}</p>
            <p>Fallback mode: {fallback?.mode ?? "none"}</p>
            <p>Global confidence: {formatConfidence(result.confidence)}</p>
          </div>
        </article>
      </div>

      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <div className="rounded-3xl border border-line/15 bg-white p-5">
          <p className="text-sm font-semibold text-ink">Validation</p>
          {validation ? (
            <div className="mt-3 space-y-2 text-sm leading-6 text-line">
              <p>Validator version: {validation.validator_version}</p>
              <p>Missing fields: {validation.missing_fields.length === 0 ? "none" : validation.missing_fields.join(", ")}</p>
              <p>Warnings: {validation.warnings.length === 0 ? "none" : validation.warnings.join(" | ")}</p>
            </div>
          ) : (
            <p className="mt-3 text-sm leading-6 text-line">当前结果未提供 validation 区块，页面按非强依赖降级展示。</p>
          )}
        </div>
        <div className="rounded-3xl border border-line/15 bg-white p-5">
          <p className="text-sm font-semibold text-ink">Fallback / Degraded</p>
          {fallback ? (
            <div className="mt-3 space-y-2 text-sm leading-6 text-line">
              <p>Mode: {fallback.mode}</p>
              <p>Reason: {fallback.reason}</p>
              <p>Degraded fields: {fallback.degraded_fields.length === 0 ? "none" : fallback.degraded_fields.join(", ")}</p>
              <p>Used sample: {String(fallback.used_sample)}</p>
            </div>
          ) : (
            <p className="mt-3 text-sm leading-6 text-line">当前结果未声明 fallback 块，按正式结果路径处理。</p>
          )}
        </div>
      </div>
    </Panel>
  );
}
