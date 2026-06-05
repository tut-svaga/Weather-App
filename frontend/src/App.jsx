import { useEffect, useMemo, useState } from 'react';
import { fetchWeather } from './api/weatherApi';
import { mockWeather } from './data/mockWeather';
import { SearchBar } from './components/SearchBar';
import { CurrentWeather } from './components/CurrentWeather';
import { ForecastList } from './components/ForecastList';
import { HourlyForecast } from './components/HourlyForecast';
import { WeatherScene } from './components/WeatherScene';
import { LoadingState } from './components/LoadingState';
import { ErrorState } from './components/ErrorState';

export default function App() {
  const [weather, setWeather] = useState(mockWeather);
  const [selectedDate, setSelectedDate] = useState(mockWeather.daily[0]?.date);
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState('');

  async function loadWeather(city) {
    setStatus('loading');
    setError('');

    try {
      const nextWeather = await fetchWeather(city);
      setWeather(nextWeather);
      setSelectedDate(nextWeather.daily[0]?.date);
      setStatus('success');
    } catch (currentError) {
      setError(currentError.message || 'Не удалось загрузить погоду');
      setWeather(mockWeather);
      setSelectedDate(mockWeather.daily[0]?.date);
      setStatus('error');
    }
  }

  useEffect(() => {
    loadWeather();
  }, []);

  const selectedHours = useMemo(() => {
    return weather.hourly.filter((hour) => hour.date === selectedDate);
  }, [selectedDate, weather.hourly]);

  return (
    <main className="app-shell">
      <WeatherScene condition={weather.current.condition} intensity={weather.current.intensity} />

      <section className="weather-layout" aria-label="Погода">
        <header className="top-panel">
          <div>
            <p className="eyebrow">Open-Meteo forecast</p>
            <h1>Погода сейчас</h1>
          </div>
          <SearchBar onSearch={loadWeather} isLoading={status === 'loading'} />
        </header>

        {status === 'loading' && <LoadingState />}
        {status === 'error' && <ErrorState message={error} />}

        <CurrentWeather weather={weather} />
        <ForecastList
          forecast={weather.daily}
          selectedDate={selectedDate}
          onSelectDate={setSelectedDate}
        />
        <HourlyForecast hours={selectedHours} />
      </section>
    </main>
  );
}
