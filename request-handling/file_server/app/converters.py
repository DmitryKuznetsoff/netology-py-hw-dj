import datetime


class DateConverter:
    regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, date: str) -> datetime:
        year, month, day = map(int, date.split('-'))
        return datetime.date(year, month, day)

    def to_url(self, date: datetime):
        return date.strftime('%Y-%m-%d')
