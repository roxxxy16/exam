# Создание базы данных

## Вариант А — PostgreSQL через psql (основной)

Открой `cmd` и выполни:

```cmd
set PGPASSWORD=твой_пароль_от_postgres
"C:\postresql\bin\psql.exe" -U postgres -h localhost
```

После входа в psql выполни:

```sql
CREATE DATABASE vodit_rf;
\l
\q
```

`\l` покажет список баз — там должна быть `vodit_rf`.
`\q` — выйти из psql.

**Одной строкой без входа в psql:**

```cmd
set PGPASSWORD=твой_пароль
"C:\postresql\bin\psql.exe" -U postgres -h localhost -c "CREATE DATABASE vodit_rf;"
```

Затем в `vodit_rf/settings.py` укажи свой пароль в блоке `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vodit_rf',
        'USER': 'postgres',
        'PASSWORD': 'твой_пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Вариант Б — MySQL через XAMPP / phpMyAdmin (запасной)

1. Запусти **XAMPP Control Panel** → нажми **Start** напротив **Apache** и **MySQL**.
2. Открой в браузере: <http://localhost/phpmyadmin>
3. Слева нажми **Создать БД (New)** → введи имя `vodit_rf` → кодировка `utf8mb4_general_ci` → кнопка **Create**.

Установи драйвер MySQL:

```bash
pip install mysqlclient
```

Если `mysqlclient` не ставится — поставь `PyMySQL`:

```bash
pip install pymysql
```

И в самом верху файла `vodit_rf/__init__.py` добавь:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

Затем в `vodit_rf/settings.py` замени блок `DATABASES` на:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vodit_rf',
        'USER': 'root',
        'PASSWORD': '',          # в XAMPP по умолчанию пароля нет
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```
