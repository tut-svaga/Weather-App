# Weather App

Веб-приложение для просмотра погоды с автоматическим CI/CD деплоем.

## Стек

| Часть | Технологии |
|-------|-----------|
| Backend | Python |
| Frontend | JavaScript, HTML, CSS |
| Proxy | Nginx |
| Контейнеризация | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Деплой | Render.com |
| Weather API | [Open-Meteo](https://open-meteo.com/) (бесплатно, без ключа) |

## Архитектура

```
Browser
  ↓
Nginx (reverse proxy, port 80)
Frontend (React)
  ↓
Backend (Python API)
```

## CI/CD Pipeline

```
git push → main и dev
    ↓
GitHub Actions (сборка)
    ↓
Webhook → Render.com (автодеплой)
```

## Запуск локально

### 1. Клонировать репозиторий

```bash
git clone https://github.com/tut-svaga/Weather-App.git
cd Weather-App
```

### 2. Создать .env файл

```bash
cp .env.example .env
```

### 3. Запустить через Docker Compose

```bash
docker-compose up --build
```

Приложение доступно на `http://localhost`

## Переменные окружения

Создай `.env` файл в корне проекта:

```env
# Пример переменных
BACK_PORT=
APP_HOST=
PYTHONUNBUFFERED=
PYTHONDONTWRITEBYTECODE=
FRONT_PORT=
BACKEND_URL=
```

## Демо

```
[frontend]: (https://weather-services-3ilo.onrender.com)
[backend]: (https://weather-backend-3ilo.onrender.com) 
```