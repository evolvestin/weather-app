from app.models import WeatherData


def test_weather_data_model():
    weather = WeatherData(
        temperature=25.0,
        wind_speed=5.5,
        wind_direction='NE',
        pressure=1015.0,
        precipitation_type='rain',
        precipitation_amount=1.5
    )

    assert weather.temperature == 25.0
    assert weather.wind_direction == 'NE'
