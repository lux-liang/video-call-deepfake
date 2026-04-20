const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

function getApiBaseUrl(): string {
  return process.env.MEETTRUTH_API_BASE_URL ?? DEFAULT_API_BASE_URL;
}

export async function proxyToMeetTruth(path: string, init?: RequestInit): Promise<Response> {
  const targetUrl = `${getApiBaseUrl()}${path}`;

  try {
    const response = await fetch(targetUrl, {
      ...init,
      headers: {
        Accept: "application/json",
        ...(init?.headers ?? {}),
      },
      cache: "no-store",
    });

    const payload = await response.text();

    return new Response(payload, {
      status: response.status,
      headers: {
        "Content-Type": response.headers.get("Content-Type") ?? "application/json",
      },
    });
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Unknown error while reaching MeetTruth backend.";

    return Response.json(
      {
        error: `Unable to reach backend at ${targetUrl}. ${message}`,
      },
      {
        status: 502,
      },
    );
  }
}
