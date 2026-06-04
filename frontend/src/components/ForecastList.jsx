import { ForecastCard } from './ForecastCard';

export function ForecastList({ forecast, selectedDate, onSelectDate }) {
  return (
    <section className="forecast-section" aria-label="Прогноз на 5 дней">
      <div className="section-heading">
        <h2>5 дней</h2>
        <span>Нажми на день, чтобы увидеть часы</span>
      </div>
      <div className="forecast-grid">
        {forecast.map((day) => (
          <ForecastCard
            day={day}
            key={day.date}
            isActive={day.date === selectedDate}
            onClick={() => onSelectDate(day.date)}
          />
        ))}
      </div>
    </section>
  );
}
