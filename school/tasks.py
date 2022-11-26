from config.celery import  app
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@app.task
def send_confirmation_email(email, activation_code):
    context = {
        "small_text": f"""
        Thank you for creating an account.
        You must follow this link to activate your account:
        """,
        "email": email,
        "activation_code": activation_code,
    }
    msg_html = render_to_string("email.html", context)
    plain_message = strip_tags(msg_html)
    subject = "Account activation"
    to_emails = email
    mail.send_mail(
        subject,
        plain_message,
        "nurkamilaturathankyzy@gmail.com",
        [to_emails],
        html_message=msg_html
    )


@app.task
def send_pass_res(email, new_password):
    context = {
        "email_text_detail": "That's your new password. Please save it)",
        "new_password": new_password,
        "email": f"Your email: {email}"
    }

    msg_html = render_to_string("password_reset.html", context)
    subject = "Password reset"
    plain_message = strip_tags(msg_html)
    to_emails = email
    mail.send_mail(
        subject,
        plain_message,
        "maviboncuaika@gmail.com",
        [to_emails],
        html_message= msg_html
    )