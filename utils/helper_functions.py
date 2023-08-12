from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings


def send_email_with_template(username, email):
    """Sends an email to the specified user with an HTML template.

    Args:
    username: The username of the user to send the email to.
    email: The email address of the user to send the email to.
    """

    template = get_template('emails/email_template.html')
    context = {
    'username': username,
    'CUSTOMER_SUPPORT_EMAIL':settings.CUSTOMER_SUPPORT_EMAIL
    }
    message = template.render(context)

    email_message = EmailMessage(
    subject='Welcome to Django!',
    body=message,
    from_email=settings.EMAIL_HOST_USER,
    to=[email],
    )
    email_message.content_subtype = 'html'
    email_message.send()
