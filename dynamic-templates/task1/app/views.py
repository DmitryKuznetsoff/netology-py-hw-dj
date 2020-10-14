import csv
import os
from django.shortcuts import render
from dataclasses import dataclass


class TableData:
    def __init__(self, data):
        # Выделяем заголовки таблицы в отдеельный атрибут:
        self.headers = data[0]

        # Выделяем данные таблицы в отдельный атрибут:
        self.data = []
        for year, *inflation, total in data[1:]:
            # Создаём список объектов класса InflationValue из данных с процентами инфляции:
            inflation_obj = [InflationValue(i) for i in inflation]
            self.data.append([year, *inflation_obj, total])


@dataclass
class InflationValue:
    value: float

    def __repr__(self):
        return '-' if not self.value else self.value

    @property
    def get_value(self):
        if self.value:
            return float(self.value)

    @property
    def is_inflation_value(self):
        if isinstance(self, InflationValue):
            return self


def inflation_view(request):
    template_name = 'inflation.html'

    csv_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'inflation_russia.csv')
    with open(csv_file, 'r', encoding='utf-8') as f:
        content = [row[0].split(';') for row in csv.reader(f)]
    # чтение csv-файла и заполнение контекста
    context = {'csv_content': TableData(content)}
    print(content)
    return render(request, template_name,
                  context)
