import { Cloud, CloudFog, CloudRain, CloudSnow, Sun, Zap } from 'lucide-react';
import { getConditionLabel } from '../utils/weatherCodes';
import { formatPrecipitation, formatTemperature } from '../utils/formatters';

const icons = {
  clear: Sun,
  cloudy: Cloud,
  rain: CloudRain,
  storm: Zap,
  snow: CloudSnow,
  fog: CloudFog,
};

export function ForecastCard({ day, isActive, onClick }) {
  const Icon = icons[day.condition] || Cloud;

  return (
    <button className={`forecast-card ${isActive ? 'is-active' : ''}`} type="button" onClick={onClick}>
      <span className="forecast-date">{day.label}</span>
      <Icon size={28} aria-hidden="true" />
      <strong>{formatTemperature(day.tempMax)}</strong>
      <span>{formatTemperature(day.tempMin)} ночью</span>
      <span>{getConditionLabel(day.condition)}</span>
      <small>{formatPrecipitation(day.precipitation)}</small>
    </button>
  );
}
