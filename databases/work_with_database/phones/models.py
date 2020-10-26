from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    name = models.TextField()
    image = models.URLField()
    price = models.FloatField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField()

    def __str__(self):
        return f'{self.name}'
