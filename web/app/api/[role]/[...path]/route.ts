import { NextRequest, NextResponse } from "next/server";

// Server-side proxy: the browser never talks to the agents directly, and no
// secret ever reaches the browser.
const TARGETS: Record<string, string | undefined> = {
  community: process.env.AGENT_COMMUNITY_URL || "http://127.0.0.1:8101",
  facility: process.env.AGENT_FACILITY_URL || "http://127.0.0.1:8102",
};

async function proxy(
  req: NextRequest,
  ctx: { params: Promise<{ role: string; path: string[] }> },
) {
  const { role, path } = await ctx.params;
  const base = TARGETS[role];
  if (!base) {
    return NextResponse.json(
      { ok: false, error: { code: "bad_role", message: `unknown role ${role}` } },
      { status: 404 },
    );
  }
  const url = `${base}/${path.join("/")}${req.nextUrl.search}`;
  const init: RequestInit = {
    method: req.method,
    headers: { "content-type": req.headers.get("content-type") || "application/json" },
    cache: "no-store",
  };
  if (req.method !== "GET" && req.method !== "HEAD") {
    init.body = await req.text();
  }
  try {
    const upstream = await fetch(url, init);
    const text = await upstream.text();
    const contentType = upstream.headers.get("content-type") || "application/json";
    return new NextResponse(text, {
      status: upstream.status,
      headers: { "content-type": contentType },
    });
  } catch {
    return NextResponse.json(
      { ok: false, error: { code: "agent_unreachable", message: `${role} agent is unreachable` } },
      { status: 502 },
    );
  }
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const DELETE = proxy;
