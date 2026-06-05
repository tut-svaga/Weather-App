import { mockWeather } from '../data/mockWeather';
import { normalizeCurrentBackendWeather } from '../utils/weatherCodes';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api';

export async function fetchWeather(city) {
  const query = city ? `?city=${encodeURIComponent(city)}` : '';
  const response = await fetch(`${API_BASE_URL}/weather${query}`);

  if (!response.ok) {
    throw new Error('Backend пока не вернул погоду');
  }

  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('application/json')) {
    throw new Error('Backend вернул не JSON');
  }

  const data = await response.json();
  return normalizeWeatherResponse(data);
}

function normalizeWeatherResponse(data) {
  if (data.current && data.daily && data.hourly) {
    return {
      city: data.city || data.city_name || mockWeather.city,
      country: data.country || '',
      updatedAt: data.updatedAt || data.updated_at || mockWeather.updatedAt,
      current: normalizeCurrentBackendWeather(data.current),
      daily: data.daily.map(normalizeDailyItem),
      hourly: data.hourly.map(normalizeHourlyItem),
    };
  }

  return {
    ...mockWeather,
    city: data.city_name || mockWeather.city,
    country: '',
    current: {
      ...mockWeather.current,
      ...normalizeCurrentBackendWeather(data),
    },
  };
}

function normalizeDailyItem(day) {
  return {
    date: day.date,
    label: day.label,
    tempMin: day.tempMin,
    tempMax: day.tempMax,
    weatherCode: day.weatherCode,
    condition: day.condition,
    intensity: day.intensity,
    precipitation: day.precipitation,
  };
}

function normalizeHourlyItem(hour) {
  return {
    date: hour.date,
    time: hour.time,
    temperature: hour.temperature,
    feelsLike: hour.feelsLike,
    windSpeed: hour.windSpeed,
    precipitation: hour.precipitation,
    humidity: hour.humidity,
    weatherCode: hour.weatherCode,
    condition: hour.condition,
    intensity: hour.intensity,
    isDay: hour.isDay,
  };
}
