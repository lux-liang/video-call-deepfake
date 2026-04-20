import { proxyToMeetTruth } from "@/lib/server-api";

export async function GET(): Promise<Response> {
  return proxyToMeetTruth("/api/demo/sample-result");
}
