import unittest
from consumer import preview
class Contract(unittest.TestCase):
 def test_preview(self):
  self.assertEqual(preview([1,2,1],2),([1,2],2))
  self.assertEqual(preview([1,2],0),([],2))
