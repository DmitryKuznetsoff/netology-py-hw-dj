import csv

from django.shortcuts import render

from table.models import Columns, CsvFile


# CSV_FILENAME = 'phones.csv'
# COLUMNS = [
#     {'name': 'id', 'width': 1},
#     {'name': 'name', 'width': 3},
#     {'name': 'price', 'width': 2},
#     {'name': 'release_date', 'width': 2},
#     {'name': 'lte_exists', 'width': 1},
# ]


def table_view(request):
    csv_filename = CsvFile().get_filename()
    columns = Columns.objects.values('name', 'width').order_by('index')

    template = 'table/table.html'
    with open(csv_filename, 'rt') as csv_file:
        header = []
        table = []
        table_reader = csv.reader(csv_file, delimiter=';')
        for table_row in table_reader:
            if not header:
                header = {idx: value for idx, value in enumerate(table_row)}
            else:
                row = {header.get(idx) or 'col{:03d}'.format(idx): value
                       for idx, value in enumerate(table_row)}
                table.append(row)

        context = {
            'columns': columns,
            'table': table,
            'csv_file': csv_filename
        }
        result = render(request, template, context)
    return result
