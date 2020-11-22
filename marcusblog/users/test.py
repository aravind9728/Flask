from flask import render_template, url_for,flash,redirect,request
from twilio.rest import Client
import random 
from flask import Flask

app = Flask(__name__)
app.secret_key = 'otp'
if __name__ == '__main__':
   app.run(debug=True)

@app.route('/')
def home():
    return render_template('login.html')


@app.route("/getotp", methods =['POST'])
def getotp():
    number = request.form['number']
    val = getotpAPI(number)
    if val:
        return render_template("otp.html")

@app.route ("/validateotp", methods = ['POST'])
def validateotp():
    otp = request.form['otp']
    if 'response' in session:
        s = session['response']
        session.pop('response',None)
        if s == otp:
            return 'Your are Authorized for the session! thank you' 
        else:
            return 'Your not AUthorized'    

def generateOTP():
    return random.randrange(100000,999999)  

def getotpAPI(number):
    account_sid='ACdcf496da61c4c4a0502ff4ccd32b8762'
    auth_token ='9f9ca481ab1ef79a9235fcb9ff866c97'
    client = Client(account_sid,auth_token)
    otp = generateOTP()
    session['response'] = str(otp)
    body = 'Your OTP is' + str(otp)
    message = client.messages.create(from_='+13513336544',body=body,to=number)

    if message.sid:
        return True
    else:
        False

