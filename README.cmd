# Flask CRUD Application

Это простое CRUD-приложение (Create, Read, Update, Delete), созданное на базе Python3.10,
Flask и SQLAlchemy, так же использующее PostgreSQL как БД для хранения данных.


## Перед началом:

Убедитесь, что на машине установлены:

- Python (version 3.x recommended)
- PostgreSQL

## Установка

1. Склонируйте репозиторий проекта с сайта github в свою рабочую директорию:

    ```bash
    https://github.com/vitalykravez/flask_app.git
    cd flask-crud-app
    ```

2. (Опционально) Создайте виртуальное окружение:

    ```bash
    python -m venv venv
    ```

3. Активируйте виртуальное окружение:

    - На Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - На Unix или MacOS:

        ```bash
        source venv/bin/activate
        ```

4. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Конфигурация

1. Создайте в PostgreSQL базу данных и замените в нужных местах данные, связанные с башей БД:


   '''postgresql://имя_пользователя:пароль@localhost/имя_бд'''

2. В рабочей директории запустите файл run.py:

    ```bash
    python run.py
    ```

3. Откройте браузер и посетите страницу http://localhost:5000.

## Использование

- Посетите [http://localhost:5000](http://localhost:5000) в браузере.
- Зарегистрируйтесь и залогиньтесь в системе.
- Используйте CRUD-функционал для управления системой.

## Тестирование

Запустите тесты с помощью следующей консольной команды:

```bash
python tests.py
'''

## Особенности приложения:

- Реализована аутентификация и авторизация пользователей
- Присутствует функционал резервного копирования данных в отдельный CSV-файл
- Добавлена интеграция с NASA API для просмотра ежедневно сменяющихся фотографий космоса
   (APOD - Astronomy Picture of the Day)


## Мысли автора по теме:

Данный проект создан за короткий срок и является скорее демонстрацией разносторонних
возможностей к обучению и развитию, нежели как готовый и полностью функционирующий продукт.
Ниже вкратце изложена лишь небольшая часть вероятных улучшений:
    - Более тщательная обработка ошибок
    - Работа с миграциями БД
    - Хэширование данных для обеспечения должной безопасности
    - Более глубокая проработка функционала
    - и т.д. и т.п.

Автор открыт к любому фидбэку и будет рад конструктивной критике.