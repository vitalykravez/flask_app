import unittest
from flask import url_for
from app import create_app
from app.models import db, User, Entry


app = create_app()


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/test_flask_app'
        self.app = app.test_client()
        with app.test_request_context():
            db.create_all()

    def tearDown(self):
        with app.test_request_context():
            db.session.remove()
            db.drop_all()

    def test_index_page_requires_login(self):
        response = self.app.get(url_for('index'))
        self.assertEqual(response.status_code, 302)  # Перенаправление, так как требуется вход в систему

    def test_index_page_with_login(self):
        # Создаем пользователя и входим в систему
        with app.test_request_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
        self.app.post(
            url_for('login'),
            data={'username': 'testuser', 'password': 'testpassword'},
            follow_redirects=True
        )

        # После входа в систему мы должны успешно получить доступ к главной странице
        response = self.app.get(url_for('index'))
        self.assertEqual(response.status_code, 200)

    def test_create_entry(self):
        # Создаем пользователя и входим в систему
        with app.test_request_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
        self.app.post(
            url_for('login'),
            data={'username': 'testuser', 'password': 'testpassword'},
            follow_redirects=True
        )

        # После входа в систему мы должны успешно создать запись
        response = self.app.post(
            url_for('create'),
            data={'title': 'Test Title', 'content': 'Test Content'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Entry created successfully!', response.data)
        self.assertIn(b'Test Title', response.data)
        self.assertIn(b'Test Content', response.data)

    # Добавить другие тесты для редактирования, удаления, регистрации, входа и т. д.


if __name__ == '__main__':
    unittest.main()
