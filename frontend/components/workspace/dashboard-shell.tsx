"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import { ControlPanel } from "@/components/workspace/control-panel";
import { DashboardHeader } from "@/components/workspace/dashboard-header";
import { EmptyWorkspace } from "@/components/workspace/empty-workspace";
import { FeedbackPanel } from "@/components/workspace/feedback-panel";
import { OverviewStrip } from "@/components/workspace/overview-strip";
import { ReportSummaryPanel } from "@/components/workspace/report-summary-panel";
import { ResultSections } from "@/components/workspace/result-sections";
import { StatusPanel } from "@/components/workspace/status-panel";
import { fetchReport, fetchResult, fetchTask } from "@/lib/api";
import { sampleAnalysisResult, sampleCompletedTask, sampleReport, sampleTaskSequence } from "@/lib/sample-data";
import type { AnalysisResult, ReportResponse, TaskStatusResponse, TaskStatus, UploadResponse } from "@/lib/types";

type WorkspaceMode = "demo" | "live";
type ViewState = "idle" | "loading" | "success" | "error" | "empty";

interface DashboardShellProps {
  initialMode: WorkspaceMode;
}

export function DashboardShell({ initialMode }: DashboardShellProps) {
  const [mode, setMode] = useState<WorkspaceMode>(initialMode);
  const [viewState, setViewState] = useState<ViewState>(initialMode === "demo" ? "loading" : "idle");
  const [status, setStatus] = useState<TaskStatusResponse | null>(initialMode === "demo" ? sampleTaskSequence[0] : null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [uploadPayload, setUploadPayload] = useState<UploadResponse | null>(null);
  const [selectedFileName, setSelectedFileName] = useState<string>("");
  const [isPolling, setIsPolling] = useState(false);
  const demoTimerRef = useRef<number | null>(null);

  useEffect(() => {
    if (initialMode === "demo") {
      void runDemoMode();
    }

    return () => {
      if (demoTimerRef.current) {
        window.clearTimeout(demoTimerRef.current);
      }
    };
  }, [initialMode]);

  const participantMap = useMemo(() => {
    return new Map((result?.participants ?? []).map((participant) => [participant.participant_id, participant]));
  }, [result?.participants]);

  async function runDemoMode(): Promise<void> {
    if (demoTimerRef.current) {
      window.clearTimeout(demoTimerRef.current);
    }

    setMode("demo");
    setViewState("loading");
    setIsPolling(true);
    setErrorMessage(null);
    setUploadPayload({
      task_id: sampleCompletedTask.task_id,
      meeting_id: sampleCompletedTask.meeting_id,
      upload_id: "upload_demo_001",
      status: "queued",
      message: "demo mode ready",
    });
    setSelectedFileName("demo_meeting_playback.mp4");
    setResult(null);
    setReport(null);

    sampleTaskSequence.forEach((entry, index) => {
      demoTimerRef.current = window.setTimeout(() => {
        setStatus(entry);
      }, index * 700);
    });

    demoTimerRef.current = window.setTimeout(() => {
      setStatus(sampleCompletedTask);
      setResult(sampleAnalysisResult);
      setReport(sampleReport);
      setViewState("success");
      setIsPolling(false);
    }, sampleTaskSequence.length * 700 + 300);
  }

  async function beginLiveAnalysis(fileName: string): Promise<void> {
    setMode("live");
    setSelectedFileName(fileName);
    setViewState("loading");
    setIsPolling(true);
    setErrorMessage(null);
    setResult(null);
    setReport(null);

    try {
      const uploadResponse = await fetch("/api/meettruth/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          filename: fileName,
          content_type: "video/mp4",
          source: "local_upload",
        }),
      }).then(async (response) => {
        if (!response.ok) {
          const payload = (await response.json().catch(() => ({}))) as { error?: string; message?: string };
          throw new Error(payload.error ?? payload.message ?? `Upload failed with ${response.status}`);
        }

        return (await response.json()) as UploadResponse;
      });

      setUploadPayload(uploadResponse);
      setStatus({
        task_id: uploadResponse.task_id,
        meeting_id: uploadResponse.meeting_id,
        status: uploadResponse.status,
        progress: 8,
        stage: "ingestion",
        confidence: 0.24,
        error: null,
      });

      const analyzeResponse = await fetch("/api/meettruth/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          meeting_id: uploadResponse.meeting_id,
          upload_id: uploadResponse.upload_id,
          mode: "playback_mock",
          use_mock: true,
        }),
      }).then(async (response) => {
        if (!response.ok) {
          const payload = (await response.json().catch(() => ({}))) as { error?: string; message?: string };
          throw new Error(payload.error ?? payload.message ?? `Analyze failed with ${response.status}`);
        }

        return (await response.json()) as { task_id: string; status: TaskStatus };
      });

      await pollTask(analyzeResponse.task_id);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error while starting analysis.";
      setErrorMessage(message);
      setViewState("error");
      setIsPolling(false);
    }
  }

  async function pollTask(taskId: string): Promise<void> {
    for (let attempt = 0; attempt < 8; attempt += 1) {
      const taskStatus = await fetchTask(taskId);
      setStatus(taskStatus);

      if (taskStatus.status === "completed" || taskStatus.status === "partial_success" || taskStatus.status === "degraded") {
        const [analysisResult, reportResult] = await Promise.all([fetchResult(taskId), fetchReport(taskId)]);
        setResult(analysisResult);
        setReport(reportResult);
        setViewState(analysisResult.participants.length > 0 ? "success" : "empty");
        setIsPolling(false);
        return;
      }

      if (taskStatus.status === "failed") {
        setErrorMessage(taskStatus.error ?? "Task failed");
        setViewState("error");
        setIsPolling(false);
        return;
      }

      await new Promise((resolve) => {
        window.setTimeout(resolve, 900);
      });
    }

    setErrorMessage("Polling timed out before the backend returned a final task state.");
    setViewState("error");
    setIsPolling(false);
  }

  function enterErrorState(): void {
    setMode("live");
    setViewState("error");
    setIsPolling(false);
    setStatus({
      task_id: "task_error_001",
      meeting_id: "meeting_error_001",
      status: "failed",
      progress: 39,
      stage: "event_extraction",
      confidence: 0.2,
      error: "Pipeline validation failed before result assembly.",
    });
    setErrorMessage("Pipeline validation failed before result assembly.");
    setResult(null);
    setReport(null);
  }

  function enterEmptyState(): void {
    setMode("live");
    setViewState("empty");
    setIsPolling(false);
    setStatus({
      task_id: "task_empty_001",
      meeting_id: "meeting_empty_001",
      status: "degraded",
      progress: 100,
      stage: "reporting",
      confidence: 0.31,
      error: null,
    });
    setUploadPayload({
      task_id: "task_empty_001",
      meeting_id: "meeting_empty_001",
      upload_id: "upload_empty_001",
      status: "queued",
      message: "upload accepted for empty_case.mp4",
    });
    setSelectedFileName("empty_case.mp4");
    setResult({
      ...sampleAnalysisResult,
      meeting_id: "meeting_empty_001",
      status: "degraded",
      confidence: 0.31,
      participants: [],
      events: [],
      risk_scores: [],
      suspicious_segments: [],
      tool_logs: [
        {
          tool_name: "ffmpeg",
          status: "success",
          started_at: "2026-04-20T03:00:00Z",
          ended_at: "2026-04-20T03:00:03Z",
          summary: "Input normalized successfully.",
          artifacts: ["outputs/meeting_empty_001/audio.wav"],
        },
        {
          tool_name: "mediapipe",
          status: "failed",
          started_at: "2026-04-20T03:00:03Z",
          ended_at: "2026-04-20T03:00:06Z",
          summary: "No stable face track detected in the sample input.",
          artifacts: [],
        },
      ],
      responses: [
        {
          response_id: "resp_empty_001",
          kind: "fallback_notice",
          source: "phase1_bootstrap",
          summary: "No participant-level output available, rendering degraded empty state.",
          confidence: 0.31,
        },
      ],
      report_summary: {
        headline: "No stable participant evidence was produced.",
        overview: "The task completed in degraded mode and returned no participant-level risk cards.",
        recommended_actions: ["Retry with a clearer playback segment.", "Review acquisition quality before rerun."],
      },
      validation: {
        schema_valid: true,
        missing_fields: [],
        warnings: ["Result is empty because participant extraction did not produce stable tracks."],
        validator_version: "phase1",
      },
      fallback: {
        mode: "mock",
        reason: "Participant extraction produced no stable entities.",
        degraded_fields: ["participants", "events", "risk_scores", "suspicious_segments"],
        used_sample: false,
      },
    });
    setReport({
      task_id: "task_empty_001",
      meeting_id: "meeting_empty_001",
      status: "degraded",
      generated_at: "2026-04-20T03:00:06Z",
      report_markdown: "# Empty Output\n\nNo stable participant evidence was returned for this playback sample.",
    });
    setErrorMessage(null);
  }

  return (
    <div className="space-y-8">
      <DashboardHeader />
      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <ControlPanel
          mode={mode}
          selectedFileName={selectedFileName}
          isPolling={isPolling}
          onDemo={runDemoMode}
          onLive={beginLiveAnalysis}
          onEmpty={enterEmptyState}
          onError={enterErrorState}
        />
        <StatusPanel
          mode={mode}
          uploadPayload={uploadPayload}
          status={status}
          errorMessage={errorMessage}
          viewState={viewState}
        />
      </div>

      {result && status ? (
        <>
          <OverviewStrip result={result} status={status} participantMap={participantMap} />
          <FeedbackPanel result={result} />
        </>
      ) : null}

      {viewState === "idle" ? <EmptyWorkspace /> : null}
      {viewState === "empty" && result && status ? (
        <>
          <EmptyWorkspace
            title="已完成，但没有可渲染的 participant 级结果"
            description="合同字段仍然完整返回，当前用 degraded 空结果展示 fallback 策略和工具日志。"
          />
          <FeedbackPanel result={result} />
        </>
      ) : null}
      {viewState === "error" ? (
        <EmptyWorkspace
          title="任务失败或后端不可达"
          description={errorMessage ?? "请确认 backend 已启动，或切回 demo 模式继续录屏演示。"}
        />
      ) : null}

      {viewState === "success" && result && status ? (
        <>
          <ResultSections result={result} participantMap={participantMap} />
          <ReportSummaryPanel reportSummary={result.report_summary} report={report} />
        </>
      ) : null}
    </div>
  );
}
