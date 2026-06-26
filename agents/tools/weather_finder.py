import requests
from langchain_core.tools import tool

@tool
def weather_finder(latitude: float, longitude: float) -> str:
    """Find the current weather and 7-day forecast for a specific location using latitude and longitude.
    This is extremely useful when a user asks about the weather at their travel destination.
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current_weather", {})
        daily = data.get("daily", {})
        
        if not current:
            return "Weather data could not be retrieved."
            
        temp = current.get("temperature", "N/A")
        windspeed = current.get("windspeed", "N/A")
        
        result = f"Current Temperature: {temp}°C, Windspeed: {windspeed} km/h.\n\nForecast for next 7 days:\n"
        for i in range(len(daily.get("time", []))):
            date = daily["time"][i]
            max_temp = daily["temperature_2m_max"][i]
            min_temp = daily["temperature_2m_min"][i]
            precip = daily["precipitation_sum"][i]
            result += f"- {date}: {min_temp}°C to {max_temp}°C, Precipitation: {precip}mm\n"
            
        return result
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
