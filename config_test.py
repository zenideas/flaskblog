import os
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
TESTING = True
CSRF_ENABLED = False
SECRET_KEY = 'OijMJmjjkjsdhsdghsdshjdgsgjasadfs'


OPENID_PROVIDERS = [ {'name' : 'Google', 'url' : 'https://www.google.com/accounts/o8/id'}, {'name' : 'Yahoo', 'url' : 'https://me.yahoo.com/'}, {'name' :  'AOL', 'url' : 'http://openid.aol.com/<username>'}, {'name' : 'Flicker', 'url' : 'http://www.flicker.com/<username>' }, {'name' : 'MyOpenID', 'url' : 'http://www.myopenid.com/'} ]
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'application/db/py2blog-test.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'application/db/db_repository')


MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

ADMINS = ['nislam@localhost']
