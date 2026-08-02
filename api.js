// Thin fetch wrapper — same-origin, since the FastAPI backend serves this frontend.
const API_BASE = "";

async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${path} failed: ${res.status}`);
  return res.json();
}

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`${path} failed: ${res.status}`);
  return res.json();
}

async function apiUpload(path, formData) {
  const res = await fetch(`${API_BASE}${path}`, { method: "POST", body: formData });
  if (!res.ok) throw new Error(`${path} failed: ${res.status}`);
  return res.json();
}

const Api = {
  checkPassword: pw => apiPost("/api/password/check", { password: pw }),
  scanUrl: url => apiPost("/api/url/scan", { url }),
  scanFile: formData => apiUpload("/api/malware/scan", formData),
  getTips: () => apiGet("/api/tips"),
  getDashboardStats: () => apiGet("/api/dashboard/stats"),
  getHistory: (params = "") => apiGet(`/api/history${params}`),
};
