import { proxyToMeetTruth } from "@/lib/server-api";

export async function POST(request: Request): Promise<Response> {
  const body = await request.text();

  return proxyToMeetTruth("/api/upload", {
    method: "POST",
    body,
    headers: {
      "Content-Type": "application/json",
    },
  });
}
