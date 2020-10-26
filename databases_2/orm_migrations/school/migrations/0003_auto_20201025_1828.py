# Generated by Django 3.1.2 on 2020-10-25 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20201025_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='teacher',
        ),
        migrations.AddField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='school.teacher'),
            preserve_default=False,
        ),
    ]
