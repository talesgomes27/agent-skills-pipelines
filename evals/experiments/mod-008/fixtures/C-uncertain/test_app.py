import unittest
from app import normalize_age
class Contract(unittest.TestCase):
 def test_known(self):
  self.assertEqual(normalize_age('42'),42)
  self.assertEqual(normalize_age(0),0)
