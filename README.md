# Домашняя финансовая система (MVP)

> ⚠️ **Внимание:** Для работы OCR необходим установленный [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract). После установки убедитесь, что путь к tesseract.exe добавлен в переменную среды PATH.

---

## Быстрый запуск (Windows)

1. Установите [Python 3.10+](https://www.python.org/downloads/)
2. Установите [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) и добавьте путь к tesseract.exe в PATH
3. Откройте командную строку в папке проекта и выполните:
   ```bat
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Запустите приложение:
   ```bat
    python finance_app/ui/main.py
   ```

---

## Сборка Windows-exe

1. Установите зависимости:
   ```bat
   pip install -r requirements.txt
   ```
2. Соберите exe:
   ```bat
   build.bat
   ```
3. В папке dist/ появится `finance.exe` — двойной клик, и приложение готово.

---

## Добавление новых правил категоризации

1. Создайте JSON-файл с шаблонами:
   ```json
   {
     "Magnit|Пятёрочка": "Еда",
     "Yandex\\.Taxi": "Транспорт"
   }
   ```
2. В GUI нажмите "Загрузить правила из JSON" и выберите файл.

---

## Тесты

```bat
pytest
```

---

## Структура
- finance_app/data/parser.py — OCR и парсинг выписок
- finance_app/db/models.py — SQLAlchemy-модели
- finance_app/logic/categorizer.py — категоризация
- finance_app/ui/main.py — GUI
- finance_app/analytics/reports.py — отчёты
- tests/ — тесты
