from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_weather_returns_200():
    response = client.get("/weather?city=London")
    assert response.status_code == 200

def test_weather_response_has_correct_fields():
    response = client.get("/weather?city=London")
    data = response.json()
    assert "city" in data
    assert "country" in data
    assert "current" in data
    assert "daily" in data
    assert "hourly" in data

def test_weather_current_fields():
    response = client.get("/weather?city=London")
    current = response.json()["current"]
    assert "temperature" in current
    assert "feelsLike" in current
    assert "windSpeed" in current
    assert "condition" in current

def test_city_not_found():
    response = client.get("/weather?city=asdfghjkl123")
    assert response.status_code == 404