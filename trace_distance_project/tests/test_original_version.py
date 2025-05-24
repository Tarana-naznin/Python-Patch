import unittest
import sys
import os

# Ensure parent directory is in sys.path so "targets" can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from targets.original_version import User, process_users

class TestOriginalVersion(unittest.TestCase):

    def test_user_login(self):
        user = User("Test", 25)
        self.assertFalse(user.logged_in)
        user.login()
        self.assertTrue(user.logged_in)

    def test_is_adult_threshold(self):
        adult = User("Adult", 18)
        teen = User("Teen", 17)
        self.assertTrue(adult.is_adult())
        self.assertFalse(teen.is_adult())

    def test_no_skip_under_16(self):
        data = [
            {"name": "Young", "age": 15},
            {"name": "Mid", "age": 18},
        ]
        summary, total = process_users(data)
        self.assertIn("Young", summary)
        self.assertIn("Mid", summary)
        self.assertEqual(total, 1)

    def test_total_adults(self):
        data = [
            {"name": "One", "age": 18},
            {"name": "Two", "age": 22},
            {"name": "Three", "age": 17},
        ]
        summary, total = process_users(data)
        self.assertEqual(total, 2)
        self.assertIn("One", summary)
        self.assertIn("Two", summary)
        self.assertIn("Three", summary)

if __name__ == "__main__":
    unittest.main()
