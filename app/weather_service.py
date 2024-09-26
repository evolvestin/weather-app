import aiohttp
import asyncio
from app.db_storage import DbStorage


def get_wind_direction(degrees: float):
    """Функция для преобразования углов в градусах в направление ветра"""
    if degrees is None:
        return None
    if 337.5 <= degrees <= 360 or 0 <= degrees < 22.5:
        return 'С'  # Север
    elif 22.5 <= degrees < 67.5:
        return 'СВ'  # Северо-Восток
    elif 67.5 <= degrees < 112.5:
        return 'В'  # Восток
    elif 112.5 <= degrees < 157.5:
        return 'ЮВ'  # Юго-Восток
    elif 157.5 <= degrees < 202.5:
        return 'Ю'  # Юг
    elif 202.5 <= degrees < 247.5:
        return 'ЮЗ'  # Юго-Запад
    elif 247.5 <= degrees < 292.5:
        return 'З'  # Запад
    elif 292.5 <= degrees < 337.5:
        return 'СЗ'  # Северо-Запад


class WeatherClient:
    """Клиент для получения данных о погоде через API"""

    API_URL = 'https://api.open-meteo.com/v1/forecast'  # URL для получения данных о погоде

    async def fetch_weather(self):
        """Асинхронный метод для запроса данных о погоде с помощью API"""
        params = {
            'forecast_days': 1,  # Указываем прогноз на 1 день
            'latitude': 55.698520,  # Широта Сколтеха
            'longitude': 37.359490,  # Долгота Сколтеха
            'current_weather': 'true',  # Запрашиваем текущие погодные условия
            'hourly': 'surface_pressure',  # Запрашиваем данные о давлении
        }
        async with aiohttp.ClientSession() as session:  # Открываем сессию HTTP
            async with session.get(self.API_URL, params=params) as response:  # Отправляем GET-запрос
                return await response.json()  # Возвращаем JSON-ответ


class WeatherService:
    """Сервис для взаимодействия с погодным клиентом и базой данных"""

    def __init__(self, weather_client: WeatherClient, db_storage: DbStorage):
        """Инициализируем сервис с клиентом и хранилищем данных"""
        self.weather_client = weather_client  # Клиент для получения данных о погоде
        self.db_storage: DbStorage = db_storage  # Хранилище данных

    async def get_and_save_weather(self):
        """Получение данных о погоде и сохранение их в базу данных"""
        weather_data = await self.weather_client.fetch_weather()  # Получаем данные о погоде
        current_weather = weather_data.get('current_weather', {})  # Извлекаем текущие данные о погоде
        hourly_data = weather_data.get('hourly', {})  # Извлекаем данные о давлении
        pressure_data = hourly_data.get('surface_pressure', [None])[0]  # Получаем значение давления

        # Формируем новую запись для базы данных
        new_weather_entry = {
            'temperature': current_weather['temperature'],
            'wind_speed': current_weather['windspeed'],
            'wind_direction': get_wind_direction(current_weather['winddirection']),
            'pressure': pressure_data or 0,
            'precipitation_type': current_weather.get('precipitation_type', 'none'),
            'precipitation_amount': current_weather.get('precipitation_amount', 0)
        }
        await self.db_storage.save_weather_data(new_weather_entry)  # Сохраняем запись в базу данных

    async def start_fetching_weather(self, interval: int = 180):
        """Запуск цикла получения данных о погоде с интервалом в 180 секунд"""
        while True:
            await self.get_and_save_weather()  # Получаем и сохраняем данные о погоде
            await asyncio.sleep(interval)  # Задержка между запросами
