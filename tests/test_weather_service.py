import pytest
from app.weather_service import WeatherService, WeatherClient


@pytest.mark.asyncio
async def test_get_and_save_weather(mocker):
    weather_client_mock = mocker.AsyncMock(WeatherClient)
    db_storage_mock = mocker.AsyncMock()

    weather_service = WeatherService(weather_client_mock, db_storage_mock)

    weather_client_mock.fetch_weather.return_value = {
        'current_weather': {
            'temperature': 22.5,
            'windspeed': 3.5,
            'winddirection': 45
        },
        'hourly': {
            'surface_pressure': [1013.0]
        }
    }

    await weather_service.get_and_save_weather()
    db_storage_mock.save_weather_data.assert_called_once()
