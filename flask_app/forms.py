from flask_wtf import Form
#from flask import session, g
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, HiddenField, validators
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import EmailField


class ContactForm(Form):
    id = HiddenField()
    email = EmailField('email', validators=[DataRequired(), validators.Email()])
    message = TextAreaField('message')
    get_newsletter = BooleanField('newsletter', default=False)
    contact_reason = StringField('contact_reason', validators=[DataRequired()])    
