import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return str(random.randint(100000,999999))

def send_otp_email(user,otp):
    subject = 'Your Email OTP'
    message = f"Hi  {user.username} ,\n\nYour OTP is: {otp}\n\nThis OTP is valid only for a short time."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject,message,from_email,recipient_list)