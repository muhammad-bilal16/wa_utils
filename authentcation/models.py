from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'email': reset_password_token.user.email,
        'reset_password_url': reset_password_token.key
    }

    # render email text
    email_html_message = render_to_string('user_reset_password.html', context)
    email = EmailMessage(
        "Reset password",
        email_html_message,
        settings.DEFAULT_FROM_EMAIL,
        [reset_password_token.user.email]
    )
    email.content_subtype = "html"
    email.send()
