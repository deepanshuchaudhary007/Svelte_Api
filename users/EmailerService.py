from django.core.mail import EmailMessage
import os

class EmailerService:
    @staticmethod
    def email_sender(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('FROM_EMAIL'),
            to=[data['to_email']]
        )
        email.send()