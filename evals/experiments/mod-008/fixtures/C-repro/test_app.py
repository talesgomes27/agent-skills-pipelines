import unittest
from app import ratio
class Contract(unittest.TestCase):
 def test_ratio(self):
  self.assertEqual(ratio(6,2),3)
  self.assertIsNone(ratio(1,0))
