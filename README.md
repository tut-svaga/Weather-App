# Weather App

Weather App — учебный DevOps-проект с frontend, backend, базой данных и reverse proxy.

Приложение показывает погоду по текущему местоположению или по названию города, а также получает случайные цитаты из базы данных.

## Что делает проект

Пользователь открывает frontend в браузере. Frontend отправляет запросы к backend через Nginx по пути `/api`.

Backend обрабатывает запросы:

* получает прогноз погоды;
* отдаёт случайную цитату;
* работает с PostgreSQL;
* запускает миграции базы данных при старте контейнера.

## Стек

| Часть проекта   | Технологии                           |
| --------------- | ------------------------------------ |
| Frontend        | React, Vite, JavaScript, CSS         |
| Backend         | Python, FastAPI, SQLAlchemy, Alembic |
| Database        | PostgreSQL                           |
| Proxy           | Nginx                                |
| Контейнеризация | Docker, Docker Compose               |
| CI/CD           | GitHub Actions                       |
| Деплой          | Render                               |

## Архитектура

```text
Browser
  ↓
Nginx + Frontend
  ↓ /api/*
Backend API
  ↓
PostgreSQL
```

Локально frontend доступен на порту `10000`, backend — на порту `8000`.

## API

Основные backend endpoints:

```text
GET /weather
GET /weather?city=London
GET /quotes/random
```

Через frontend/Nginx эти же запросы доступны с префиксом `/api`:

```text
GET /api/weather
GET /api/weather?city=London
GET /api/quotes/random
```

## Запуск локально

### 1. Клонировать репозиторий

```bash
git clone https://github.com/tut-svaga/Weather-App.git
cd Weather-App
```

### 2. Создать `.env`

```bash
cp .env.example .env
```

### 3. Запустить проект

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://localhost:10000
```

Backend напрямую:

```text
http://localhost:8000
```

## Проверка работы

Проверить frontend:

```bash
curl http://localhost:10000
```

Проверить backend напрямую:

```bash
curl http://localhost:8000/weather
```

Проверить backend через Nginx:

```bash
curl http://localhost:10000/api/weather
curl http://localhost:10000/api/quotes/random
```

## Переменные окружения

| Переменная                | Для чего нужна                       |
| ------------------------- | ------------------------------------ |
| `BACK_PORT`               | Порт backend-сервиса локально        |
| `APP_HOST`                | Host, на котором запускается backend |
| `FRONT_PORT`              | Порт frontend/Nginx локально         |
| `BACKEND_URL`             | Адрес backend для Nginx              |
| `POSTGRES_DB`             | Название базы данных                 |
| `POSTGRES_USER`           | Пользователь PostgreSQL              |
| `POSTGRES_PASSWORD`       | Пароль PostgreSQL                    |
| `DATABASE_URL`            | URL подключения backend к PostgreSQL |
| `PYTHONUNBUFFERED`        | Вывод логов Python без буферизации   |
| `PYTHONDONTWRITEBYTECODE` | Отключает создание `.pyc` файлов     |

Для локального запуска через Docker Compose:

```env
BACKEND_URL=http://backend:8000
```

Для Render в переменных окружения frontend-сервиса нужно указать публичный URL backend:

```env
BACKEND_URL=https://your-backend.onrender.com
```

## Деплой

Проект рассчитан на деплой двух сервисов:

* backend service;
* frontend service.

Frontend использует переменную `BACKEND_URL`, чтобы Nginx понимал, куда проксировать API-запросы.

На локальной машине `BACKEND_URL` указывает на docker-compose сервис `backend`.

На Render `BACKEND_URL` должен указывать на опубликованный backend-сервис.

## Полезные команды

Пересобрать и запустить контейнеры:

```bash
docker compose up --build
```

Остановить контейнеры:

```bash
docker compose down
```

Остановить контейнеры и удалить volume с базой данных:

```bash
docker compose down -v
```

Посмотреть логи:

```bash
docker compose logs -f
```

Посмотреть логи backend:

```bash
docker compose logs -f backend
```

Посмотреть логи frontend/Nginx:

```bash
docker compose logs -f nginx
```

Безопасность переменных окружения

Файл .env.example хранится в репозитории только как пример.

Некоторые значения в проекте указаны для демонстрации и локального запуска. Например, имя пользователя базы данных, название базы данных и пример пароля нужны, чтобы было понятно, какие переменные требуется создать.

В реальном продукте нельзя публиковать настоящие данные доступа:

реальные пароли от базы данных;
production DATABASE_URL;
токены;
API keys;
секретные ключи приложения.

## Примечание

Файл `.env` не должен попадать в репозиторий. В репозитории хранится только `.env.example` с примером переменных.
