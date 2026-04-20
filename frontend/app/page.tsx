import { Hero } from "@/components/home/hero";
import { PositioningGrid } from "@/components/home/positioning-grid";
import { WorkflowStrip } from "@/components/home/workflow-strip";

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-8 px-4 py-6 md:px-6 md:py-8">
      <Hero />
      <WorkflowStrip />
      <PositioningGrid />
    </main>
  );
}
