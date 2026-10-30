# FinTrack

FinTrack — веб-приложение для учёта личных финансов. Позволяет управлять категориями доходов и расходов, создавать и редактировать финансовые операции, фильтровать историю и просматривать сводную статистику.

## Возможности

- Учёт доходов и расходов: создание, просмотр, редактирование и удаление операций.
- Категории: просмотр стандартных категорий и управление пользовательскими.
- Фильтрация операций по типу, категории и периоду.
- Поиск операций по описанию и пагинация списка.
- Сводная статистика: доходы, расходы, баланс и количество операций.
- Распределение расходов по категориям в интерфейсе.
- API статистики поддерживает фильтрацию по периоду.

## Технологии

**Backend:** Python 3.12, FastAPI, PyMongo (async), MongoDB, Pydantic v2, Uvicorn.

**Frontend:** React, JavaScript, Vite, CSS, Fetch API.

## Требования

- Python 3.12
- MongoDB
- Node.js 20 или совместимая версия
- npm
- Git

## Установка и запуск

### 1. Клонирование репозитория

```powershell
git clone https://github.com/seshzeo/FinTrack.git
cd FinTrack
```

### 2. Backend

Создайте виртуальное окружение в корне проекта и установите зависимости:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Создайте `backend/.env` на основе `backend/.env.example`. Убедитесь, что MongoDB запущена.

Запустите API из каталога backend:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Подробная информация о backend, настройках и тестах находится в [backend/README.md](backend/README.md).

### 3. Frontend

Откройте второй терминал из корня проекта:

```powershell
cd frontend
npm install
npm run dev
```

По умолчанию Vite запускает frontend на `http://localhost:5173`.

Чтобы открыть frontend с других устройств в локальной сети, используйте:

```powershell
npm run dev -- --host 0.0.0.0
```

Адрес в локальной сети Vite выведет в терминал. Backend при этом должен быть запущен отдельно.

## API и документация

После запуска backend доступны:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Проверка состояния: http://127.0.0.1:8000/health

Основные маршруты API:

| Метод | Маршрут | Назначение |
|---|---|---|
| GET | `/api/v1/categories` | Получение категорий |
| POST | `/api/v1/categories` | Создание пользовательской категории |
| PUT | `/api/v1/categories/{category_id}` | Переименование категории |
| DELETE | `/api/v1/categories/{category_id}` | Удаление пользовательской категории |
| GET | `/api/v1/transactions` | Список операций, фильтры и пагинация |
| POST | `/api/v1/transactions` | Создание операции |
| GET | `/api/v1/transactions/{transaction_id}` | Получение операции |
| PUT | `/api/v1/transactions/{transaction_id}` | Обновление операции |
| DELETE | `/api/v1/transactions/{transaction_id}` | Удаление операции |
| GET | `/api/v1/statistics/summary` | Сводная статистика |

Параметры фильтрации и форматы запросов описаны в Swagger UI.

## Структура проекта

```text
FinTrack/
├── backend/       # FastAPI, работа с MongoDB и тесты
├── frontend/      # React-приложение
├── .venv/         # виртуальное окружение Python
└── README.md
```
