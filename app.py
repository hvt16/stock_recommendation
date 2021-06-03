from flask import Flask,render_template,request,url_for,redirect,session
import pyrebase
import requests
from requests.packages.urllib3.contrib.appengine import is_prod_appengine_mvms
from requests.sessions import requote_uri
import mail
import sys
import hashlib
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "my secret key // will be updated"
oauth = OAuth(app)

# firebase config
firebaseConfig = {
    "apiKey": "AIzaSyACWXK2VmLBotDPD-cnDJ65XDR7WbIhcdk",
    "authDomain": "stock-recommendation-f23ad.firebaseapp.com",
    "projectId": "stock-recommendation-f23ad",
    "storageBucket": "stock-recommendation-f23ad.appspot.com",
    "messagingSenderId": "320005278116",
    "appId": "1:320005278116:web:94219442df5f9bfffd5931",
    "measurementId": "G-R1CY9NBTJY",
    "databaseURL": "https://stock-recommendation-f23ad-default-rtdb.firebaseio.com/",
  }

google = oauth.register(
    name='google',
    client_id='320005278116-rojggp59fdbmnhbl398ctrla2vk2l4og.apps.googleusercontent.com',
    client_secret='lQ_uWxqriiCbm7DzqK_hg190',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

details = {
    'uname': '',
    'name': '',
    'email': '',
    'phone': '',
    'password': '',
    'v_code': '',
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
try:
    db = firebase.database()
except Exception as e:
    sys.stderr.write('db init failed {}'.format(e))

def get_hash(s):
    h = hashlib.new('sha224')
    s = bytes(s,encoding='utf-8')
    h.update(s)
    return h.hexdigest()

def db_details():
    data = {}
    data['name'] = details['name']
    data['phone'] = details['phone']
    data['email'] = details['email']
    data['uname'] = details['uname']
    return data

def isRegistered(email):
    data = db.child("users").get()
    #print(data.key())
    for d in data.each():
        print(d.val())
        if d.val()['email'] == email:
            details['uname'] = d.val()['uname']
            return True
    return False


@app.route('/', methods=['GET','POST'])
def basic():
    if request.method == 'POST':
        uname = request.form['uname']
        password = get_hash(request.form['password'])
        try:
            act_pass = db.child("auth").child(uname).get()
            if act_pass.val() == password:
                data = db.child("users").child(uname).get()
                details['uname'] = data.val()['uname']
                details['name'] = data.val()['name']
                details['phone'] = data.val()['phone']
                details['email'] = data.val()['email']
                
                return render_template('home.html',s="logged in successfully")
            #auth.sign_in_with_email_and_password(email,password)
            return render_template('index.html',us="invalid credentials")
        except:
            return render_template('index.html',us="invalid credentials")
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        details['uname'] = request.form['uname']
        details['name'] = request.form['name']
        details['phone'] = request.form['phone']
        details['email'] = request.form['email']
        details['password'] = get_hash(request.form['password'])
        details['v_code'] = mail.get_verification_code()
        try:
            mail.send_mail(details['email'],details['v_code'])
            #auth.create_user_with_email_and_password(email,password)
            return render_template('verify_email.html')
        except:
            return render_template('register.html',us="Failed to send verification code to email")
    return render_template('register.html')

@app.route('/google_sign_in', methods=['GET','POST'])
def google_sign_in():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    print(user_info)
    session['name'] = user_info['name']
    # do something with the token and profile
    return render_template('home.html',gmail=session['name'])

@app.route('/verify_email', methods=['GET','POST'])
def verify_email():
    if request.method == 'POST':
        entered_code = request.form['code']
        if int(entered_code) == details['v_code']:
            try:
                #auth.create_user_with_email_and_password(details['email'],details['password'])
                data = db_details()
                db.child("users").child(details['uname']).set(data)
                db.child("auth").child(details['uname']).set(details['password'])
                return render_template('home.html',user=details['name'])
            except Exception as e:
                return render_template('register.html',us="{}".format(e))
        else:
            return render_template('verify_email.html',s="code is incorrect")
    return render_template('verify_email.html')

@app.route('/forgot_password', methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['reg_email']
        if isRegistered(email):
            v_code = mail.get_verification_code()
            details['v_code'] = v_code
            mail.send_mail(email,v_code)
            return render_template('verify_email_forgot.html')
    else:
        return render_template('forgot_password.html')

@app.route('/verify_email_forgot', methods=['GET','POST'])
def verify_email_forgot():
    if request.method == 'POST':
        entered_code = request.form['code']
        if int(entered_code) == details['v_code']:
            return render_template('reset_new_password.html')
        else:
            return render_template('verify_email.html',s="code is incorrect")
    return render_template('verify_email.html')

@app.route('/reset_new_password', methods=['GET','POST'])
def reset_new_password():
    if request.method == 'GET':
        return render_template('reset_new_password.html')
    else:
        new_pass = request.form['new_password']
        conf_new_pass = request.form['cnew_password']
        f_pass = db.child('auth').child(details['uname']).get()
        # add validation
        try:
            db.child("auth").child(details['uname']).set(get_hash(new_pass))
            return render_template('reset_new_password.html',s='password updated')
        except:
            return render_template('reset_new_password.html',us='could not reset password')


@app.route('/reset_password', methods=['GET','POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html')
    else:
        old_pass = request.form['curr_password']
        new_pass = request.form['new_password']
        conf_new_pass = request.form['cnew_password']
        f_pass = db.child('auth').child(details['uname']).get()
        # add validation
        print(get_hash(old_pass))
        print(f_pass.val())
        print(details)
        if get_hash(old_pass) != f_pass.val():
            return render_template('reset_password.html',us='old password incorrecct')
        try:
            db.child("auth").child(details['uname']).set(get_hash(new_pass))
            return render_template('reset_password.html',s='password updated')
        except:
            return render_template('reset_password.html',us='could not reset password')

@app.route('/logout', methods=['GET'])
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
