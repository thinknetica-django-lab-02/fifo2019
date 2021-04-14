
from commerce.celery import app
from celery.utils.log import get_task_logger

from main.emails import sending_html_mail

logger = get_task_logger(__name__)


@app.task(name="send_email_user_task")
def sending_html_mail_task(subject, text_content, html_content, from_email, to_list):
    logger.info("Sent feedback email")
    return sending_html_mail(subject, text_content, html_content, from_email, to_list)
