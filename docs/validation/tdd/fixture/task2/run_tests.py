"""Run the whole suite, or the test modules/cases named on the command line."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

loader = unittest.TestLoader()
suite = (loader.loadTestsFromNames(sys.argv[1:]) if len(sys.argv) > 1
         else loader.discover("tests", top_level_dir=ROOT))
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
