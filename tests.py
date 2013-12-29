#! py2flask/bin/python
import os
import unittest

from config_test import basedir, TESTING, CSRF_ENABLED, SQLALCHEMY_DATABASE_URI
from application import app, db
from application.models import User


class TesCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = TESTING
        app.config['CSRF_ENABLED'] = CSRF_ENABLED
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        pass

    def test_make_unique_nickname(self):
        pass
    if __name__ == '__main__':
        unittest.main()
