# Nanoparticles Accumulation Analysis API

Проект предоставляет REST API для анализа данных о накоплении наночастиц в органах лабораторных мышей для реализации лечения глиомы.
В данном проекте представлен результат работы программного обеспечения для автоматизированного анализа и визуализации данных о распределении наночастиц в органах лабораторных животных с целью:

- Оптимизации доклинических исследований
- Сравнительного анализа эффективности различных типов наночастиц
- Упрощения обработки экспериментальных данных

## Технологии

- Python 3.10+
- FastAPI
- SQLite
- SQLAlchemy 2.0
- Uvicorn

## Установка

1. Клонируете репозиторий:
```bash
git clone https://github.com/ваш-username/nanoparticles-api.git
cd nanoparticles-api
Создайте и активируйте виртуальное окружение:

bash
python -m venv venv
venv\Scripts\activate
Установите зависимости:

bash
pip install -r requirements.txt

Настройка
Импортируйте данные из Excel:

bash
python import_data.py data.xlsx
Создайте файл .env (по образцу .env.example):

ini
DATABASE_URL=sqlite:///./nanoparticles.db
SECRET_KEY=your-secret-key

Запуск
bash
uvicorn app.main:app --reload
Сервер будет доступен по адресу: http://127.0.0.1:8000"# brainAPI" 
