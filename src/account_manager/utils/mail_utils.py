import logging

from django.core.mail import get_connection, send_mail
from django.utils.html import strip_tags
from core.settings import PASSWORD_RESET_TIMEOUT_DAYS
from multiprocessing import Process
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_USE_SSL, EMAIL_USE_TLS

logger = logging.getLogger(__name__)


def realm_send_mail(realm, to, subject, message):
    logger.info('send mail')
    connection = get_connection(host=EMAIL_HOST,
                                port=EMAIL_PORT,
                                username=realm.email,
                                use_ssl=EMAIL_USE_SSL,
                                use_tls=EMAIL_USE_TLS)
    send_mail(subject=subject,
              message=strip_tags(message),
              html_message=message,
              from_email=realm.email,
              recipient_list=[to, ],
              connection=connection)
    logger.info('mail sent')


def send_welcome_mail(domain, email, protocol, realm, user):
    mail_subject = 'Aktiviere deinen StuVe Account'
    message = render_to_string('registration/welcome_email.jinja2', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': default_token_generator.make_token(user=user),
        'protocol': protocol,
        'email': email,
        'expiration_days': PASSWORD_RESET_TIMEOUT_DAYS
    })
    # TODO failure handling
    p1 = Process(target=realm_send_mail, args=(realm, user.email, mail_subject, message))
    p1.start()
