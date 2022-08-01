### Сервис созданя коротких ссылок

## 1. С помощью сервиса можно:
* Создать свой вариант замены для длинной ссылки (максимум 16 символов)
* Дать программе возможност придумать свой вариант (ровно 6 символов)
* Указать дату и время когда короткая ссылка должна перестать работать

Дату и время необходимо указать в формате: Год-Месяц-День Часы:минуты
## 2. Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AleksSpace/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Создать файл .env
```
touch .env
```
Записать в этот файл такие данные:
```
FLASK_APP= Имя вашего приложения
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3 - название базы данных
SECRET_KEY=WTF KEY - секретный ключ
```

Создать базу для сохранения данных
```
flask db upgrade
```
Запустить проект
```
flask run -h 0.0.0.0 -p 8000
```

## 3. Технологии

* Python 3.9.13
* Flask 2.0
* SQLAlchemy
* SQLite
* Bootstrap

Автор проекта: [Заикин Алексей](https://github.com/AleksSpace "GitHub аккаунт")
