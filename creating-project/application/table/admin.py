from django.contrib import admin

from table.models import Columns, CsvFile


@admin.register(Columns)
class AdminColumns(admin.ModelAdmin):
    pass


@admin.register(CsvFile)
class AdminCsvFile(admin.ModelAdmin):
    pass
