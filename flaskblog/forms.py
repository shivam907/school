from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class weather(FlaskForm):
    city = StringField('Enter City', validators=[DataRequired()])
    submit = SubmitField(' Check ')

class send_otp(FlaskForm):
    mob = StringField('Mobile Number', validators=[DataRequired()])
    send = SubmitField('Send Code')

class verify(FlaskForm):
    code = StringField('Enter 6 Digit Code', validators=[DataRequired()])
    submit = SubmitField('Verify')

class email(FlaskForm):
    email = StringField("Enter Recipient", validators=[DataRequired()])
    Next = SubmitField('Next')

class send(FlaskForm):
    subject = StringField("Enter Subject", validators=[DataRequired()])
    content = StringField("Enter Content", validators=[DataRequired()])
    send = SubmitField("Send")