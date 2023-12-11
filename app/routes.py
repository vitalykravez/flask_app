from flask import Response, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from typing import Optional, List, Dict, Any

import requests
import csv


from app.models import db, User, Entry


def init_app(app):

    login_manager: LoginManager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id: int) -> Optional[User]:
        return User.query.get(int(user_id))

    @app.route('/')
    @login_required
    def index() -> Any:
        entries: List[Entry] = Entry.query.filter_by(user_id=current_user.id).all()
        return render_template('index.html', entries=entries)

    @app.route('/create', methods=['GET', 'POST'])
    @login_required
    def create() -> Any:
        if request.method == 'POST':
            title: str = request.form.get('title')
            content: str = request.form.get('content')

            new_entry: Entry = Entry(title=title, content=content, user_id=current_user.id)
            db.session.add(new_entry)
            db.session.commit()
            flash('Entry created successfully!', 'success')
            return redirect(url_for('index'))

        return render_template('create.html')

    @app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
    @login_required
    def edit(entry_id: int) -> Any:
        entry = Entry.query.get(entry_id)

        if entry.user_id != current_user.id:
            flash('You are not authorized to edit this entry.', 'danger')
            return redirect(url_for('index'))

        if request.method == 'POST':
            entry.title = request.form.get('title')
            entry.content = request.form.get('content')

            db.session.commit()
            flash('Entry updated successfully!', 'success')
            return redirect(url_for('index'))

        return render_template('edit.html', entry=entry)

    @app.route('/delete/<int:entry_id>')
    @login_required
    def delete(entry_id: int) -> Any:
        entry: Entry = Entry.query.get(entry_id)

        if entry.user_id != current_user.id:
            flash('You are not authorized to delete this entry.', 'danger')
            return redirect(url_for('index'))

        db.session.delete(entry)
        db.session.commit()
        flash('Entry deleted successfully!', 'success')
        return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login() -> Any:
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username: str = request.form.get('username')
            password: str = request.form.get('password')

            user: Optional[User] = User.query.filter_by(username=username).first()

            if user and user.password == password:  # В реальном приложении следует использовать хэширование паролей
                login_user(user)
                next_page: Optional[str] = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Login unsuccessful. Please check your username and password.', 'danger')

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register() -> Any:
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username: str = request.form.get('username')
            password: str = request.form.get('password')

            new_user: User = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout() -> Any:
        logout_user()
        return redirect(url_for('login'))

    @app.route('/apod')
    @login_required
    def apod() -> Any:
        apod_data: Optional[Dict[str, Any]] = get_apod_data()
        return render_template('apod.html', apod_data=apod_data)

    def get_apod_data() -> Optional[Dict[str, Any]]:
        api_key: str = 'EC326fP95y9mGM8eu39G2Xa4kJLfKw4V0LVyaBDh'  # Получите свой API ключ на https://api.nasa.gov/
        api_url: str = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'

        try:
            response: requests.Response = requests.get(api_url)
            response.raise_for_status()
            data: Dict[str, Any] = response.json()
            return data
        except requests.RequestException as e:
            flash(f'Error fetching APOD data: {e}', 'danger')
            return None

    @app.route('/backup_csv')
    @login_required
    def backup_csv():
        entries: list[Any] = Entry.query.filter_by(user_id=current_user.id).all()

        # Путь к файлу CSV, в который будут выгружены данные
        csv_filename: str = 'backup.csv'

        # Заголовки CSV-файла
        csv_headers: list[str] = ['id', 'title', 'content', 'user_id']

        # Подготовка данных для записи в CSV
        data: list = [[entry.id, entry.title, entry.content, entry.user_id] for entry in entries]

        # Создание CSV-файла
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Запись заголовков
            csv_writer.writerow(csv_headers)

            # Запись данных
            csv_writer.writerows(data)

        # Отправка файла пользователю
        with open(csv_filename, 'r') as csv_file:
            response = Response(csv_file.read(), mimetype='text/csv')
            response.headers["Content-Disposition"] = f"attachment; filename={csv_filename}"
            return response
