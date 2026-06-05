import { Search } from 'lucide-react';
import { useState } from 'react';

export function SearchBar({ onSearch, isLoading }) {
  const [city, setCity] = useState('');

  function handleSubmit(event) {
    event.preventDefault();
    onSearch(city.trim() || undefined);
  }

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <Search size={18} aria-hidden="true" />
      <input
        value={city}
        onChange={(event) => setCity(event.target.value)}
        placeholder="Найти город"
        aria-label="Найти город"
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? '...' : 'Поиск'}
      </button>
    </form>
  );
}
