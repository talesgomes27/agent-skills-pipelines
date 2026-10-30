import contextlib, io, tempfile, unittest
from pathlib import Path
import app
class Contract(unittest.TestCase):
 def test_lines_and_cli(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'input.txt'
   for text,n in [('',0),('a\nb\n',2),('a\nb',2)]:
    p.write_text(text)
    self.assertEqual(app.count_lines(p),n)
   with contextlib.redirect_stdout(io.StringIO()) as out:
    self.assertEqual(app.main([str(p)]),0)
   self.assertEqual(out.getvalue().strip(),'2')
   with contextlib.redirect_stderr(io.StringIO()) as err:
    self.assertEqual(app.main([str(p)+'-missing']),1)
   self.assertTrue(err.getvalue().strip())
