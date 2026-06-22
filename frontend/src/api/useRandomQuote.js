// frontend/src/hooks/useRandomQuote.js

import { useState, useCallback, useEffect } from 'react';

export const useRandomQuote = ({ fetchOnMount = true } = {}) => {
  const [quote, setQuote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchQuote = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/quotes/random');
      if (!res.ok) throw new Error(`Ошибка ${res.status}`);
      const data = await res.json();
      setQuote(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (fetchOnMount) fetchQuote();
  }, [fetchOnMount, fetchQuote]);

  return { quote, loading, error, fetchQuote };
};
