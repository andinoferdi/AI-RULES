import os
import runpy
os.environ['PAGE_SUBJECT'] = 'subject.before.py'
runpy.run_path('test_page.py', run_name='__main__')
