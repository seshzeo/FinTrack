# FinTrack Backend

Backend часть приложения FinTrack. REST API построен на FastAPI, данные хранятся в MongoDB, доступ к базе выполняется асинхронно через PyMongo.

## Технологии

- Python 3.12
- FastAPI
- PyMongo с асинхронным API
- MongoDB
- Pydantic v2 и pydantic-settings
- Uvicorn
- pytest, pytest-asyncio и HTTPX для тестирования

## Требования

- Python 3.12
- Запущенный экземпляр MongoDB
- Git

## Установка

Команды ниже рассчитаны на PowerShell и запуск из корня репозитория.

Создайте виртуальное окружение:

```powershell
python -m venv .venv
```

Установите основные зависимости:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Для запуска тестов установите дополнительные зависимости:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-dev.txt
```

## Конфигурация

Создайте файл `.env` в каталоге `backend`, скопировав `.env.example`. Основные параметры:

| Переменная | Назначение | Значение по умолчанию |
|---|---|---|
| `APP_NAME` | Название приложения | `FinTrack` |
| `APP_ENV` | Окружение | `development` |
| `API_V1_PREFIX` | Префикс API | `/api/v1` |
| `MONGODB_URI` | Строка подключения MongoDB | `mongodb://127.0.0.1:27017` |
| `MONGODB_DATABASE` | Имя базы данных | `fintrack` |
| `CORS_ORIGINS` | Разрешённые источники CORS | `["http://localhost:5173"]` |

Пример значения `CORS_ORIGINS` в `.env`:

```dotenv
CORS_ORIGINS=["http://localhost:5173"]
```

Если frontend открыт с другого адреса или порта, добавьте его origin в список CORS.

## Запуск

Из каталога `backend`:

```powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

По умолчанию API будет доступен по адресу http://127.0.0.1:8000.

Для доступа к API из локальной сети можно запустить сервер с привязкой ко всем сетевым интерфейсам:

```powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0
```

## API

Префикс API по умолчанию — `/api/v1`.

| Метод | Маршрут | Назначение |
|---|---|---|
| GET | `/api/v1/health` | Проверка доступности API и MongoDB |
| GET | `/api/v1/categories` | Получение списка категорий |
| POST | `/api/v1/categories` | Создание пользовательской категории |
| PUT | `/api/v1/categories/{category_id}` | Переименование категории |
| DELETE | `/api/v1/categories/{category_id}` | Удаление пользовательской категории |
| GET | `/api/v1/transactions` | Получение списка операций |
| POST | `/api/v1/transactions` | Создание операции |
| GET | `/api/v1/transactions/{transaction_id}` | Получение операции по ID |
| PUT | `/api/v1/transactions/{transaction_id}` | Обновление операции |
| DELETE | `/api/v1/transactions/{transaction_id}` | Удаление операции |
| GET | `/api/v1/statistics/summary` | Получение сводной статистики |

### Фильтры списка операций

Для `GET /api/v1/transactions` доступны параметры:

- `type` — тип операции: `income` или `expense`.
- `category_id` — идентификатор категории.
- `date_from`, `date_to` — границы периода.
- `search` — поиск по описанию.
- `limit` — размер страницы (от 1 до 100, по умолчанию 50).
- `offset` — смещение (по умолчанию 0).

Для `GET /api/v1/statistics/summary` доступны параметры `date_from` и `date_to`.

Полные схемы запросов и ответов доступны в Swagger UI: http://127.0.0.1:8000/docs.

## Тестирование

Тесты находятся в каталоге `tests`. Перед запуском убедитесь, что MongoDB запущена.

Из каталога `backend` выполните:

```powershell
..\.venv\Scripts\python.exe -m pytest
```

Тестовая конфигурация использует отдельную базу `fintrack_test`. В фикстуре есть проверка имени базы: тесты прерываются, если подключение настроено на другую базу. Не удаляйте эту проверку и не направляйте тесты на рабочую базу данных.

## Структура backend

```text
backend/
├── app/
│   ├── api/v1/       # HTTP-маршруты категорий, операций и статистики
│   ├── core/         # Конфигурация приложения
│   ├── db/           # Подключение к MongoDB, индексы и начальные данные
│   ├── modules/
│   │   ├── categories/   # Логика и схемы категорий
│   │   ├── statistics/   # Расчёт статистики
│   │   └── transactions/ # Логика и схемы операций
│   └── main.py       # Создание FastAPI-приложения и lifespan
├── tests/            # Автоматические тесты API
├── .env.example
├── pytest.ini
├── requirements.txt
└── requirements-dev.txt
```

При запуске приложения выполняется подключение к MongoDB, создание индексов и инициализация стандартных категорий. При завершении приложения соединение с базой закрывается.
