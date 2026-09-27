const API = import.meta.env.VITE_API_BASE || "";
const TOKEN_KEY = "smart-homemaker-session";

export function getSessionToken() { return localStorage.getItem(TOKEN_KEY); }
export function saveSessionToken(token) { localStorage.setItem(TOKEN_KEY, token); }
export function clearSessionToken() { localStorage.removeItem(TOKEN_KEY); }

async function request(path, options = {}) {
  const headers = new Headers(options.headers);
  const token = getSessionToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const response = await fetch(`${API}${path}`, { ...options, headers });
  if (!response.ok) throw new Error(await readError(response));
  return readJson(response);
}

async function readJson(response) {
  const body = await response.text();
  if (!body) throw new Error("The API returned an empty response. Check that VITE_API_BASE points to the deployed backend URL.");
  try {
    return JSON.parse(body);
  } catch {
    throw new Error("The API returned an invalid response. Check that VITE_API_BASE points to the deployed backend URL.");
  }
}

async function readError(response) {
  try {
    const data = await response.json();
    return data.detail || "Request failed.";
  } catch {
    return "Request failed.";
  }
}

export async function getProfile() {
  return request("/api/profile");
}

export async function updateProfile(payload) {
  return request("/api/profile", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function authenticate(mode, payload) {
  const response = await fetch(`${API}/api/auth/${mode}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
  if (!response.ok) throw new Error(await readError(response));
  return readJson(response);
}

export async function sendChat(message) {
  return request("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
}

export async function getWeather(city) {
  return request(`/api/weather?city=${encodeURIComponent(city)}`);
}

export async function getReminders() {
  return request("/api/reminders");
}

export async function completeReminder(id) {
  return request(`/api/reminders/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed: true }),
  });
}

export async function getFoods(state, mealType) {
  const params = new URLSearchParams();
  if (state) params.set("state", state);
  if (mealType) params.set("meal_type", mealType);
  return request(`/api/foods?${params.toString()}`);
}

export async function getFood(id) {
  return request(`/api/foods/${id}`);
}

export async function getAIFoodSuggestions(payload) {
  return request("/api/ai/food-suggestions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}
