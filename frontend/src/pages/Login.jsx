import { useState } from "react";
import { authenticate, saveSessionToken } from "../api";

export default function Login({ onAuthenticated }) {
  const [mode, setMode] = useState("login");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setError(""); setLoading(true);
    const values = Object.fromEntries(new FormData(event.currentTarget));
    try {
      const result = await authenticate(mode, values);
      saveSessionToken(result.token);
      onAuthenticated(result.user);
    } catch (err) { setError(err.message); } finally { setLoading(false); }
  }

  const isLogin = mode === "login";
  return <main className="login-page"><section className="login-panel"><div className="login-brand"><span className="brand-mark">SH</span><span><strong>Smart Homemaker</strong><small>Your calm home command center</small></span></div><p className="eyebrow">WELCOME HOME</p><h1>{isLogin ? "Sign in to your home" : "Create your home account"}</h1><p className="muted">Your name is used across your profile, dashboard and personal home plans.</p><form onSubmit={submit}><label htmlFor="login-name">Name</label><input id="login-name" name="name" autoComplete="username" minLength="2" required placeholder="Your name" /><label htmlFor="login-password">Password</label><input id="login-password" name="password" type="password" autoComplete={isLogin ? "current-password" : "new-password"} minLength="8" required placeholder="At least 8 characters" />{error && <p className="error" role="alert">{error}</p>}<button type="submit" disabled={loading}>{loading ? "Please wait…" : isLogin ? "Sign in" : "Create account"}</button></form><p className="login-switch">{isLogin ? "New here?" : "Already have an account?"} <button type="button" className="text-button" onClick={() => { setMode(isLogin ? "register" : "login"); setError(""); }}>{isLogin ? "Create an account" : "Sign in"}</button></p></section></main>;
}
