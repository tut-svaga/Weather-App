// frontend/src/components/RandomQuote.jsx
// Использование: <RandomQuote /> — просто дропни в любое место

import { useRandomQuote } from '../api/useRandomQuote';

const RandomQuote = () => {
  const { quote, loading, error, fetchQuote } = useRandomQuote();

  return (
    <div className="quote-card">
      {loading && <p className="quote-loading">Загрузка...</p>}

      {error && (
        <p className="quote-error">Ошибка: {error}</p>
      )}

      {!loading && quote && (
        <>
          <blockquote className="quote-text">
            &ldquo;{quote.text}&rdquo;
          </blockquote>
          {quote.author && (
            <p className="quote-author">— {quote.author}</p>
          )}
          {quote.category && (
            <span className="quote-category">{quote.category}</span>
          )}
        </>
      )}

      <button
        className="quote-btn"
        onClick={fetchQuote}
        disabled={loading}
      >
        {loading ? '...' : 'Следующая цитата'}
      </button>
    </div>
  );
};

export default RandomQuote;

/* ── CSS (добавь в свой .css / tailwind / styled-components) ─────────────────
.quote-card {
  max-width: 600px;
  padding: 2rem;
  border-radius: 12px;
  background: #f9f9f9;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  text-align: center;
}
.quote-text {
  font-size: 1.25rem;
  font-style: italic;
  margin-bottom: 1rem;
  color: #333;
}
.quote-author {
  font-weight: 600;
  color: #555;
  margin-bottom: 0.5rem;
}
.quote-category {
  font-size: 0.8rem;
  padding: 2px 10px;
  border-radius: 999px;
  background: #e0e7ff;
  color: #4f46e5;
}
.quote-btn {
  margin-top: 1.5rem;
  padding: 0.6rem 1.5rem;
  border: none;
  border-radius: 8px;
  background: #4f46e5;
  color: white;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}
.quote-btn:hover:not(:disabled) { background: #4338ca; }
.quote-btn:disabled { opacity: 0.6; cursor: not-allowed; }
─────────────────────────────────────────────────────────────────────────── */
