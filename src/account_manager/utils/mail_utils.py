import logging

from django.core.mail import get_connection, send_mail
from django.utils.html import strip_tags

from src.core import EMAIL_HOST, EMAIL_PORT, EMAIL_USE_SSL, EMAIL_USE_TLS

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
