import { useEffect, useRef } from "react";

export default function useWeatherAlerts(weather) {
  const seen = useRef("");
  useEffect(() => {
    if (!weather?.rain_soon) return;
    const key = `${weather.city}-${new Date().toDateString()}`;
    if (seen.current === key || localStorage.getItem("rain-alert") === key) return;
    seen.current = key;
    localStorage.setItem("rain-alert", key);
    const notify = () => new Notification("Rain may be near", { body: `Rain is likely in the next few hours in ${weather.city}.` });
    if ("Notification" in window && Notification.permission === "granted") notify();
    else if ("Notification" in window && Notification.permission === "default") Notification.requestPermission().then((permission) => permission === "granted" && notify());
  }, [weather]);
}
