import { NavLink, Route, Routes } from "react-router-dom";
import { useEffect, useState } from "react";
import Home from "./pages/Home";
import Assistant from "./pages/Assistant";
import Food from "./pages/Food";
import Reminders from "./pages/Reminders";
import Profile from "./pages/Profile";
import { getProfile } from "./api";
import { clearSessionToken, getSessionToken } from "./api";
import Login from "./pages/Login";
import { LanguageProvider, useLanguage } from "./i18n";

function Layout({ onLogout }) {
  const [profile, setProfile] = useState(null);
  const { t } = useLanguage();

  useEffect(() => {
    loadProfile();
  }, []);

  async function loadProfile() {
    try {
      const data = await getProfile();
      setProfile(data);
    } catch (err) {
      console.error("Failed to load profile:", err);
      onLogout();
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <NavLink className="brand" to="/" aria-label="Smart Homemaker dashboard">
          <span className="brand-mark">SH</span><span><strong>Smart Homemaker</strong><small>{t("brandTagline")}</small></span>
        </NavLink>
        <nav aria-label="Main navigation">
          <NavLink to="/" end>{t("dashboard")}</NavLink><NavLink to="/assistant">{t("assistant")}</NavLink><NavLink to="/food">{t("food")}</NavLink><NavLink to="/reminders">{t("tasks")}</NavLink>
          <NavLink className="profile-nav" to="/profile"><span className="profile-avatar">{profile?.name?.charAt(0).toUpperCase() || "U"}</span><span>{t("profile")}</span></NavLink><button className="logout-button" type="button" onClick={onLogout}>Sign out</button>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/assistant" element={<Assistant />} />
          <Route path="/food" element={<Food />} />
          <Route path="/reminders" element={<Reminders />} />
          <Route path="/profile" element={<Profile onSaved={setProfile} />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  const [authenticated, setAuthenticated] = useState(Boolean(getSessionToken()));
  function logout() { clearSessionToken(); setAuthenticated(false); }
  return <LanguageProvider>{authenticated ? <Layout onLogout={logout} /> : <Login onAuthenticated={() => setAuthenticated(true)} />}</LanguageProvider>;
}
