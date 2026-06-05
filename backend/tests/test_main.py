from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_weather_returns_200():
    response = client.get("/weather?city=London")
    assert response.status_code == 200

def test_weather_response_has_correct_fields():
    response = client.get("/weather?city=London")
    data = response.json()
    assert "city_name" in data
    assert "temperature_2m" in data
    assert "wind_speed_10m" in data