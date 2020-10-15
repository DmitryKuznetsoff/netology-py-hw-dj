import re

from datetime import datetime
from django import template

register = template.Library()


@register.filter
def format_date(value: int):
    # Ваш код
    dt = datetime.fromtimestamp(value)
    now = datetime.now()
    # Разница во времени в минутах:
    time_diff = (now - dt).total_seconds() / 60
    if time_diff < 10:
        result = 'только что'
    elif 10 <= time_diff <= 1440:
        result = f'{int(time_diff / 60)} часов назад'
    else:
        result = dt.strftime('%Y %m %d')
    return result


@register.filter
def show_rating(value: int):
    if value < -5:
        result = 'всё плохо'
    elif -5 <= value <= 5:
        result = 'нейтрально'
    else:
        result = 'хорошо'
    return result


@register.filter
def format_num_comments(value=None):
    # Ваш код
    if not value:
        return 'Some default value'
    else:
        if value == 0:
            result = 'Оставьте комментарий'
        elif 0 < value <= 50:
            result = value
        else:
            result = '50+'
        return result


@register.filter
def format_text(value: str, count: int):
    words = re.findall(r'\S+', value)
    if not words:
        return ''
    elif len(words) < count:
        return value
    else:
        first = ' '.join(words[:count])
        last = ' '.join(words[-count:])
        return f'{first} ... {last}'
