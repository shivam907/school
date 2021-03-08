import json
import math
import os
import urllib.request
import requests
from flask_mail import Message
from flask import abort, render_template, request, url_for, flash, redirect
from flaskblog import app, mail
from flaskblog.forms import weather, send_otp, verify, email, send

@app.route("/")
@app.route("/about")
def home():
    return render_template('home.html')


@app.route("/weather",  methods=['GET', 'POST'])
def check_weather():
    temp=0
    city=''
    form = weather()
    if form.validate_on_submit():
        city=form.city.data
        
        api="c445762544df62f5dc5ccf510d289aea"
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city, api)).read() 
        temp = round(json.loads(source)['main']['temp']-273.15)
        
    return render_template('weather.html', title='Weather',
                            form=form, legend='Check Temperature', c=temp, city=city.capitalize())

@app.route("/covid", methods=['GET', 'POST'])
def covid():
    url = "https://api.covid19india.org/data.json"   #Using API to Get Data
    r = requests.request('GET', url)
    d = r.json()
    b=d['cases_time_series']
    a=len(b)
    return render_template('covid.html', title='COVID19', Today_New_Cases=b[a-1]['totalconfirmed'])


@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact Us')


def send_code(mobile_no):
  url = "https://d7-verify.p.rapidapi.com/send"

  payload = "{    \"expiry\": 900,    \"message\": \"Enter {code} to Verify Your Mobile Number -CEZ\",    \"mobile\": "+mobile_no+",    \"sender_id\": \"CEZ\"}"
  headers = {
    'content-type': "application/json",
    'authorization': "Token 7404642da966fe2cc0647def4bccab699b19d0c7",
    'x-rapidapi-key': "f61787f699mshf9480a998340f9ep13c50djsndfc6e2954a95",
    'x-rapidapi-host': "d7-verify.p.rapidapi.com"
    }

  response = requests.request("POST", url, data=payload, headers=headers).json()
  otp_id = response["otp_id"]
  return otp_id


def verify_code(otp, otp_id):
  url = "https://d7-verify.p.rapidapi.com/verify"
  payload = "{    \"otp_code\": \""+otp+"\",    \"otp_id\": \""+otp_id+"\"}"
  headers = {
    'content-type': "application/json",
    'authorization': "Token 7404642da966fe2cc0647def4bccab699b19d0c7",
    'x-rapidapi-key': "f61787f699mshf9480a998340f9ep13c50djsndfc6e2954a95",
    'x-rapidapi-host': "d7-verify.p.rapidapi.com"
    }
  response = requests.request("POST", url, data=payload, headers=headers).json()
  if 'status' in response:
    if response['status']=='success':
      return True
    else:
      return False
  else:
    return False


@app.route("/verify", methods=['GET', 'POST'])
def verify_mob():
    form1 = send_otp()    
    if form1.validate_on_submit():
        mob = form1.mob.data
        print("OTP SENT Successfully")
        otp_id = send_code("91"+str(mob))
        flash("OTP Sent", 'success')
        return redirect('/verify/Code/'+otp_id)
    return render_template('mob.html', title='Verify Mobile Number', form1=form1)


@app.route("/verify/Code/<string:otp_id>", methods=['GET', 'POST'])
def verify_otp(otp_id):
    form2 = verify()
    if form2.validate_on_submit():
        code = form2.code.data
        if verify_code(code, otp_id):
            flash("Your Code is Verified", 'success')
            
        else:
            flash("Invalid Code", 'danger')
    
    return render_template('verify.html', title='Verify Code', form2=form2)

def verify_email_for_valid(email):
    url = "https://api.zerobounce.net/v2/validate"
    api_key = "ee3824f3492549a4bfaa9133987ac28c"
    ip_address = "99.123.12.122" #ip_address can be blank

    params = {"email": email, "api_key": api_key, "ip_address":ip_address}

    response = requests.get(url, params=params)
    return json.loads(response.content)['status']


@app.route("/Send_Email", methods=['GET', 'POST'])
def semail():
  form = email()
  if form.validate_on_submit():
    email_id = form.email.data
    if verify_email_for_valid(email_id)=='valid':
      return redirect("/Send_Email/{}".format(email_id))
    else:
      flash("Email Entered is Not Valid", 'danger')

  return render_template('email.html', title='Enter Email', form=form)

def send_mail(to, subject, content):
  msg = Message(subject, sender='CEZ', recipients=[to])
  msg.body = content
  mail.send(msg)


@app.route("/Send_Email/<string:email_id>", methods=['GET', 'POST'])
def send_emailto(email_id):
  form = send()
  if form.validate_on_submit():
    subject = form.subject.data
    content = form.content.data
    send_mail(email_id, subject, content)
    flash("Email Sent", 'success')
    return redirect('home')

  return render_template('send.html', title="Send Email", form=form)

