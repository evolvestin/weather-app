from app.models import WeatherData
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class DbStorage:
    """Класс для работы с базой данных, содержащей данные о погоде"""

    def __init__(self, session: AsyncSession):
        """Инициализация сессии базы данных"""
        self.session: AsyncSession = session  # Сохраняем сессию базы данных

    async def save_weather_data(self, weather_data: dict):
        """Сохранение новых данных о погоде в базу данных"""
        new_weather_entry = WeatherData(
            temperature=weather_data['temperature'],
            wind_speed=weather_data['wind_speed'],
            wind_direction=weather_data['wind_direction'],
            pressure=weather_data['pressure'],
            precipitation_type=weather_data['precipitation_type'],
            precipitation_amount=weather_data['precipitation_amount']
        )  # Создаем новую запись на основе переданных данных
        self.session.add(new_weather_entry)  # Добавляем запись в сессию
        await self.session.commit()  # Коммитим изменения в базе данных

    async def get_last_weather_data(self, limit: int = 10):
        """Получение последних записей о погоде из базы данных"""
        result = await self.session.execute(
            select(WeatherData)
            .order_by(WeatherData.timestamp.desc())
            .limit(limit)
        )  # Выполняем запрос для получения данных о погоде, сортируя по времени
        return result.scalars().all()  # Возвращаем все результаты

    async def close(self):
        """Закрытие сессии базы данных"""
        await self.session.close()  # Закрываем сессию
