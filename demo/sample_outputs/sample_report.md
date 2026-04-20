# MeetTruth Agent Sample Report

## Summary

Meeting `meeting_demo_001` completed with `degraded` status in a deterministic mock-to-real bootstrap mode. The pipeline concentrated risk on participant `Alice`, specifically around direct named responses rather than across the full meeting.

## Key Findings

- `11.8s` to `17.0s`: a speaker switch into Alice's named response showed elevated response latency and visible mouth-onset lag.
- `88.4s` to `91.0s`: Alice's second named response included an abrupt head pose change before speech onset.
- `58.0s` to `60.5s`: a screen-share change was detected, but it did not materially raise participant risk.
- `Bob` remained low risk with stable turn-taking behavior.

## Interpretation

This sample result is suitable for frontend playback because it includes stable participant cards, event timeline items, suspicious segments, structured responses, risk scores, tool logs, and report summary fields. Confidence remains below a full real-pipeline run because behavior features were derived from heuristics instead of actual landmark extraction.

## Recommendation

- Route Alice's flagged segments to manual review.
- Compare the flagged named-response windows against trusted identity reference footage.
- Re-run the same meeting with a real input video path when frame and landmark extraction are available.
