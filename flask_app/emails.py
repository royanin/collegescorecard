from flask import render_template
from flask_mail import Message
from flask_app import mail
from .decorators import async
from config import ADMINS,URGENT_EMAIL
from flask_app import flask_app
from smtplib import SMTPException


@async
def send_async_email(flask_app, msg):
    with flask_app.app_context():
        try:
            mail.send(msg)    
        except SMTPException,e:
            #return str("Please enter a valid email id")
            return str(e)


def send_email(subject, sender, recipients, text_body, html_body):
    print 'sender', sender
    print 'recipients', recipients    
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(flask_app, msg)

def notify_server_error():
    print URGENT_EMAIL
    send_email(#"Hi %s!" % email,
               "collegescorecard.io failed",
               ADMINS[0],
               ['royanin@gmail.com'],
               render_template("email_server_fail.txt",
                               email=URGENT_EMAIL),
               render_template("email_server_fail.html",
                               email=URGENT_EMAIL))
    
    
def new_message(sender_email,sender_msg, sender_type, get_newsletter):
    print 'in emails.py:\n'
    print sender_email,sender_msg
    send_email(#"Hi %s!" % email,
               "New message from csc",
               ADMINS[0],
               ['royanin@gmail.com'],
               render_template("email_new_message.txt",
                                sender_email=sender_email,
                                sender_msg = sender_msg,
                                sender_type = sender_type, 
                                get_newsletter = get_newsletter),
               render_template("email_new_message.html",
                                sender_email=sender_email,
                                sender_msg = sender_msg,
                                sender_type = sender_type, 
                                get_newsletter = get_newsletter))
