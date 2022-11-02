from django.conf import settings
from django.core.mail import send_mail
from random import randint, randrange

def mail_send(subject, message, email_from, recipient_list):
    try:
        send_mail(subject, message, email_from, recipient_list )
        return True
    except Exception as e:
        print(e,'======================')
        return False
    

def generate_otp():
    return randint(100000, 999999)
