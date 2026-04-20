import { proxyToMeetTruth } from "@/lib/server-api";

export async function POST(request: Request): Promise<Response> {
  const body = await request.text();

  return proxyToMeetTruth("/api/analyze", {
    method: "POST",
    body,
    headers: {
      "Content-Type": "application/json",
    },
  });
}
