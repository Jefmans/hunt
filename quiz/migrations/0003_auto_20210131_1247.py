# Generated by Django 3.1.5 on 2021-01-31 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20210130_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='sequence_number',
            field=models.IntegerField(null=True, verbose_name='seq #'),
        ),
        migrations.AlterField(
            model_name='question',
            name='number_of_answers',
            field=models.IntegerField(default=1, verbose_name='# answ'),
        ),
    ]
