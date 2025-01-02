import requests
import pytest
from jsonschema import validate

API_KEY = "df9c078dbfbe1a3e5232c6872383fe78"

# Test 1: 5-Day Weather Forecast
def test_weather_forecast():
    params = {
        'q': 'Jakarta Selatan',
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params)

    assert response.status_code == 200
    data = response.json()
    assert 'list' in data
    assert len(data['list']) > 0
    
    forecast_schema = {
        "type": "object",
        "properties": {
            "list": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "dt": {"type": "integer"},
                        "main": {
                            "type": "object",
                            "properties": {
                                "temp": {"type": "number"},
                                "temp_min": {"type": "number"},
                                "temp_max": {"type": "number"},
                            },
                            "required": ["temp", "temp_min", "temp_max"]
                        },
                        "weather": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "description": {"type": "string"},
                                },
                                "required": ["description"]
                            }
                        }
                    },
                    "required": ["dt", "main", "weather"]
                }
            }
        },
        "required": ["list"]
    }
    
    validate(instance=data, schema=forecast_schema)

# Test 2: Current Air Pollution
def test_air_pollution():
    params = {
        'q': 'Jakarta Selatan',
        'appid': API_KEY
    }
    response = requests.get("https://api.openweathermap.org/data/2.5/air_pollution", params=params)

    assert response.status_code == 200
    data = response.json()
    assert 'list' in data
    assert len(data['list']) > 0
    
    pollution_schema = {
        "type": "object",
        "properties": {
            "list": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "main": {
                            "type": "object",
                            "properties": {
                                "aqi": {"type": "integer"}
                            },
                            "required": ["aqi"]
                        }
                    },
                    "required": ["main"]
                }
            }
        },
        "required": ["list"]
    }
    
    validate(instance=data, schema=pollution_schema)
