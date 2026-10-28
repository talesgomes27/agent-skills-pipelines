import unittest
from app import MESSAGE
class Contract(unittest.TestCase):
 def test_label(self): self.assertEqual(MESSAGE,'Olá')
