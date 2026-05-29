import requests
from pydantic import BaseModel
from fastapi import FastAPI, Response

app = FastAPI()

class JsonWeather (BaseModel):
    temperature_2m : float
    wind_speed_10m : float

@app.get("/weather")
def meteo(lat: float = 52.52 , lon: float = 13.41):
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto" 
    }
    
    response = requests.get(url,params=params)
    if response.status_code == 200:
        data = response.json()
        current_data = data["current"]
        weather = JsonWeather(**current_data)
        return weather
    return {"error": "Ошибка запроса к Open-meteo", "code": response.status_code}
    
