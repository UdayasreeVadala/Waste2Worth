export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export function apiUrl(path: string): string {
  return `${API_URL}${path}`;
}

function readToken(): string | null {
  if (typeof window === "undefined") return null;
  const direct = window.localStorage.getItem("w2w_token");
  if (direct) return direct;
  try {
    const raw = window.localStorage.getItem("w2w_auth");
    if (raw) {
      const parsed = JSON.parse(raw) as { state?: { token?: string } };
      if (parsed?.state?.token) return parsed.state.token;
    }
  } catch {
    /* ignore */
  }
  return null;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = readToken();

  const headers: Record<string, string> = {
    ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
    ...(options.headers as Record<string, string>),
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_URL}${path}`, { ...options, headers, cache: "no-store" });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") detail = body.detail;
      else if (Array.isArray(body.detail)) detail = body.detail.map((d: any) => d.msg).join("; ");
      else if (body.message) detail = body.message;
    } catch {
      /* ignore */
    }
    throw new ApiError(detail, res.status);
  }

  return res.json() as Promise<T>;
}

export const http = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: "POST", body: JSON.stringify(body ?? {}) }),
  patch: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: "PATCH", body: JSON.stringify(body ?? {}) }),
  put: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: "PUT", body: JSON.stringify(body ?? {}) }),
  upload: <T>(path: string, file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<T>(path, { method: "POST", body: form });
  },
};