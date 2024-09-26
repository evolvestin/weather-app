import typer
import pandas
import asyncio
from app.base import base_dir
from app.db_create import get_db
from app.db_storage import DbStorage

app = typer.Typer()  # Инициализируем интерфейс командной строки с помощью Typer


class Cli:
    """Класс для реализации командной строки и экспорта данных в Excel"""
    def __init__(self, db_storage: DbStorage):
        self.db_storage: DbStorage = db_storage

    async def export_to_excel(self):
        data = await self.db_storage.get_last_weather_data()  # Получаем последние данные о погоде из базы данных

        weather_data = [{
            'Timestamp': record.timestamp,
            'Temperature (°C)': record.temperature,
            'Wind Speed (m/s)': record.wind_speed,
            'Wind Direction': record.wind_direction,
            'Pressure (mm Hg)': record.pressure,
            'Precipitation Type': record.precipitation_type,
            'Precipitation Amount (mm)': record.precipitation_amount
        } for record in data]  # Формируем список данных для создания DataFrame

        df = pandas.DataFrame(weather_data)  # Создаем DataFrame с данными о погоде
        df.to_excel(base_dir.joinpath('weather_data.xlsx'), index=False)  # Сохраняем данные в файл Excel
        print('Data exported to weather_data.xlsx')  # Выводим сообщение об успешном экспорте


@app.command()
def export_to_excel(_):
    """Экспорт данных погоды в Excel через интерфейс командной строки"""
    asyncio.run(async_export_to_excel())  # Запускаем асинхронную функцию для экспорта данных


async def async_export_to_excel():
    """Асинхронная функция для получения сессии базы данных и экспорта данных в Excel"""
    async with get_db() as session:  # Открываем сессию базы данных
        db_storage = DbStorage(session)  # Инициализируем объект для работы с базой данных
        cli = Cli(db_storage)  # Создаем объект командной строки
        await cli.export_to_excel()  # Выполняем экспорт данных
        await db_storage.close()  # Закрываем сессию базы данных


if __name__ == '__main__':
    app()  # Запускаем интерфейс командной строки
