# Водить.РФ — портал записи на курсы вождения речного транспорта

Информационная система демо-экзамена 09.02.07 (вариант В1).
Стек: **Python 3 · Django · PostgreSQL (psycopg2-binary) · HTML/CSS · Bootstrap 5**.

## Функционал

- Регистрация пользователя с валидацией (логин — латиница и цифры, ≥6 символов; пароль ≥8).
- Авторизация с информативными сообщениями об ошибках.
- Личный кабинет: история заявок + отзывы (после смены статуса администратором).
- Оформление заявки: вид транспорта, дата начала, способ оплаты — через выпадающие списки.
- Панель администратора (логин `Admin26` / пароль `Demo20`) с фильтрами, поиском,
  сортировкой и постраничной навигацией.
- Слайдер с 4 изображениями, авто-смена каждые 3 секунды, стрелки вперёд/назад.
- Мобильная адаптация под 390×844, микроанимации.

## Запуск

```bash
pip install -r requirements.txt

# создать БД vodit_rf в PostgreSQL (user: postgres / pass: postgres)
# или временно переключиться на SQLite в vodit_rf/settings.py

python manage.py migrate
python manage.py createsuperuser  # для /admin/
python manage.py runserver
```

## Создание пользователя-администратора Admin26

```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_superuser('Admin26', 'admin@vodit.rf', 'Demo20')
```

## Структура

- `vodit_rf/` — настройки проекта
- `main/` — модели (Profile, Application, Review), формы, представления, URL'ы
- `main/templates/main/` — шаблоны Bootstrap
- `static/css/app.css` — стили, анимации, мобильная адаптация
