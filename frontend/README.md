# Up Weather Frontend

React + Vite каркас для погодного фронтенда.

## Запуск

```bash
npm install
npm run dev
```

Frontend ожидает расширенный backend из `up_backend`:

```env
VITE_API_BASE_URL=http://localhost:8001
```

## Сейчас готово

- поиск города через `GET /weather?city=...`;
- первая загрузка через `GET /weather`;
- текущая погода, 5 дней и почасовые карточки;
- динамический фон по `condition`: ясно, пасмурно, дождь, гроза, снег, туман;
- поддержка старого backend-ответа как временный fallback.
