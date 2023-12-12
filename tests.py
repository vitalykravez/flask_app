import unittest
from app import create_app
from app.models import db, User, Entry

app = create_app()


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/test_flask_app'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page_requires_login(self):
        with self.app.application.app_context():
            response = self.app.get('/login')
            self.assertEqual(response.status_code, 200)

        with self.app.application.app_context():
            response = self.app.get('/')
            self.assertEqual(response.status_code, 302)  # Перенаправление, так как требуется вход в систему

    def test_index_page_with_login(self):
        # Создаем пользователя и входим в систему
        with app.test_request_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()

        self.app.post(
            '/login',
            data={'username': 'testuser', 'password': 'testpassword'},
            follow_redirects=True
        )

        # После входа в систему мы должны успешно получить доступ к главной странице
        with self.app.application.app_context():
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)

    def test_create_entry(self):
        # Создаем пользователя и входим в систему
        with app.test_request_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()

        self.app.post(
            '/login',
            data={'username': 'testuser', 'password': 'testpassword'},
            follow_redirects=True
        )

        # После входа в систему мы должны успешно создать запись
        with self.app.application.app_context():
            response = self.app.post(
                '/create',
                data={'title': 'Test Title', 'content': 'Test Content'},
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)

            # Вместо поиска конкретной строки HTML, проверим, что созданная запись появилась на странице
            self.assertIn(b'Test Title', response.data)
            self.assertIn(b'Test Content', response.data)

    # Добавить другие тесты для редактирования, удаления, регистрации, входа и т. д.


if __name__ == '__main__':
    unittest.main()
