import { cn, toTitleLabel } from "@/lib/format";

interface BadgeProps {
  value: string;
  variant?: "risk" | "status" | "neutral";
}

const riskStyles: Record<string, string> = {
  high: "bg-red-100 text-red-700 border-red-200",
  medium: "bg-amber-100 text-amber-700 border-amber-200",
  low: "bg-emerald-100 text-emerald-700 border-emerald-200",
};

const statusStyles: Record<string, string> = {
  success: "bg-emerald-100 text-emerald-700 border-emerald-200",
  completed: "bg-emerald-100 text-emerald-700 border-emerald-200",
  processing: "bg-sky-100 text-sky-700 border-sky-200",
  queued: "bg-stone-100 text-stone-700 border-stone-200",
  mocked: "bg-amber-100 text-amber-700 border-amber-200",
  degraded: "bg-amber-100 text-amber-700 border-amber-200",
  partial_success: "bg-amber-100 text-amber-700 border-amber-200",
  failed: "bg-red-100 text-red-700 border-red-200",
};

export function Badge({ value, variant = "neutral" }: BadgeProps) {
  const style =
    variant === "risk"
      ? riskStyles[value] ?? "bg-stone-100 text-stone-700 border-stone-200"
      : variant === "status"
        ? statusStyles[value] ?? "bg-stone-100 text-stone-700 border-stone-200"
        : "bg-stone-100 text-stone-700 border-stone-200";

  return (
    <span className={cn("inline-flex rounded-full border px-3 py-1 text-xs font-semibold", style)}>
      {toTitleLabel(value)}
    </span>
  );
}
