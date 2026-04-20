import type {
  AnalysisResult,
  AnalyzeRequest,
  AnalyzeResponse,
  ReportResponse,
  TaskStatusResponse,
  UploadRequest,
  UploadResponse,
} from "@/lib/types";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const payload = (await response.json()) as { error?: string; message?: string };
      message = payload.error ?? payload.message ?? message;
    } catch {
      message = message;
    }

    throw new Error(message);
  }

  return (await response.json()) as T;
}

export function uploadVideo(payload: UploadRequest): Promise<UploadResponse> {
  return request<UploadResponse>("/api/meettruth/upload", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function analyzeVideo(payload: AnalyzeRequest): Promise<AnalyzeResponse> {
  return request<AnalyzeResponse>("/api/meettruth/analyze", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchTask(taskId: string): Promise<TaskStatusResponse> {
  return request<TaskStatusResponse>(`/api/meettruth/task/${taskId}`);
}

export function fetchResult(taskId: string): Promise<AnalysisResult> {
  return request<AnalysisResult>(`/api/meettruth/result/${taskId}`);
}

export function fetchReport(taskId: string): Promise<ReportResponse> {
  return request<ReportResponse>(`/api/meettruth/report/${taskId}`);
}

export function fetchDemoSampleResult(): Promise<AnalysisResult> {
  return request<AnalysisResult>("/api/meettruth/demo-sample");
}
