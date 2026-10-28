import unittest
from app import take
class Contract(unittest.TestCase):
 def test_take(self):
  self.assertEqual(take([1,2,3],2),[1,2])
  self.assertEqual(take([1,2,3],0),[])
  self.assertEqual(take([],3),[])
