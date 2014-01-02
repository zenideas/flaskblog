import os
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'OijMJmjjkjsdhsdghsdshjdgsgjasadfs'


OPENID_PROVIDERS = [ {'name' : 'Google', 'url' : 'https://www.google.com/accounts/o8/id'}, {'name' : 'Yahoo', 'url' : 'https://me.yahoo.com/'}, {'name' :  'AOL', 'url' : 'http://openid.aol.com/<username>'}, {'name' : 'Flicker', 'url' : 'http://www.flicker.com/<username>' }, {'name' : 'MyOpenID', 'url' : 'http://www.myopenid.com/'} ]
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'application/db/py2blog.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'application/db/db_repository')


MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'nazryul25bd@gmail.com'
MAIL_PASSWORD = ''

ADMINS = ['devs@karitkarma.com']

#Pagination
POSTS_PER_PAGE = 3

WHOOSH_BASE = os.path.join(basedir, 'tmp/search.db')
MAX_SEARCH_RESULTS = 50
