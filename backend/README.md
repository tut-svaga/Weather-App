# Up Weather Backend

FastAPI backend с расширенным контрактом для `up_frontend`.

## Локальный запуск

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

Для frontend:

```env
VITE_API_BASE_URL=http://localhost:8001
```

## Endpoint

```text
GET /weather
GET /weather?city=Tiraspol
```

Ответ включает текущую погоду, 5 дней прогноза и почасовые карточки.
