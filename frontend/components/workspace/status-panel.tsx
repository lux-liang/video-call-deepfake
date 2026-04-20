import { Badge } from "@/components/ui/badge";
import { Panel } from "@/components/ui/panel";
import { ProgressBar } from "@/components/ui/progress-bar";
import { formatConfidence, toTitleLabel } from "@/lib/format";
import type { TaskStatusResponse, UploadResponse } from "@/lib/types";

interface StatusPanelProps {
  mode: "demo" | "live";
  uploadPayload: UploadResponse | null;
  status: TaskStatusResponse | null;
  errorMessage: string | null;
  viewState: "idle" | "loading" | "success" | "error" | "empty";
}

export function StatusPanel({
  mode,
  uploadPayload,
  status,
  errorMessage,
  viewState,
}: StatusPanelProps) {
  return (
    <Panel
      eyebrow="Task Progress"
      title="任务进度与分析状态"
      action={
        <span className="rounded-full bg-sand/50 px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-line">
          {mode === "demo" ? "demo pipeline" : "live api path"}
        </span>
      }
    >
      <div className="space-y-5">
        <div className="grid gap-4 sm:grid-cols-3">
          <MetricCard label="Current View" value={toTitleLabel(viewState)} />
          <MetricCard label="Task Status" value={status ? toTitleLabel(status.status) : "Not started"} />
          <MetricCard label="Confidence" value={status ? formatConfidence(status.confidence) : "N/A"} />
        </div>

        {status ? (
          <div className="rounded-3xl border border-line/15 bg-sand/20 p-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-xs uppercase tracking-[0.24em] text-line">Pipeline Stage</p>
                <p className="mt-2 text-2xl font-semibold text-ink">{toTitleLabel(status.stage)}</p>
              </div>
              <Badge value={status.status} variant="status" />
            </div>
            <div className="mt-4">
              <ProgressBar value={status.progress} />
            </div>
            <div className="mt-3 flex flex-wrap gap-4 text-sm text-line">
              <span>Progress {status.progress}%</span>
              <span>Task ID {status.task_id}</span>
              <span>Meeting ID {status.meeting_id}</span>
            </div>
          </div>
        ) : (
          <div className="rounded-3xl border border-dashed border-line/25 bg-sand/10 p-5 text-sm text-line">
            还没有创建任务。可直接进入 demo，或输入文件名后从上传流程启动。
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-3xl border border-line/15 bg-white p-5">
            <p className="text-xs uppercase tracking-[0.24em] text-line">Upload Payload</p>
            <div className="mt-3 space-y-2 text-sm text-ink">
              <p>Task: {uploadPayload?.task_id ?? "N/A"}</p>
              <p>Meeting: {uploadPayload?.meeting_id ?? "N/A"}</p>
              <p>Upload: {uploadPayload?.upload_id ?? "N/A"}</p>
            </div>
          </div>
          <div className="rounded-3xl border border-line/15 bg-white p-5">
            <p className="text-xs uppercase tracking-[0.24em] text-line">Error Channel</p>
            <p className="mt-3 text-sm leading-6 text-ink">
              {errorMessage ?? "No blocking error. If backend is unavailable, this panel surfaces the API failure."}
            </p>
          </div>
        </div>
      </div>
    </Panel>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-3xl border border-line/15 bg-white p-4">
      <p className="text-xs uppercase tracking-[0.24em] text-line">{label}</p>
      <p className="mt-2 text-xl font-semibold text-ink">{value}</p>
    </div>
  );
}
