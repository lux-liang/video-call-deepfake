export type TaskStatus =
  | "queued"
  | "processing"
  | "completed"
  | "partial_success"
  | "degraded"
  | "failed";

export interface UploadRequest {
  filename: string;
  content_type: string;
  source: string;
}

export interface UploadResponse {
  task_id: string;
  meeting_id: string;
  upload_id: string;
  status: TaskStatus;
  message: string;
}

export interface AnalyzeRequest {
  meeting_id: string;
  upload_id: string;
  mode: string;
  use_mock: boolean;
}

export interface AnalyzeResponse {
  task_id: string;
  meeting_id: string;
  status: TaskStatus;
  estimated_mode: string;
}

export interface TaskStatusResponse {
  task_id: string;
  meeting_id: string;
  status: TaskStatus;
  progress: number;
  stage: string;
  confidence: number;
  error: string | null;
}

export interface Participant {
  participant_id: string;
  display_name: string;
  role: string;
  dominant_risk_level: string;
  notes: string;
}

export interface EventItem {
  event_id: string;
  participant_id: string;
  timestamp_start: number;
  timestamp_end: number;
  event_type: string;
  severity: string;
  summary: string;
  evidence_refs: string[];
}

export interface ResponseItem {
  response_id: string;
  kind: string;
  source: string;
  summary: string;
  confidence: number;
}

export interface RiskScore {
  participant_id: string;
  score: number;
  level: string;
  reasons: string[];
}

export interface SuspiciousSegment {
  segment_id: string;
  timestamp_start: number;
  timestamp_end: number;
  participant_ids: string[];
  reason: string;
  confidence: number;
}

export interface ToolLog {
  tool_name: string;
  status: string;
  started_at: string;
  ended_at: string;
  summary: string;
  artifacts: string[];
}

export interface ReportSummary {
  headline: string;
  overview: string;
  recommended_actions: string[];
}

export interface ValidationResult {
  schema_valid: boolean;
  missing_fields: string[];
  warnings: string[];
  validator_version: string;
}

export interface FallbackResult {
  mode: string;
  reason: string;
  degraded_fields: string[];
  used_sample: boolean;
}

export interface AnalysisResult {
  meeting_id: string;
  status: TaskStatus;
  confidence: number;
  participants: Participant[];
  events: EventItem[];
  responses: ResponseItem[];
  risk_scores: RiskScore[];
  suspicious_segments: SuspiciousSegment[];
  tool_logs: ToolLog[];
  report_summary: ReportSummary;
  validation?: ValidationResult;
  fallback?: FallbackResult;
}

export interface ReportResponse {
  task_id: string;
  meeting_id: string;
  status: TaskStatus;
  report_markdown: string;
  generated_at: string;
}
