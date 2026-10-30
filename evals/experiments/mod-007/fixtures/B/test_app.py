import unittest
from app import total
class Contract(unittest.TestCase):
 def test_integers(self):
  for values in ([],[0],[1,2,3],[-3,1,0],list(range(100))):
   self.assertEqual(total(values),sum(values))
