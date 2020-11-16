import os

from django.db import models


class Columns(models.Model):
    class Meta:
        verbose_name = 'Колонки'
        verbose_name_plural = 'Колонки'

    name = models.TextField(max_length=100)
    width = models.IntegerField()
    index = models.IntegerField()


class CsvFile(models.Model):
    class Meta:
        verbose_name = 'Путь к .csv'
        verbose_name_plural = 'Путь к .csv'

    path = models.TextField()

    def set_path(self, path):
        current_path = self.get_path()
        if not current_path:
            CsvFile.objects.create(path=path)
        else:
            current_path.path = path
        return current_path

    def get_path(self):
        return CsvFile.objects.first()

    def get_filename(self):
        current_path = self.get_path()
        return os.path.basename(current_path.path)

    def __str__(self):
        return os.path.abspath(self.path)
