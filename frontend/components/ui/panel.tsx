import type { ReactNode } from "react";

import { cn } from "@/lib/format";

interface PanelProps {
  title?: string;
  eyebrow?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function Panel({ title, eyebrow, action, children, className }: PanelProps) {
  return (
    <section
      className={cn(
        "rounded-4xl border border-line/20 bg-white/75 p-6 shadow-panel backdrop-blur md:p-8",
        className,
      )}
    >
      {(title || eyebrow || action) && (
        <div className="mb-5 flex flex-wrap items-start justify-between gap-3">
          <div className="space-y-2">
            {eyebrow ? (
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-rust">{eyebrow}</p>
            ) : null}
            {title ? <h2 className="text-2xl font-semibold tracking-tight text-ink">{title}</h2> : null}
          </div>
          {action ? <div>{action}</div> : null}
        </div>
      )}
      {children}
    </section>
  );
}
