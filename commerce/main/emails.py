
from django.core.mail import EmailMultiAlternatives


def sending_html_mail(subject, text_content, html_content,
                      from_email, to_list):
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
