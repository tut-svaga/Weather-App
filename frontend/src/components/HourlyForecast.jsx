import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useRef } from 'react';
import { HourlyCard } from './HourlyCard';

export function HourlyForecast({ hours }) {
  const rowRef = useRef(null);
  const visibleHours = hours.slice(0, 24);

  function scrollHours(direction) {
    rowRef.current?.scrollBy({
      left: direction * 420,
      behavior: 'smooth',
    });
  }

  return (
    <section className="hourly-section" aria-label="Почасовой прогноз">
      <div className="section-heading">
        <div>
          <h2>24 часа</h2>
          <span>Прокручиваемая лента выбранного дня</span>
        </div>
        <div className="hourly-controls" aria-label="Прокрутка почасового прогноза">
          <button type="button" onClick={() => scrollHours(-1)} aria-label="Назад по часам">
            <ChevronLeft size={18} aria-hidden="true" />
          </button>
          <button type="button" onClick={() => scrollHours(1)} aria-label="Вперёд по часам">
            <ChevronRight size={18} aria-hidden="true" />
          </button>
        </div>
      </div>

      <div className="hourly-row" ref={rowRef}>
        {visibleHours.map((hour) => (
          <HourlyCard hour={hour} key={`${hour.date}-${hour.time}`} />
        ))}
      </div>
    </section>
  );
}
