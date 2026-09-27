import { useEffect, useRef, useState } from "react";
import { completeReminder, getReminders } from "./api";

export default function useReminderAlerts() {
  const [due, setDue] = useState([]);
  const [toast, setToast] = useState(null);
  const seen = useRef(new Set());

  useEffect(() => {
    if ("Notification" in window && Notification.permission === "default") {
      Notification.requestPermission();
    }

    async function poll() {
      try {
        const data = await getReminders();
        setDue(data.due || []);
        [...(data.near || []), ...(data.due || [])].forEach((reminder) => {
          if (seen.current.has(reminder.id)) return;
          seen.current.add(reminder.id);
          const text = reminder.reminder_message || `Check the ${reminder.food_name}`;
          setToast(text);
          if ("Notification" in window && Notification.permission === "granted") {
            new Notification("Smart Homemaker task", { body: text });
          }
        });
      } catch {
        // Keep the UI usable if polling fails once.
      }
    }

    poll();
    const timer = setInterval(poll, 10000);
    return () => clearInterval(timer);
  }, []);

  async function dismiss(id) {
    await completeReminder(id);
    setDue((current) => current.filter((item) => item.id !== id));
    setToast(null);
  }

  return { due, toast, dismiss, setToast };
}
