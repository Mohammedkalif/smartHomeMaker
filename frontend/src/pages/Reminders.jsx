import { useEffect, useState } from "react";
import ReminderList from "../components/ReminderList";
import { completeReminder, getReminders } from "../api";
import useReminderAlerts from "../useReminderAlerts";

export default function Reminders() {
  const [data, setData] = useState({ active: [], completed: [] });
  const { toast, setToast } = useReminderAlerts();

  async function load() {
    setData(await getReminders());
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="grid">
      <ReminderList
        title="Active"
        reminders={data.active || []}
        onComplete={async (id) => {
          await completeReminder(id);
          load();
        }}
      />
      <ReminderList title="Completed" reminders={data.completed || []} />
      {toast && (
        <div className="toast">
          <p>{toast}</p>
          <button type="button" className="secondary" onClick={() => setToast(null)}>
            Close
          </button>
        </div>
      )}
    </div>
  );
}
