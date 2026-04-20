import type { AnalysisResult, ReportResponse, TaskStatusResponse } from "@/lib/types";

export const sampleAnalysisResult: AnalysisResult = {
  meeting_id: "meeting_demo_001",
  status: "completed",
  confidence: 0.78,
  participants: [
    {
      participant_id: "p_001",
      display_name: "Alice",
      role: "host",
      dominant_risk_level: "high",
      notes: "Repeated lip-sync mismatch around speaking turns.",
    },
    {
      participant_id: "p_002",
      display_name: "Bob",
      role: "guest",
      dominant_risk_level: "low",
      notes: "No high-severity anomaly cluster detected.",
    },
  ],
  events: [
    {
      event_id: "evt_001",
      participant_id: "p_001",
      timestamp_start: 42.5,
      timestamp_end: 49,
      event_type: "lip_sync_mismatch",
      severity: "high",
      summary: "Visible mouth motion diverges from detected speech.",
      evidence_refs: ["frame:001240", "audio:seg_014"],
    },
    {
      event_id: "evt_002",
      participant_id: "p_001",
      timestamp_start: 120,
      timestamp_end: 128,
      event_type: "face_boundary_instability",
      severity: "medium",
      summary: "Face boundary jitter increases during head turns.",
      evidence_refs: ["frame:003100"],
    },
  ],
  responses: [
    {
      response_id: "resp_001",
      kind: "explanation",
      source: "mock_rule_engine",
      summary: "Participant p_001 shows clustered multimodal inconsistencies.",
      confidence: 0.74,
    },
    {
      response_id: "resp_002",
      kind: "fallback_notice",
      source: "phase1_bootstrap",
      summary: "Result generated from sample/mock pipeline output.",
      confidence: 0.55,
    },
  ],
  risk_scores: [
    {
      participant_id: "p_001",
      score: 0.81,
      level: "high",
      reasons: ["multiple lip-sync mismatches", "face boundary instability"],
    },
    {
      participant_id: "p_002",
      score: 0.18,
      level: "low",
      reasons: ["no sustained anomaly cluster"],
    },
  ],
  suspicious_segments: [
    {
      segment_id: "seg_001",
      timestamp_start: 42.5,
      timestamp_end: 61,
      participant_ids: ["p_001"],
      reason: "Clustered audio-visual inconsistency around active speech.",
      confidence: 0.79,
    },
  ],
  tool_logs: [
    {
      tool_name: "ffmpeg",
      status: "success",
      started_at: "2026-04-20T00:00:00Z",
      ended_at: "2026-04-20T00:00:06Z",
      summary: "Extracted audio track and sampled frames.",
      artifacts: ["outputs/meeting_demo_001/audio.wav", "outputs/meeting_demo_001/frames/"],
    },
    {
      tool_name: "mediapipe",
      status: "mocked",
      started_at: "2026-04-20T00:00:06Z",
      ended_at: "2026-04-20T00:00:08Z",
      summary: "Phase 1 mock landmark pass for contract validation.",
      artifacts: [],
    },
  ],
  report_summary: {
    headline: "Alice flagged with elevated synthetic-behavior risk.",
    overview:
      "The sample analysis identified clustered lip-sync mismatch and face boundary instability around Alice's speaking turns.",
    recommended_actions: [
      "Request manual reviewer confirmation.",
      "Compare with trusted identity reference footage.",
    ],
  },
  validation: {
    schema_valid: true,
    missing_fields: [],
    warnings: ["Sample/mock output used in Phase 1 bootstrap."],
    validator_version: "phase1",
  },
  fallback: {
    mode: "mock",
    reason: "Real pipeline not connected yet.",
    degraded_fields: [],
    used_sample: true,
  },
};

export const sampleCompletedTask: TaskStatusResponse = {
  task_id: "task_demo_001",
  meeting_id: "meeting_demo_001",
  status: "completed",
  progress: 100,
  stage: "reporting",
  confidence: 0.78,
  error: null,
};

export const sampleTaskSequence: TaskStatusResponse[] = [
  {
    task_id: "task_demo_001",
    meeting_id: "meeting_demo_001",
    status: "queued",
    progress: 12,
    stage: "ingestion",
    confidence: 0.24,
    error: null,
  },
  {
    task_id: "task_demo_001",
    meeting_id: "meeting_demo_001",
    status: "processing",
    progress: 46,
    stage: "parsing",
    confidence: 0.48,
    error: null,
  },
  {
    task_id: "task_demo_001",
    meeting_id: "meeting_demo_001",
    status: "processing",
    progress: 77,
    stage: "event_extraction",
    confidence: 0.65,
    error: null,
  },
  sampleCompletedTask,
];

export const sampleReport: ReportResponse = {
  task_id: "task_demo_001",
  meeting_id: "meeting_demo_001",
  status: "completed",
  generated_at: "2026-04-20T00:00:00Z",
  report_markdown: `# MeetTruth Agent Sample Report

## Summary

Meeting \`meeting_demo_001\` completed in mock playback mode. The system flagged participant \`Alice\` as elevated risk based on clustered visual-audio inconsistency signals.

## Key Findings

- High-severity lip-sync mismatch detected between \`42.5s\` and \`49.0s\`.
- Medium-severity face boundary instability detected between \`120.0s\` and \`128.0s\`.
- Participant \`Bob\` remained low risk in the sample result.

## Recommendation

- Route the meeting to manual review.
- Compare the flagged participant against trusted reference footage.
- Keep the current result marked as sample/mock until the real pipeline is connected.
`,
};
