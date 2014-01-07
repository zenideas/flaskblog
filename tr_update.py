#! py2flask/bin/python
import os
import sys

if sys.platform == 'win32':
    pybabel = 'py2flask\\Script\pybabel'
else:
    pybabel = 'py2flask/bin/pybabel'

if len(sys.argv) != 2:
    print('usages: tr_init <language-code>')
    exit(1)
os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot application')
os.system(pybabel + ' update -i messages.pot -d application/translations -l ' + sys.argv[1])
os.unlink('messages.pot')
