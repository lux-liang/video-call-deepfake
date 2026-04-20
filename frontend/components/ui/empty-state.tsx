interface EmptyStateProps {
  title: string;
  description: string;
}

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="rounded-3xl border border-dashed border-line/30 bg-sand/30 px-5 py-8 text-center">
      <p className="text-lg font-semibold text-ink">{title}</p>
      <p className="mt-2 text-sm leading-6 text-line">{description}</p>
    </div>
  );
}
