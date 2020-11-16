from django.core.validators import MaxValueValidator
from django.db import models
from django.conf import settings


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
        validators=[MaxValueValidator(settings.MAX_STUDENTS_PER_COURSE)]
    )
