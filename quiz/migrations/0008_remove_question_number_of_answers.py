# Generated by Django 3.1.5 on 2021-02-01 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20210201_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='number_of_answers',
        ),
    ]
