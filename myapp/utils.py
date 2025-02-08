from django.core.mail import send_mail
import uuid
from django.conf import settings

def password_reset_email(email,token):
  
   subject='Your forget password link'
   message=f'Hi,click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
   email_from=settings.EMAIL_HOST_USER
   recipient_list=[email]
   send_mail(subject,message,email_from,recipient_list)
   return True
