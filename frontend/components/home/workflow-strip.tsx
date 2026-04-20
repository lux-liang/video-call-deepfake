const steps = [
  "1. Upload video or enter demo mode",
  "2. Track ingestion / parsing / event extraction progress",
  "3. Review participants, events, suspicious segments, tool logs",
  "4. Export report summary and route to manual review",
];

export function WorkflowStrip() {
  return (
    <section className="grid gap-3 md:grid-cols-4">
      {steps.map((step) => (
        <div key={step} className="rounded-3xl border border-line/15 bg-white/65 px-5 py-4 shadow-panel">
          <p className="text-sm font-medium leading-6 text-ink">{step}</p>
        </div>
      ))}
    </section>
  );
}
