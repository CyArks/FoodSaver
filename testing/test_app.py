<<<<<<< HEAD:code/test_app.py
import unittest
from your_app_name import create_app, db

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        tester = self.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Your App!', response.data)

# Additional tests can be added here

if __name__ == "__main__":
    unittest.main()
=======
import unittest
from app import create_app, db


class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        tester = self.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Your App!', response.data)

# Additional tests can be added here


if __name__ == "__main__":
    unittest.main()
>>>>>>> b2281d0f31a00b7a805a9cd78fa2455b23fec8b5:testing/test_app.py
