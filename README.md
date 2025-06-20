# Домашняя финансовая система (MVP)

## Установка и запуск (локально)

```bash
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate для Windows
pip install -r requirements.txt
```

## Миграции Alembic

```bash
alembic init db/migrations  # только при первом запуске, если нет папки
# Проверьте, что в db/migrations/env.py используется metadata из db.models
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## Запуск приложения и тестов

```bash
pytest && alembic upgrade head && python ui/main.py
```

## Docker

```bash
docker-compose build
docker-compose up
```

## Добавление новых правил категоризации

1. Создайте JSON-файл с шаблонами:
   ```json
   {
     "Magnit|Пятёрочка": "Еда",
     "Yandex\\.Taxi": "Транспорт"
   }
   ```
2. В GUI нажмите "Загрузить правила из JSON" и выберите файл.

## Тесты

```bash
pytest
```

## Структура
- data/parser.py — OCR и парсинг выписок
- db/models.py — SQLAlchemy-модели
- logic/categorizer.py — категоризация
- ui/main.py — GUI
- analytics/reports.py — отчёты
- tests/ — тесты 