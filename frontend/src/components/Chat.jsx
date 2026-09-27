import { useEffect, useRef, useState } from "react";
import { getProfile, sendChat } from "../api";

export default function Chat({ compact = false }) {
  const [profile, setProfile] = useState(null);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I can recommend food, create household tasks from your message, help with cooking, and check the weather. You can type or use the microphone.",
    },
  ]);
  const [text, setText] = useState("");
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const boxRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    loadProfile();
  }, []);

  async function loadProfile() {
    try {
      const data = await getProfile();
      setProfile(data);
    } catch (err) {
      console.error("Failed to load profile:", err);
    }
  }

  useEffect(() => {
    if (boxRef.current) {
      boxRef.current.scrollTop = boxRef.current.scrollHeight;
    }
  }, [messages, loading]);

  async function submit(message) {
    const value = (message || text).trim();
    if (!value || loading) return;
    setText("");
    setError("");
    setMessages((current) => [...current, { role: "user", content: value }]);
    setLoading(true);
    try {
      const data = await sendChat(value);
      setMessages((current) => [
        ...current,
        { role: "assistant", content: data.response },
      ]);
      
      await loadProfile();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function startVoice() {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError("Voice input is not supported in this browser. Try Chrome or Edge.");
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = ({ Tamil: "ta-IN", Hindi: "hi-IN", Malayalam: "ml-IN", Telugu: "te-IN", Kannada: "kn-IN" })[profile?.language] || "en-IN";
    recognition.interimResults = false;
    recognition.onresult = (event) => {
      const spoken = event.results[0][0].transcript;
      setText(spoken);
      submit(spoken);
    };
    recognition.onerror = () => {
      setListening(false);
      setError("Could not hear that. Please try again.");
    };
    recognition.onend = () => setListening(false);
    recognitionRef.current = recognition;
    setListening(true);
    recognition.start();
  }

  return (
    <div className="card">
      <h2>{compact ? "Chat" : "Ask Something"}</h2>
      <div className="chat-box" ref={boxRef} style={{ minHeight: compact ? 220 : 360 }}>
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            {message.content}
          </div>
        ))}
        {loading && <div className="message assistant">Thinking...</div>}
      </div>
      {error && <p className="error">{error}</p>}
      <div className="row">
        <input
          value={text}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={(event) => event.key === "Enter" && submit()}
          placeholder="Try: 'Remind me to call the plumber tomorrow'"
        />
        <button type="button" className="secondary" onClick={startVoice} title="Voice input">
          {listening ? "Listening..." : "Voice"}
        </button>
        <button type="button" onClick={() => submit()} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}
