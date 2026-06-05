export function formatTemperature(value) {
  return `${Math.round(value)}°`;
}

export function formatWind(value) {
  return `${Number(value).toFixed(1)} м/с`;
}

export function formatPrecipitation(value) {
  return `${Number(value).toFixed(1)} мм`;
}

export function formatHumidity(value) {
  return `${Math.round(value)}%`;
}
