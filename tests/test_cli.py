import pytest
from app.cli import Cli
from app.db_storage import DbStorage


@pytest.mark.asyncio
async def test_export_to_excel(mocker):
    db_storage_mock = mocker.AsyncMock(DbStorage)
    cli = Cli(db_storage=db_storage_mock)

    await cli.export_to_excel()
    db_storage_mock.get_last_weather_data.assert_called_once()
