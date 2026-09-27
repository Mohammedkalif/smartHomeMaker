export default function WeatherCard({ weather, error }) {
  if (error) {
    return (
      <div className="card">
        <h2>Weather</h2>
        <p className="error">{error}</p>
      </div>
    );
  }
  if (!weather) {
    return (
      <div className="card">
        <h2>Weather</h2>
        <p className="muted">Loading weather...</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Weather in {weather.city}</h2>
      <p>
        <strong>{Math.round(weather.temperature)}°C</strong> · {weather.condition}
      </p>
      <p>Humidity: {weather.humidity ?? "N/A"}%</p>
      <p>
        Rain possibility:{" "}
        {weather.rain_probability == null ? "Not available" : `${weather.rain_probability}%`}
      </p>
      <p>{weather.recommendation}</p>
    </div>
  );
}
