import { Droplets, ThermometerSun, Umbrella, Wind } from 'lucide-react';
import { formatHumidity, formatPrecipitation, formatTemperature, formatWind } from '../utils/formatters';

export function WeatherStats({ current }) {
  const stats = [
    { icon: ThermometerSun, label: 'Ощущается', value: formatTemperature(current.feelsLike) },
    { icon: Wind, label: 'Ветер', value: formatWind(current.windSpeed) },
    { icon: Umbrella, label: 'Осадки', value: formatPrecipitation(current.precipitation) },
    { icon: Droplets, label: 'Влажность', value: formatHumidity(current.humidity) },
  ];

  return (
    <div className="weather-stats">
      {stats.map(({ icon: Icon, label, value }) => (
        <article className="stat-card" key={label}>
          <Icon size={20} aria-hidden="true" />
          <span>{label}</span>
          <strong>{value}</strong>
        </article>
      ))}
    </div>
  );
}
