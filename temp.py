from base64 import encode
import sys
import pyrebase
import hashlib


# firebaseConfig = {
#     "apiKey": "AIzaSyACWXK2VmLBotDPD-cnDJ65XDR7WbIhcdk",
#     "authDomain": "stock-recommendation-f23ad.firebaseapp.com",
#     "projectId": "stock-recommendation-f23ad",
#     "storageBucket": "stock-recommendation-f23ad.appspot.com",
#     "messagingSenderId": "320005278116",
#     "appId": "1:320005278116:web:94219442df5f9bfffd5931",
#     "measurementId": "G-R1CY9NBTJY",
#     "databaseURL": "https://stock-recommendation-f23ad-default-rtdb.firebaseio.com/",
#   }

# details = {
#     'name': '',
#     'email': '',
#     'phone': '',
#     'password': '',
#     'v_code': '',
# }

# firebase = pyrebase.initialize_app(firebaseConfig)

# auth = firebase.auth()
# try:
#     db = firebase.database()
# except Exception as e:
#     sys.stderr.write('db init failed {}'.format(e))

# data = {
#     'name': 'hvt',
#     'number': '7891009270',
# }

# email = 'hvtailor16@gmail.com'
# password = '12345678'

# user = auth.sign_in_with_email_and_password(email,password)
# auth.send_password_reset_email(email)


h = hashlib.new('sha224')
s = bytes("12345678",encoding='utf-8')
h.update(s)
print(h.hexdigest())