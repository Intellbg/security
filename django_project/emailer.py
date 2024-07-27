# -*- coding: utf-8 -*-
import base64
import qrcode
from io import BytesIO
from django_project import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from datetime import date, timedelta, datetime
import logging

def notify_creation_by_mail(invitation):
    try:
        subject = "Invitación PASSE " + invitation.invite_time.strftime("%Y-%m-%d %H:%M:%S")
        from_email = "Passe <" + settings.EMAIL_HOST_USER + ">"
        receiver_email = invitation.user_invitee.email()
        logging.info(f"Sending mail | {receiver_email}")
        img = qrcode.make(invitation.passe_code + "|$$|" + str(invitation.id) + "#")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        logging.info(f"Sending mail | QR IMG CREATED")
        qr_code_data = buffered.getvalue()
        html_content = render_to_string(
            "email/invitation_send.html",
            {
                "invitee": invitation.name_invitee(),
                "host": invitation.name_host(),
                "place": invitation.site,
                "initiate_timestamp": invitation.invite_time,
                "expiration_timestamp": invitation.max_entry_time,
                "qr": base64.b64encode(qr_code_data).decode("utf-8"),
            },
        )
        logging.info(f"Sending mail | Rendered")
        plain_message = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email,
            [receiver_email],
            headers={
                "X-Priority": "Medium",
                "User-Agent": "Zoho Mail",
                "X-Mailer": "Zoho Mail",
            },
        )
        logging.info(f"Sending mail | email content created")
        email.attach("qrcode.png", qr_code_data, "image/png")
        email.attach_alternative(html_content, "text/html")
        logging.info(f"Sending mail | email image attached")
        email.send()
        logging.info(f"Sending mail | Success")
    except Exception as e:
        logging.error(e)
        return False
    return True


def send_passe_id_by_mail(user):
    subject = f"PASSE ID {date.today()}"
    from_email = "Passe <" + settings.EMAIL_HOST_USER + ">"
    receiver_email = user.user.username
    img = qrcode.make(f"{user.id_hash}|$$|id{user.user_id}#")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_data = buffered.getvalue()
    html_content = render_to_string(
        "email/passe_id.html",
        {
            "host": user.full_name(),
            "initiate_timestamp": datetime.now(),
            "expiration_timestamp": datetime.now()+timedelta(days=1),
            "qr": base64.b64encode(qr_code_data).decode("utf-8"),
        },
    )
    plain_message = strip_tags(html_content)
    try:
        email = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email,
            [receiver_email],
            headers={
                "X-Priority": "Medium",
                "User-Agent": "Zoho Mail",
                "X-Mailer": "Zoho Mail",
            },
        )
        email.attach("qrcode.png", qr_code_data, "image/png")
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(e)
        return False
    return True
