from app.models import Base
from app.base import base_dir
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

db_path = base_dir.joinpath('weather.db')  # Определяем путь к файлу базы данных
engine = create_async_engine(f'sqlite+aiosqlite:///{db_path}', echo=True)  # Создаем асинхронный движок бд SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
# Создаем фабрику сессий для работы с базой данных


async def init_db():
    """Асинхронная функция для инициализации базы данных"""
    async with engine.begin() as conn:  # Открываем подключение к базе данных
        await conn.run_sync(Base.metadata.create_all)  # Выполняем создание всех таблиц в базе данных


@asynccontextmanager
async def get_db():
    """Контекстный менеджер для получения сессии базы данных"""
    async with SessionLocal() as session:  # Открываем новую сессию
        try:
            yield session  # Возвращаем сессию для выполнения операций
        finally:
            await session.close()  # Закрываем сессию после использования
