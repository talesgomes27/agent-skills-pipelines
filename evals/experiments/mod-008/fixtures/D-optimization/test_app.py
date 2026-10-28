import unittest
from consumer import priority_order
class Contract(unittest.TestCase):
 def test_order(self): self.assertEqual(priority_order([3,1,3,2]),[3,1,2])
