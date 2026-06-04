export const conditionLabels = {
  clear: 'Ясно',
  cloudy: 'Пасмурно',
  rain: 'Дождь',
  storm: 'Гроза',
  snow: 'Снег',
  fog: 'Туман',
};

export function normalizeCurrentBackendWeather(data) {
  const weatherCode = Number(data.weatherCode ?? data.weather_code ?? 3);
  const precipitation = Number(data.precipitation ?? 0);

  return {
    temperature: Math.round(data.temperature ?? data.temperature_2m ?? 0),
    feelsLike: Math.round(data.feelsLike ?? data.apparent_temperature ?? data.temperature_2m ?? 0),
    windSpeed: Number(data.windSpeed ?? data.wind_speed_10m ?? 0),
    precipitation,
    humidity: Number(data.humidity ?? data.relative_humidity_2m ?? 0),
    weatherCode,
    condition: data.condition || conditionFromWeatherCode(weatherCode),
    intensity: data.intensity || intensityFromWeather(weatherCode, precipitation),
    isDay: Boolean(data.isDay ?? data.is_day ?? true),
  };
}

export function getConditionLabel(condition) {
  return conditionLabels[condition] || 'Погода';
}

export function conditionFromWeatherCode(code) {
  if (code === 0 || code === 1) return 'clear';
  if (code === 2 || code === 3) return 'cloudy';
  if (code === 45 || code === 48) return 'fog';
  if ([71, 73, 75, 77, 85, 86].includes(code)) return 'snow';
  if ([95, 96, 99].includes(code)) return 'storm';
  if ([51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return 'rain';
  return 'cloudy';
}

export function intensityFromWeather(code, precipitation = 0) {
  if ([55, 57, 65, 67, 75, 82, 86, 95, 96, 99].includes(code) || precipitation >= 4) {
    return 'strong';
  }

  if ([3, 53, 63, 73, 81].includes(code) || precipitation >= 1) {
    return 'medium';
  }

  return 'soft';
}
