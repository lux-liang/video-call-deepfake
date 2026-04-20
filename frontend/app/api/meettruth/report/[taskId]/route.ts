import { proxyToMeetTruth } from "@/lib/server-api";

export async function GET(
  _request: Request,
  context: { params: Promise<{ taskId: string }> },
): Promise<Response> {
  const { taskId } = await context.params;

  return proxyToMeetTruth(`/api/report/${taskId}`);
}
