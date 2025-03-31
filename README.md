# Django Order Management System

##  Описание проекта
Веб-приложение для управления заказами в кафе на Django. Позволяет добавлять, редактировать, удалять и просматривать заказы.

## Функции
- Добавление нового заказа
- Поиск заказов по номеру стола и статусу
- Изменение статуса заказа ("в ожидании", "готово", "оплачено")
- Удаление заказа
- Подсчет выручки за смену
- REST API для работы с заказами

---

## Установка и запуск

###  Клонирование репозитория
```bash
git clone https://github.com/ТВОЙ_РЕПОЗИТОРИЙ.git
cd ТВОЙ_РЕПОЗИТОРИЙ
```

### Создание и активация виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate    # Для Windows
```

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Применение миграций
```bash
python manage.py migrate
```

### Запуск сервера
```bash
python manage.py runserver
```
Открыть в браузере: [http://127.0.0.1:8001/](http://127.0.0.1:8001/)

---

## Использование API

### Добавить заказ (POST `/api/orders/`)
Пример JSON-запроса:
```json
{
    "table_number": 5,
    "items": {"Пицца": 1200, "Пепси": 600},
    "total_price": 1800,
    "status": "pending"
}
```

### Получить список заказов (GET `/api/orders/`)

### Изменить заказ (PUT/PATCH `/api/orders/{id}/`)

### Удалить заказ (DELETE `/api/orders/{id}/`)

---

##  Технологии
- Python 3.8+
- Django 5+
- Django REST Framework
- HTML/CSS (шаблоны)
- SQLite/PostgreSQL

---


## Автор
Разработала **Aida Kozhabekkyzy**. 

