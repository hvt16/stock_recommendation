import smtplib
import random

def get_verification_code():
    verification_code = random.randint(111111,999999)
    return verification_code

def send_mail(receiver,verification_code):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    login = 0
    try:
        s.login("stock.recommendation.sp@gmail.com", "Spro@2021")
        login = 1
    except:
        print("login failed")

    if login:
        subject = "Verify Your Email !!"
        text = "Your verification code is : {}".format(verification_code)
        message = "Subject: {}\n\n{}".format(subject,text)
        s.sendmail("stock.recommendation.sp@gmail.com", receiver, message)

    s.quit()
