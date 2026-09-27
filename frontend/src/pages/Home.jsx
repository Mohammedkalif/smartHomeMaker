import { useEffect, useState } from "react";
import WeatherCard from "../components/WeatherCard";
import ReminderList from "../components/ReminderList";
import { completeReminder, getFoods, getProfile, getReminders, getWeather } from "../api";
import useReminderAlerts from "../useReminderAlerts";
import useWeatherAlerts from "../useWeatherAlerts";
import { Link } from "react-router-dom";
import { useLanguage } from "../i18n";

export default function Home() {
  const [profile, setProfile] = useState(null);
  const [weather, setWeather] = useState(null);
  const [weatherError, setWeatherError] = useState("");
  const [active, setActive] = useState([]);
  const [foods, setFoods] = useState([]);
  const { toast, setToast, dismiss } = useReminderAlerts();
  const { t } = useLanguage();
  useWeatherAlerts(weather);

  async function load() {
    const user = await getProfile();
    setProfile(user);
    const reminderData = await getReminders();
    setActive(reminderData.active || []);
    const foodData = await getFoods(user.state, "dinner");
    setFoods((foodData.foods || []).slice(0, 3));
    try {
      setWeather(await getWeather(user.city));
      setWeatherError("");
    } catch (err) {
      setWeatherError(err.message);
    }
  }

  useEffect(() => {
    load().catch(() => {});
  }, []);

  if (!profile) return <div className="card">{t("loading")}</div>;

  return (
    <div className="dashboard">
      <section className="dashboard-hero"><div><p className="eyebrow">{t("today")}</p><h1>{t("welcome")}, {profile.name}.</h1><p>{t("dashboardIntro")}</p></div><Link className="hero-action" to="/assistant">{t("askAssistant")} <span>→</span></Link></section>
      <section className="dashboard-grid">
        <WeatherCard weather={weather} error={weatherError} />
        <ReminderList title={t("activeTasks")} reminders={active.slice(0, 3)} onComplete={async (id) => { await completeReminder(id); const reminderData = await getReminders(); setActive(reminderData.active || []); dismiss(id); }} />
        <div className="card food-card"><div className="card-heading"><h2>{t("dinnerIdeas")}</h2><Link to="/food">{t("viewAll")}</Link></div>{foods.map((food) => <div className="food-preview" key={food.id}><strong>{food.dish_name}</strong><p>{food.description}</p></div>)}</div>
      </section>
      {toast && (
        <div className="toast">
          <strong>Reminder</strong>
          <p>{toast}</p>
          <button type="button" className="secondary" onClick={() => setToast(null)}>
            Close
          </button>
        </div>
      )}
    </div>
  );
}
