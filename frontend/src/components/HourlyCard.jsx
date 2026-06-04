import { Cloud, CloudFog, CloudRain, CloudSnow, Sun, Zap } from 'lucide-react';
import { formatHumidity, formatTemperature, formatWind } from '../utils/formatters';

const icons = {
  clear: Sun,
  cloudy: Cloud,
  rain: CloudRain,
  storm: Zap,
  snow: CloudSnow,
  fog: CloudFog,
};

export function HourlyCard({ hour }) {
  const Icon = icons[hour.condition] || Cloud;

  return (
    <article className="hourly-card">
      <span>{hour.time}</span>
      <Icon size={22} aria-hidden="true" />
      <strong>{formatTemperature(hour.temperature)}</strong>
      <small>{formatWind(hour.windSpeed)}</small>
      <small>{formatHumidity(hour.humidity)}</small>
    </article>
  );
}
