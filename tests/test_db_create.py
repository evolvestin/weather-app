import pytest
from app.db_create import get_db


@pytest.mark.asyncio
async def test_get_db():
    async with get_db() as session:
        assert session is not None
