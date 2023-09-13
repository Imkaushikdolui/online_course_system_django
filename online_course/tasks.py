from celery import shared_task
from django.core.mail import send_mail

@shared_task(bind=True)
def send_mail_celery(self, subject, message, sender_email, recipient_list):
    try:
        send_mail(subject, message, sender_email, recipient_list, fail_silently=True)
        print("Email sent successfully")
    except Exception as e:
        print(f"Email sending failed: {e}")

    return "Email sent successfully"