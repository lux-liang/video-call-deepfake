export function cn(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export function formatConfidence(value?: number): string {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "N/A";
  }

  return `${Math.round(value * 100)}%`;
}

export function formatSeconds(value: number): string {
  const safeValue = Number.isFinite(value) ? Math.max(0, value) : 0;
  const minutes = Math.floor(safeValue / 60);
  const seconds = (safeValue % 60).toFixed(1).padStart(4, "0");

  return `${String(minutes).padStart(2, "0")}:${seconds}`;
}

export function formatDateTime(value: string): string {
  const parsed = new Date(value);

  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(parsed);
}

export function formatElapsedSeconds(startedAt: string, endedAt: string): string {
  const started = new Date(startedAt).getTime();
  const ended = new Date(endedAt).getTime();

  if (Number.isNaN(started) || Number.isNaN(ended) || ended < started) {
    return "N/A";
  }

  return `${((ended - started) / 1000).toFixed(1)}s`;
}

export function toTitleLabel(value: string): string {
  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}
