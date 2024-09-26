
import pytest
from app.models import Base
from app.db_storage import DbStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


@pytest.fixture
async def session():
    """Создаем движок для базы данных в памяти (SQLite)"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Создаем все таблицы

    # Создаем асинхронную сессию
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
        await session.close()


@pytest.mark.asyncio
async def test_save_weather_data(mocker, session):
    db_storage = DbStorage(session)

    # Мокаем метод commit у сессии
    mock_commit = mocker.patch.object(session, 'commit', autospec=True)

    weather_data = {
        'temperature': 20.0,
        'wind_speed': 5.0,
        'wind_direction': 'N',
        'pressure': 1012.0,
        'precipitation_type': 'rain',
        'precipitation_amount': 2.0
    }

    # Сохраняем данные в базу
    await db_storage.save_weather_data(weather_data)

    # Проверяем, что commit был вызван один раз
    mock_commit.assert_awaited_once()
