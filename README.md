Flask Blog
======
Installation
------------
- Make Directory 'db' at application and 'tmp' under system root
	`mkdir application/db && mkdir tmp`
- Create VirtualENV name should be 'py2flask'
	`virtualenv py2flask`
- Install Flask `py2flask/bin/pip install flask==0.10.1`
- Install Packages
- $`py2flask/bin/pip install sqlalchemy==0.8.4 sqlalchemy-migrate flask-sqlalchemy flask_whooshalchemy==0.55a`
- $`py2flask/bin/pip install flask-login flask-openid flask-mail flask-wtf pytz flask-babel flup flask-testing`
- Run `db_create.py`
