from flask.ext.mail import Message
from application import mail
from config import ADMINS
from decorators import async

@async
def send_async_mail(msg):
    mail.send(msg)


def send_mail(subject, sender, recipents, text_body, html_body):
    msg = Message(subject, sender=sender, recipents=recipents)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_mail, arg=[msg])
    thr.start()

def follower_notification(followed, follower):
    send_mail("[flaskblog] %s is now following you!" % follower.nickname,
              ADMINS[0], [followed.email],
              render_template('follower_email.txt', user=followed, follower=follower),
              render_template('follower_email.html', user=followed, follower=follower))
