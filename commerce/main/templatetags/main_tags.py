from django import template
from datetime import datetime


register = template.Library()


@register.simple_tag()
def get_date_server():
    date = datetime.now()
    return f"{date.hour}:{date.minute}:{date.second}"


