import datetime


class PubDateConverter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value):
        year, month, day = map(int, value.split('-'))
        return datetime.date(year, month, day)

    def to_url(self, value):
        return value.strptime('%Y-%m-%d')
