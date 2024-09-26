## Документация к тестовому проекту

### Описание проекта
- Данный проект представляет собой Python-скрипт для автоматического сбора данных о погоде в районе Сколтеха и сохранения их в базу данных.
- Скрипт также поддерживает экспорт последних 10 записей о погоде в файл формата .xlsx через командную строку. 
- Проект использует асинхронные запросы к API для получения данных о текущей погоде.

### Основные функции:
1. **Сбор данных о погоде**: Запросы к API для получения информации о текущей температуре, ветре, давлении и осадках. 
Данные автоматически сохраняются в базе данных через заданные промежутки времени.
2. **Экспорт данных в Excel**: Возможность экспорта последних 10 записей из базы данных в файл `.xlsx` без прерывания 
процесса сбора данных.
3. **Асинхронная обработка**: Асинхронные запросы к API и работа с базой данных с использованием библиотеки SQLAlchemy 
и асинхронных функций.

### Структура проекта
- `app/base.py`: Определяет корневую директорию проекта.
- `app/cli.py`: Командный интерфейс для экспорта данных в Excel.
- `app/db_create.py`: Логика создания и инициализации базы данных.
- `app/db_storage.py`: Класс для работы с базой данных.
- `app/main.py`: Основной скрипт для запуска процесса сбора данных.
- `app/models.py`: Определение модели данных о погоде.
- `app/weather_service.py`: Сервис для взаимодействия с API и хранения данных о погоде.
- `tests/`: Директория с тестами для проверки функциональности API.

### Используемые технологии:
- **Python 3**: Язык программирования.
- **Typer**: Библиотека для создания интерфейса командной строки.
- **SQLAlchemy (asyncio)**: ORM для работы с базой данных.
- **aiohttp**: Асинхронный HTTP-клиент для запросов к API.
- **Pandas**: Для работы с Excel-файлами.

### Установка и настройка
#### Требования
- Python 3.8 или выше
- Установленные зависимости из файла requirements.txt

#### Шаги по установке
1. Клонирование репозитория:
```bash
git clone https://github.com/evolvestin/weather-app.git
cd <папка проекта>
```
2. Установка зависимостей:
```bash
pip3 install -r requirements.txt
```
3. Запуск основного скрипта:
```bash
python app/main.py
```
#### Экспорт данных в Excel
Для экспорта последних 10 записей о погоде из базы данных в файл `.xlsx` выполните команду:
```bash
python app/cli.py export_to_excel
```
Файл `weather_data.xlsx` будет сохранен в корневую папку проекта.

### Примечания
- Данные собираются каждые 3 минуты. Этот интервал можно изменить в файле `app/weather_service.py`, 
изменив параметр `interval` в методе `start_fetching_weather`.
- Скрипт поддерживает асинхронную работу с базой данных, 
что позволяет экспортировать данные без остановки процесса сбора данных.