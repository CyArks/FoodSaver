<<<<<<< HEAD:code/test_permissions.py
import unittest
from your_app_name.permissions import has_permission
from unittest.mock import patch  # Added for mocking


class TestPermissions(unittest.TestCase):
    
    def test_has_permission_admin(self):
        self.assertTrue(has_permission("admin", "read"))
        self.assertTrue(has_permission("admin", "write"))
        self.assertTrue(has_permission("admin", "delete"))
    
    def test_has_permission_user(self):
        self.assertTrue(has_permission("user", "read"))
        self.assertFalse(has_permission("user", "write"))
        self.assertFalse(has_permission("user", "delete"))
    
    def test_has_permission_guest(self):
        self.assertFalse(has_permission("guest", "read"))
        self.assertFalse(has_permission("guest", "write"))
        self.assertFalse(has_permission("guest", "delete"))

    @patch('your_app_name.permissions.database')  # Mocking database
    def test_mocked_database(self, mock_db):
        mock_db.get_permission.return_value = True
        self.assertTrue(has_permission("user", "read"))


if __name__ == "__main__":
    unittest.main()
=======
import unittest
from your_app_name.permissions import has_permission
from unittest.mock import patch  # Added for mocking


class TestPermissions(unittest.TestCase):
    
    def test_has_permission_admin(self):
        self.assertTrue(has_permission("admin", "read"))
        self.assertTrue(has_permission("admin", "write"))
        self.assertTrue(has_permission("admin", "delete"))
    
    def test_has_permission_user(self):
        self.assertTrue(has_permission("user", "read"))
        self.assertFalse(has_permission("user", "write"))
        self.assertFalse(has_permission("user", "delete"))
    
    def test_has_permission_guest(self):
        self.assertFalse(has_permission("guest", "read"))
        self.assertFalse(has_permission("guest", "write"))
        self.assertFalse(has_permission("guest", "delete"))

    @patch('your_app_name.permissions.database')  # Mocking database
    def test_mocked_database(self, mock_db):
        mock_db.get_permission.return_value = True
        self.assertTrue(has_permission("user", "read"))


if __name__ == "__main__":
    unittest.main()
>>>>>>> b2281d0f31a00b7a805a9cd78fa2455b23fec8b5:testing/test_permissions.py
