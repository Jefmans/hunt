# Generated by Django 3.1.5 on 2021-02-01 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_quiz_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
