from __future__ import absolute_import, unicode_literals

from django.conf import settings

from commerce.celery import app
from main.emails import sending_html_mail

from main.models import Subsciber, Product, SMSLog
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

import os, json
from twilio.rest import Client
from random import choice
from string import digits


def generic_code_sms():
    code = list()
    for i in range(4):
        code.append(choice(digits))

    return ''.join(code)


@app.task(name="send_email_user_task")
def sending_html_mail_task(subject, text_content, html_content, from_email, to_list):
    return sending_html_mail(subject, text_content, html_content, from_email, to_list)


@app.task
def sending_new_products():
    emails = [e.user.email for e in Subsciber.objects.all()]
    products = Product.objects.order_by('-id')[:5]
    subject = f"Новый товары за неделю!"
    text_content = ""
    html_content = ""
    for product in products:
        text_content += f"{product.title}, "
        html_content += f"""<p>{product.title}</p><br>"""
    from_email = settings.EMAIL_HOST_USER
    sending_html_mail(subject, text_content, html_content, from_email, emails)


@receiver(user_signed_up)
def user_signed_up_(sender, request, user, **kwargs):
    subject, from_email, to_list = f"Пользователь {user}", 'paveldudkov003@gmail.com', [user.email]
    text_content = 'Благодарим Вас за интерес к нашему сайту!'
    html_content = '<p>Благодарим Вас за интерес к нашему сайту!</p>'
    sending_html_mail_task.delay(subject, text_content, html_content, from_email, to_list)


@receiver(post_save, sender=Product)
def send_new_product(sender, instance, created, **kwargs):
    if created:
        emails = [e.user.email for e in Subsciber.objects.all()]
        subject = f"Новый товар: {instance.title}"
        text_content = f"Появился новый товар {instance.title}. Все подробности по ссылке {instance.get_absolute_url()}"
        html_content = f'''
            <h1>Появился новый товар {instance.title}</h1>
            <ul>
                <li>Описание: {instance.description}</li>
                <li>Цена: {instance.price}</li>
            </ul>
            Все подробности <a href="{instance.get_absolute_url()}">по ссылке</a>.
        '''
        from_email = settings.EMAIL_HOST_USER
        sending_html_mail_task.delay(subject, text_content, html_content, from_email, emails)


@app.task
def send_sms_code_twilio():
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    user_code = generic_code_sms()

    message = client.messages.create(
        body=user_code,
        from_='+14152344670',
        to='+79370230700'
    )

    SMSLog.objects.create(
        code=int(user_code),
        response_server=message.uri
    )

    print('Complied')



