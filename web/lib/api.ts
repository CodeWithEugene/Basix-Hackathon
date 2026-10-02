"use client";

// The browser talks only to Next.js route handlers, which proxy to the agents.
import { useCallback, useEffect, useRef, useState } from "react";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export async function api<T>(
  role: "community" | "facility",
  path: string,
  init?: RequestInit,
): Promise<T> {
  const res = await fetch(`/api/${role}${path}`, {
    ...init,
    headers: { "content-type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body?.error?.message || body?.detail || detail;
    } catch {
      // keep status text
    }
    throw new ApiError(detail, res.status);
  }
  const text = await res.text();
  return (text ? JSON.parse(text) : {}) as T;
}

export function useAgent<T>(
  role: "community" | "facility",
  path: string,
  options: { pollMs?: number; initial?: T } = {},
) {
  const { pollMs = 0, initial } = options;
  const [data, setData] = useState<T | undefined>(initial);
  const [error, setError] = useState<ApiError | null>(null);
  const [loading, setLoading] = useState(true);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  const load = useCallback(async () => {
    try {
      const d = await api<T>(role, path);
      setData(d);
      setError(null);
    } catch (e) {
      setError(e as ApiError);
    } finally {
      setLoading(false);
    }
  }, [role, path]);

  useEffect(() => {
    const id = setTimeout(() => void load(), 0);
    if (pollMs > 0) {
      timer.current = setInterval(() => void load(), pollMs);
    }
    return () => {
      clearTimeout(id);
      if (timer.current) clearInterval(timer.current);
    };
  }, [load, pollMs]);

  return { data, error, loading, reload: load };
}
