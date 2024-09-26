from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime

Base = declarative_base()  # Инициализируем базовый класс для моделей


class WeatherData(Base):
    """Модель данных о погоде, содержащая информацию о температуре, ветре, давлении и осадках"""

    __tablename__ = 'weather_data'  # Определяем имя таблицы

    id = Column(Integer, primary_key=True, autoincrement=True)  # Первичный ключ
    timestamp = Column(DateTime, default=datetime.utcnow)  # Время записи данных
    temperature = Column(Float)  # Температура
    wind_speed = Column(Float)  # Скорость ветра
    wind_direction = Column(String)  # Направление ветра
    pressure = Column(Float)  # Атмосферное давление
    precipitation_type = Column(String)  # Тип осадков
    precipitation_amount = Column(Float)  # Количество осадков
