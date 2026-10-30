const API_URL = (import.meta.env.VITE_API_URL || "/api/v1").replace(/\/+$/, "");

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(API_URL + path, {
      ...options,
      headers: {
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...(options.headers || {}),
      },
    });
  } catch {
    throw new Error("Не удалось подключиться к API. Проверьте, запущен ли бэкенд на порту 8000.");
  }

  if (response.status === 204) return null;

  const text = await response.text();
  let data = null;
  if (text) {
    try { data = JSON.parse(text); }
    catch { data = { detail: text }; }
  }

  if (!response.ok) {
    let message = data && data.detail;
    if (Array.isArray(message)) message = message.map((item) => item.msg || String(item)).join("; ");
    if (message && typeof message === "object") message = message.message || JSON.stringify(message);
    throw new Error(message || "Ошибка API: " + response.status);
  }
  return data;
}

function queryString(filters = {}) {
  const params = new URLSearchParams();
  for (const key of ["type", "category_id", "search", "limit", "offset"]) {
    if (filters[key] !== undefined && filters[key] !== null && String(filters[key]).trim() !== "") {
      params.set(key, String(filters[key]).trim());
    }
  }
  if (filters.date_from) params.set("date_from", new Date(filters.date_from + "T00:00:00").toISOString());
  if (filters.date_to) params.set("date_to", new Date(filters.date_to + "T23:59:59").toISOString());
  const result = params.toString();
  return result ? "?" + result : "";
}

export const api = {
  getCategories: () => request("/categories"),
  createCategory: (payload) => request("/categories", { method: "POST", body: JSON.stringify(payload) }),
  updateCategory: (id, payload) => request("/categories/" + encodeURIComponent(id), { method: "PUT", body: JSON.stringify(payload) }),
  deleteCategory: (id) => request("/categories/" + encodeURIComponent(id), { method: "DELETE" }),
  getTransactions: (filters) => request("/transactions" + queryString(filters)),
  createTransaction: (payload) => request("/transactions", { method: "POST", body: JSON.stringify(payload) }),
  updateTransaction: (id, payload) => request("/transactions/" + encodeURIComponent(id), { method: "PUT", body: JSON.stringify(payload) }),
  deleteTransaction: (id) => request("/transactions/" + encodeURIComponent(id), { method: "DELETE" }),
  getStatistics: () => request("/statistics/summary"),
};

