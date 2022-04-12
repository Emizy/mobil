import json

from celery import shared_task

from utils.mail_handler import EmailHandler
from utils.logger import logger


@shared_task
def email_notification(to, subject, template, context, reply_to=None, files=None, logo=None):
    """
    Email notification function: This function handles sending of emails.
    The following parameters are required: to, subject, template, context.
    """
    msg = {'code': 400, 'message': 'Error'}
    try:
        EmailHandler(to=to, subject=subject, reply_to=reply_to, files=files).html(template, context, logo).send()
        msg = {'code': 200, 'message': 'Ok'}
    except Exception as ex:
        msg = {'code': 400, 'message': str(ex)}
    logger.info(msg)
    return msg
