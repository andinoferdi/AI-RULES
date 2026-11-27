"""Run the test suite, or the tests named on the command line, with src/ importable."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "src"), ROOT]
os.chdir(ROOT)

loader = unittest.TestLoader()
suite = (loader.loadTestsFromNames(sys.argv[1:]) if len(sys.argv) > 1
         else loader.discover("tests", top_level_dir=ROOT))
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
