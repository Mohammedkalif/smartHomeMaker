export default function ReminderList({ reminders = [], onComplete, title = "Reminders" }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {reminders.length === 0 && <p className="muted">No reminders yet.</p>}
      <div className="food-list">
        {reminders.map((reminder) => (
          <div className="reminder-item" key={reminder.id}>
            <strong>{reminder.food_name}</strong>
            <p>{reminder.reminder_message}</p>
            <p className="muted">At {new Date(reminder.remind_at).toLocaleString()}</p>
            {!reminder.completed && onComplete && (
              <button type="button" onClick={() => onComplete(reminder.id)}>
                Mark done
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
