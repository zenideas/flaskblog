#! py2flask/bin/python
import os
import unittest
from flask.ext.testing import TestCase

from config_test import basedir, TESTING, CSRF_ENABLED, SQLALCHEMY_DATABASE_URI
from application import app, db
from application.models import User


class TesCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = TESTING
        app.config['CSRF_ENABLED'] = CSRF_ENABLED
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname='john', email='john@example.com')
        avatar = u.avatar(120)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'

        u = User(nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname

    def test_follow(self):
        u1 = User(nickname='john', email='john@mayait.org')
        u2 = User(nickname='susan', email='susan@mayait.org')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None

        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()

        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'susan'

        assert u2.followers.count == 1
        assert u2.followers.first().nickname == 'john'

        u = u1.unfollow(u2)
        assert u != None
        db.session.add(u)
        db.session.commit()

        assert u1.is_following(u2) is False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

if __name__ == '__main__':
    unittest.main()
