from __future__ import annotations

from app.schemas.analysis import AnalysisResult, TaskStatus


class ReportService:
    def build_report(self, *, task_id: str, result: AnalysisResult) -> str:
        participant_lines = [
            f"- `{participant.display_name}` ({participant.role}) risk `{participant.dominant_risk_level}`: {participant.notes}"
            for participant in result.participants
        ] or ["- No participant-level findings were available."]

        event_lines = [
            f"- `{event.event_type}` for `{event.participant_id}` from `{event.timestamp_start:.1f}s` to `{event.timestamp_end:.1f}s`: {event.summary}"
            for event in result.events
        ] or ["- No event evidence was produced."]

        recommendation_lines = [
            f"- {action}"
            for action in result.report_summary.recommended_actions
        ] or ["- Keep the result under manual review until stronger evidence is available."]

        warnings = [
            f"- {warning}"
            for warning in result.validation.warnings
        ] or ["- No validation warnings."]

        fallback_note = (
            f"Fallback mode `{result.fallback.mode}` was applied because {result.fallback.reason}."
            if result.fallback.reason
            else "No fallback path was used."
        )

        sections = [
            "# MeetTruth Agent Report",
            "",
            "## Summary",
            "",
            f"Task `{task_id}` for meeting `{result.meeting_id}` finished with status `{result.status}` and confidence `{result.confidence:.2f}`.",
            f"{result.report_summary.overview}",
            fallback_note,
            "",
            "## Participants",
            "",
            *participant_lines,
            "",
            "## Key Findings",
            "",
            *event_lines,
            "",
            "## Validation",
            "",
            *warnings,
            "",
            "## Recommendation",
            "",
            *recommendation_lines,
        ]
        return "\n".join(sections)

    def build_pending_report(self, *, task_id: str, meeting_id: str, status: TaskStatus) -> str:
        return "\n".join(
            [
                "# MeetTruth Agent Report",
                "",
                "## Summary",
                "",
                f"Task `{task_id}` for meeting `{meeting_id}` is currently `{status}`.",
                f"The analysis result is not finalized yet. Poll `/api/task/{task_id}` and retry `/api/report/{task_id}` after completion.",
            ]
        )
