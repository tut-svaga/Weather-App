import httpx
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="Weather DevOps Service")

# Валидация выходных данных
class JsonWeather(BaseModel):
    city_name: str
    temperature_2m: float
    wind_speed_10m: float

# ==========================================
# ЯДРО: Единая функция запроса погоды по коордам
# ==========================================
async def fetch_weather(client: httpx.AsyncClient, lat: float, lon: float, city_name: str) -> JsonWeather:
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto"
    }
    
    response = await client.get(weather_url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Open-Meteo API error")
        
    data = response.json()
    current_data = data["current"]
    
    return JsonWeather(
        city_name=city_name,
        temperature_2m=current_data["temperature_2m"],
        wind_speed_10m=current_data["wind_speed_10m"]
    )

# ==========================================
# ДИСПЕТЧЕР: Основной эндпоинт
# ==========================================
@app.get("/weather")
async def get_weather(request: Request, city: str = None):
    async with httpx.AsyncClient() as client:
        
        # СЦЕНАРИЙ 1: Пользователь сам передал город (?city=Tiraspol)
        if city:
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_params = {"name": city, "count": 1, "language": "ru", "format": "json"}
            
            geo_response = await client.get(geo_url, params=geo_params)
            if geo_response.status_code != 200:
                raise HTTPException(status_code=500, detail="Geocoding service error")
                
            geo_data = geo_response.json()
            if "results" not in geo_data or not geo_data["results"]:
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")
                
            location = geo_data["results"][0]
            return await fetch_weather(
                client=client, 
                lat=location["latitude"], 
                lon=location["longitude"], 
                city_name=location.get("name", city)
            )
            
        # СЦЕНАРИЙ 2: Город не передан, вычисляем по IP
        else:
            client_ip = request.client.host
            
            # DevOps-заглушка: ip-api.com не умеет в локальные IP (127.0.0.1 или 192.168.x.x)
            if client_ip in ("127.0.0.1", "localhost") or client_ip.startswith("192.168."):
                client_ip = "178.17.173.1" # Дефолтный внешний IP для тестов локально
                
            ip_url = f"http://ip-api.com/json/{client_ip}?lang=ru"
            ip_response = await client.get(ip_url)
            if ip_response.status_code != 200:
                raise HTTPException(status_code=500, detail="IP Geolocation service error")
                
            ip_data = ip_response.json()
            if ip_data.get("status") == "fail":
                raise HTTPException(status_code=400, detail=f"Failed to locate IP: {ip_data.get('message')}")
                
            return await fetch_weather(
                client=client, 
                lat=ip_data["lat"], 
                lon=ip_data["lon"], 
                city_name=ip_data.get("city", "Defined by IP")
            )