# 👁️ Досье сотрудника

Трекер глупых вопросов и просмотра сериалов. Flask + PostgreSQL.

---

## Быстрый старт

### 1. Установка PostgreSQL (если не установлен)
Скачай с https://www.postgresql.org/download/windows/ и установи.
Запомни пароль для пользователя `postgres`.

### 2. Создание базы данных
Открой **pgAdmin** или **psql** и выполни:
```sql
CREATE DATABASE employee_tracker;
```

### 3. Запуск приложения
Просто дважды кликни на `start.bat` — он всё сделает сам:
- создаст виртуальное окружение Python
- установит зависимости
- запросит параметры БД
- запустит сервер

### 4. Открой в браузере
```
http://localhost:5000
```

---

## Ручной запуск (через CMD)

```cmd
cd C:\путь\до\employee_tracker

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

set DATABASE_URL=postgresql://postgres:ВАШ_ПАРОЛЬ@localhost:5432/employee_tracker
python app.py
```

---

## Доступ с других устройств в сети

После запуска узнай IP ноутбука:
```cmd
ipconfig
```
Найди строку `IPv4 Address` — например `192.168.1.50`.

Открой на любом устройстве в той же сети:
```
http://192.168.1.50:5000
```

---

## Структура проекта

```
employee_tracker/
├── app.py            ← Flask приложение + API
├── requirements.txt  ← Зависимости Python
├── start.bat         ← Скрипт запуска для Windows
├── README.md         ← Эта инструкция
└── templates/
    └── index.html    ← Весь фронтенд (HTML + CSS + JS)
```

---

## API endpoints

| Метод | URL | Описание |
|-------|-----|---------|
| GET | /api/questions | Список всех вопросов |
| POST | /api/questions | Добавить вопрос |
| DELETE | /api/questions/:id | Удалить вопрос |
| GET | /api/series | Список просмотров |
| POST | /api/series | Добавить просмотр |
| DELETE | /api/series/:id | Удалить запись |
| GET | /api/stats | Общая статистика |
