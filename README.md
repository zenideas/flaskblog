# Flask Blog

## Installation

- Make Directory 'db' at application and 'tmp' under system root:

```bash
mkdir application/db && mkdir tmp
```

- Create the VirtualENV, name should be 'py2flask':

```bash
$ virtualenv py2flask
```
- Install Flask:

```bash
$ py2flask/bin/pip install flask==0.10.1
```
- Install SQLAlchemy Packages:

```bash
py2flask/bin/pip install sqlalchemy==0.8.4 sqlalchemy-migrate flask-sqlalchemy flask_whooshalchemy==0.55a
```

- Install other dependencies:

```bash
py2flask/bin/pip install flask-login flask-openid flask-mail flask-wtf pytz flask-babel flup flask-testing
```
- Now to create the Database for the app Run:

```bash
./db_create.py
```
- For Chapter 15|Ajax
``` py2flask/bin/pip install guess-language
