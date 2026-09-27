import Chat from "../components/Chat";
import useReminderAlerts from "../useReminderAlerts";

export default function Assistant() {
  const { toast, setToast } = useReminderAlerts();
  return (
    <>
      <Chat />
      {toast && (
        <div className="toast">
          <p>{toast}</p>
          <button type="button" className="secondary" onClick={() => setToast(null)}>
            Close
          </button>
        </div>
      )}
    </>
  );
}
