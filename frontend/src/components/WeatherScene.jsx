const rainDrops = Array.from({ length: 58 }, (_, index) => ({
  id: `rain-${index}`,
  left: (index * 17 + 9) % 100,
  delay: -((index * 0.19) % 2.8),
  duration: 0.72 + (index % 7) * 0.08,
  length: 34 + (index % 5) * 13,
  opacity: 0.28 + (index % 6) * 0.08,
}));

const rainSplashes = Array.from({ length: 28 }, (_, index) => ({
  id: `splash-${index}`,
  left: (index * 29 + 7) % 100,
  delay: -((index * 0.23) % 2.2),
  scale: 0.7 + (index % 5) * 0.18,
}));

const snowFlakes = Array.from({ length: 42 }, (_, index) => ({
  id: `snow-${index}`,
  left: (index * 23 + 11) % 100,
  delay: -((index * 0.37) % 8),
  duration: 7 + (index % 8) * 0.8,
  size: 3 + (index % 5),
}));

export function WeatherScene({ condition, intensity }) {
  return (
    <div className={`weather-scene weather-${condition} intensity-${intensity}`} aria-hidden="true">
      <div className="scene-gradient" />
      <div className="sun-core" />
      <div className="cloud-bank cloud-bank-back" />
      <div className="cloud-bank cloud-bank-mid" />
      <div className="cloud-bank cloud-bank-front" />

      <div className="rain-field">
        {rainDrops.map((drop) => (
          <span
            className="rain-drop"
            key={drop.id}
            style={{
              '--left': `${drop.left}%`,
              '--delay': `${drop.delay}s`,
              '--duration': `${drop.duration}s`,
              '--length': `${drop.length}px`,
              '--opacity': drop.opacity,
            }}
          />
        ))}
      </div>

      <div className="splash-field">
        {rainSplashes.map((splash) => (
          <span
            className="rain-splash"
            key={splash.id}
            style={{
              '--left': `${splash.left}%`,
              '--delay': `${splash.delay}s`,
              '--scale': splash.scale,
            }}
          />
        ))}
      </div>

      <div className="snow-field">
        {snowFlakes.map((flake) => (
          <span
            className="snow-flake"
            key={flake.id}
            style={{
              '--left': `${flake.left}%`,
              '--delay': `${flake.delay}s`,
              '--duration': `${flake.duration}s`,
              '--size': `${flake.size}px`,
            }}
          />
        ))}
      </div>

      <div className="fog-layer fog-layer-low" />
      <div className="fog-layer fog-layer-high" />
      <div className="lightning-bolt bolt-one" />
      <div className="lightning-bolt bolt-two" />
      <div className="storm-flash" />
    </div>
  );
}
