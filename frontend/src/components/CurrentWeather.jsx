import { Cloud, CloudFog, CloudRain, CloudSnow, MapPin, Sun, Zap } from 'lucide-react';
import { WeatherStats } from './WeatherStats';
import { getConditionLabel } from '../utils/weatherCodes';
import { formatTemperature } from '../utils/formatters';

const icons = {
  clear: Sun,
  cloudy: Cloud,
  rain: CloudRain,
  storm: Zap,
  snow: CloudSnow,
  fog: CloudFog,
};

export function CurrentWeather({ weather }) {
  const location = [weather.city, weather.country].filter(Boolean).join(', ');
  const Icon = icons[weather.current.condition] || Cloud;

  return (
    <section className="current-weather">
      <div className="current-summary">
        <div className="location-line">
          <MapPin size={18} aria-hidden="true" />
          <span>{location}</span>
        </div>
        <strong className="temperature">{formatTemperature(weather.current.temperature)}</strong>
        <p>{getConditionLabel(weather.current.condition)}</p>
      </div>

      <div className="condition-mark">
        <Icon size={76} strokeWidth={1.4} aria-hidden="true" />
      </div>

      <WeatherStats current={weather.current} />
    </section>
  );
}
