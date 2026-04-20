import { Panel } from "@/components/ui/panel";

interface EmptyWorkspaceProps {
  title?: string;
  description?: string;
}

export function EmptyWorkspace({
  title = "工作台已就绪，等待任务启动",
  description = "你可以输入文件名模拟上传，或直接进入 demo 模式查看完整结构化结果。",
}: EmptyWorkspaceProps) {
  return (
    <Panel eyebrow="State" title={title}>
      <div className="rounded-3xl border border-dashed border-line/25 bg-sand/15 px-6 py-10">
        <p className="max-w-3xl text-sm leading-7 text-line">{description}</p>
      </div>
    </Panel>
  );
}
