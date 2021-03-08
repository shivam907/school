import os
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CEZ'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cezlogin@gmail.com'  #Email ID
app.config['MAIL_PASSWORD'] = 'creativeexpertz'  #Email Account Password
mail = Mail(app)
from flaskblog import routes