"use client";

import { useState } from "react";

import { Panel } from "@/components/ui/panel";

interface ControlPanelProps {
  mode: "demo" | "live";
  selectedFileName: string;
  isPolling: boolean;
  onDemo: () => Promise<void>;
  onLive: (fileName: string) => Promise<void>;
  onEmpty: () => void;
  onError: () => void;
}

export function ControlPanel({
  mode,
  selectedFileName,
  isPolling,
  onDemo,
  onLive,
  onEmpty,
  onError,
}: ControlPanelProps) {
  const [fileName, setFileName] = useState(selectedFileName || "team-sync.mp4");

  return (
    <Panel eyebrow="Start Analysis" title="上传与开始分析区">
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-3xl border border-line/15 bg-sand/25 p-5">
            <p className="text-sm font-semibold text-ink">Local Upload</p>
            <p className="mt-2 text-sm leading-6 text-line">
              Phase 1 先用文件名占位模拟上传，请求体严格对齐 `filename`、`content_type`、`source`。
            </p>
            <label className="mt-4 block">
              <span className="mb-2 block text-xs font-semibold uppercase tracking-[0.24em] text-line">
                Filename
              </span>
              <input
                value={fileName}
                onChange={(event) => setFileName(event.target.value)}
                className="w-full rounded-2xl border border-line/20 bg-white px-4 py-3 outline-none transition focus:border-rust"
                placeholder="team-sync.mp4"
              />
            </label>
            <button
              type="button"
              onClick={() => void onLive(fileName || "team-sync.mp4")}
              disabled={isPolling}
              className="mt-4 rounded-full bg-ink px-5 py-3 text-sm font-semibold text-white transition hover:bg-ink/90 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isPolling && mode === "live" ? "分析进行中..." : "上传并开始分析"}
            </button>
          </div>
          <div className="rounded-3xl border border-line/15 bg-white p-5">
            <p className="text-sm font-semibold text-ink">Demo Sample</p>
            <p className="mt-2 text-sm leading-6 text-line">
              直接进入完整结果页，适合录屏和课堂展示。不会跳到聊天界面，直接复现任务状态与结果面板。
            </p>
            <button
              type="button"
              onClick={() => void onDemo()}
              disabled={isPolling && mode === "demo"}
              className="mt-4 rounded-full bg-rust px-5 py-3 text-sm font-semibold text-white transition hover:bg-rust/90 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isPolling && mode === "demo" ? "加载 Demo 中..." : "进入 Demo 模式"}
            </button>
          </div>
        </div>

        <div className="rounded-3xl border border-line/15 bg-ink p-5 text-white">
          <p className="text-sm font-semibold">状态态检查</p>
          <p className="mt-2 text-sm leading-6 text-white/80">
            为了保证 P0 页面可演示，这里保留 empty / error 快速入口，便于验证降级和失败反馈是否可见。
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            <button
              type="button"
              onClick={onEmpty}
              className="rounded-full border border-white/20 px-4 py-2 text-sm font-semibold text-white/90 transition hover:border-white/40 hover:text-white"
            >
              查看 Empty State
            </button>
            <button
              type="button"
              onClick={onError}
              className="rounded-full border border-white/20 px-4 py-2 text-sm font-semibold text-white/90 transition hover:border-white/40 hover:text-white"
            >
              查看 Error State
            </button>
          </div>
        </div>
      </div>
    </Panel>
  );
}
