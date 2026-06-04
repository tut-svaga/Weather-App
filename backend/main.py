from datetime import datetime
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


Condition = Literal["clear", "cloudy", "rain", "storm", "snow", "fog"]
Intensity = Literal["soft", "medium", "strong"]


class CurrentWeather(BaseModel):
    temperature: float
    feelsLike: float
    windSpeed: float
    precipitation: float
    humidity: int
    weatherCode: int
    condition: Condition
    intensity: Intensity
    isDay: bool


class DailyWeather(BaseModel):
    date: str
    label: str
    tempMin: float
    tempMax: float
    weatherCode: int
    condition: Condition
    intensity: Intensity
    precipitation: float


class HourlyWeather(BaseModel):
    date: str
    time: str
    temperature: float
    feelsLike: float
    windSpeed: float
    precipitation: float
    humidity: int
    weatherCode: int
    condition: Condition
    intensity: Intensity
    isDay: bool


class WeatherResponse(BaseModel):
    city: str
    country: str | None = None
    latitude: float
    longitude: float
    timezone: str
    updatedAt: str
    current: CurrentWeather
    daily: list[DailyWeather]
    hourly: list[HourlyWeather]


app = FastAPI(
    title="Up Weather service",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://weather-frontend-fvss.onrender.com",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def describe_weather(code: int, precipitation: float = 0) -> tuple[Condition, Intensity]:
    if code in (0, 1):
        return "clear", "soft"
    if code in (2, 3):
        return "cloudy", "medium" if code == 3 else "soft"
    if code in (45, 48):
        return "fog", "medium"
    if code in (71, 73, 75, 77, 85, 86):
        return "snow", "strong" if code in (75, 86) else "medium"
    if code in (95, 96, 99):
        return "storm", "strong"
    if code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        if code in (55, 57, 65, 67, 82) or precipitation >= 4:
            return "rain", "strong"
        if code in (53, 63, 81) or precipitation >= 1:
            return "rain", "medium"
        return "rain", "soft"

    return "cloudy", "soft"


def day_label(date_text: str, index: int) -> str:
    if index == 0:
        return "Сегодня"

    labels = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    date = datetime.fromisoformat(date_text)
    return labels[date.weekday()]


async def locate_by_city(client: httpx.AsyncClient, city: str) -> dict:
    response = await client.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1, "language": "ru", "format": "json"},
    )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Geocoding service error")

    data = response.json()
    results = data.get("results") or []
    if not results:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")

    location = results[0]
    return {
        "city": location.get("name") or city,
        "country": location.get("country"),
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }


async def locate_by_ip(client: httpx.AsyncClient, request: Request) -> dict:
    client_ip = request.client.host if request.client else ""

    if (
        client_ip in ("127.0.0.1", "localhost")
        or client_ip.startswith("192.168.")
        or client_ip.startswith("10.")
        or client_ip.startswith("172.")
    ):
        client_ip = "178.17.173.1"

    response = await client.get(f"http://ip-api.com/json/{client_ip}?lang=ru")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="IP geolocation service error")

    data = response.json()
    if data.get("status") == "fail":
        raise HTTPException(status_code=400, detail=data.get("message", "Failed to locate IP"))

    return {
        "city": data.get("city") or "Defined by IP",
        "country": data.get("country"),
        "latitude": data["lat"],
        "longitude": data["lon"],
    }


async def fetch_forecast(client: httpx.AsyncClient, location: dict) -> WeatherResponse:
    response = await client.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "is_day",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                ]
            ),
            "hourly": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                    "is_day",
                ]
            ),
            "daily": ",".join(
                [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                ]
            ),
            "forecast_days": 5,
            "timezone": "auto",
        },
    )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Open-Meteo API error")

    data = response.json()
    current = data["current"]
    current_condition, current_intensity = describe_weather(
        current["weather_code"],
        current.get("precipitation", 0),
    )

    daily = []
    daily_data = data["daily"]
    for index, date_text in enumerate(daily_data["time"]):
        condition, intensity = describe_weather(
            daily_data["weather_code"][index],
            daily_data["precipitation_sum"][index],
        )
        daily.append(
            DailyWeather(
                date=date_text,
                label=day_label(date_text, index),
                tempMin=daily_data["temperature_2m_min"][index],
                tempMax=daily_data["temperature_2m_max"][index],
                weatherCode=daily_data["weather_code"][index],
                condition=condition,
                intensity=intensity,
                precipitation=daily_data["precipitation_sum"][index],
            )
        )

    hourly = []
    hourly_data = data["hourly"]
    for index, timestamp in enumerate(hourly_data["time"]):
        date_text, time_text = timestamp.split("T")
        if date_text not in daily_data["time"]:
            continue

        condition, intensity = describe_weather(
            hourly_data["weather_code"][index],
            hourly_data["precipitation"][index],
        )
        hourly.append(
            HourlyWeather(
                date=date_text,
                time=time_text,
                temperature=hourly_data["temperature_2m"][index],
                feelsLike=hourly_data["apparent_temperature"][index],
                windSpeed=hourly_data["wind_speed_10m"][index],
                precipitation=hourly_data["precipitation"][index],
                humidity=hourly_data["relative_humidity_2m"][index],
                weatherCode=hourly_data["weather_code"][index],
                condition=condition,
                intensity=intensity,
                isDay=bool(hourly_data["is_day"][index]),
            )
        )

    return WeatherResponse(
        city=location["city"],
        country=location.get("country"),
        latitude=location["latitude"],
        longitude=location["longitude"],
        timezone=data.get("timezone", "auto"),
        updatedAt=current["time"],
        current=CurrentWeather(
            temperature=current["temperature_2m"],
            feelsLike=current["apparent_temperature"],
            windSpeed=current["wind_speed_10m"],
            precipitation=current["precipitation"],
            humidity=current["relative_humidity_2m"],
            weatherCode=current["weather_code"],
            condition=current_condition,
            intensity=current_intensity,
            isDay=bool(current["is_day"]),
        ),
        daily=daily,
        hourly=hourly,
    )


@app.get("/weather", response_model=WeatherResponse)
async def get_weather(request: Request, city: str | None = None):
    async with httpx.AsyncClient(timeout=12) as client:
        location = await locate_by_city(client, city) if city else await locate_by_ip(client, request)
        return await fetch_forecast(client, location)
