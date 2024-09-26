import asyncio
from app.db_storage import DbStorage
from app.db_create import init_db, get_db
from app.weather_service import WeatherService, WeatherClient


async def main():
    """Главная асинхронная функция для запуска процесса сбора данных о погоде"""
    await init_db()  # Инициализируем базу данных, создавая необходимые таблицы

    async with get_db() as session:  # Открываем сессию базы данных
        db_storage = DbStorage(session)  # Создаем объект для работы с базой данных
        weather_client = WeatherClient()  # Инициализируем клиент для получения данных о погоде
        weather_service = WeatherService(weather_client, db_storage)  # Создаем сервис для работы с погодными данными

        try:
            await weather_service.start_fetching_weather()  # Запускаем процесс получения и сохранения данных о погоде
        except Exception as error:
            print(f'An error occurred: {error}')  # Обрабатываем возможные ошибки
        finally:
            await db_storage.close()  # Закрываем сессию базы данных после завершения работы


if __name__ == '__main__':
    asyncio.run(main())  # Запускаем асинхронную функцию при выполнении скрипта
