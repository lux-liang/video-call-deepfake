interface ProgressBarProps {
  value: number;
}

export function ProgressBar({ value }: ProgressBarProps) {
  const width = `${Math.min(100, Math.max(0, value))}%`;

  return (
    <div className="h-3 w-full overflow-hidden rounded-full bg-sand/80">
      <div
        className="h-full rounded-full bg-gradient-to-r from-rust via-rust/80 to-teal transition-all duration-500"
        style={{ width }}
      />
    </div>
  );
}
