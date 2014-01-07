#! py2flask/bin/python
import os
import sys

if sys.platform == 'win32':
    pybabel = 'py2flask\\Script\\pybabel'
else:
    pybabel = 'py2flask/bin/pybabel'

os.system(pybabel + ' compile -d application/translations')
