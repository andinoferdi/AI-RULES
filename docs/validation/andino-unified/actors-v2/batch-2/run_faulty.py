import os
import runpy

os.environ['PAGE_SUBJECT'] = 'before.py'
runpy.run_path('test_page.py', run_name='__main__')
