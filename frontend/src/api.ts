const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

interface CustomTokenResponse {
  custom_token: string;
  uid: string;
}

export async function fetchCustomToken(
  code: string
): Promise<CustomTokenResponse> {
  const res = await fetch(`${API_BASE_URL}/api/auth/custom-token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }

  return res.json();
}
