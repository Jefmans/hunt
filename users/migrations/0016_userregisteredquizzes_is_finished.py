# Generated by Django 3.1.5 on 2021-02-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_useranswers_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregisteredquizzes',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]
