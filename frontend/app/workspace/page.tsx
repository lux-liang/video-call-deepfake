import { DashboardShell } from "@/components/workspace/dashboard-shell";

export default async function WorkspacePage({
  searchParams,
}: {
  searchParams: Promise<{ mode?: string }>;
}) {
  const params = await searchParams;
  const initialMode = params.mode === "demo" ? "demo" : "live";

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-8 px-4 py-6 md:px-6 md:py-8">
      <DashboardShell initialMode={initialMode} />
    </main>
  );
}
