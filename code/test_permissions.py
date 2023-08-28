import unittest
from your_app_name.permissions import has_permission

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

# Additional tests can be added here

if __name__ == "__main__":
    unittest.main()
