import pytest
from app.main import main


@pytest.mark.asyncio
async def test_main(mocker):
    # Мокируем асинхронные функции
    mock_init_db = mocker.patch('app.main.init_db', autospec=True)
    mocker.patch('app.main.get_db', autospec=True)

    # Вызываем основную функцию
    print("Calling main...")
    await main()
    print("Main has completed.")

    # Проверяем, что init_db был вызван
    mock_init_db.assert_awaited_once()
