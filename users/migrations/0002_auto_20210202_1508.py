# Generated by Django 3.1.5 on 2021-02-02 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_question_slug'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregisteredquizzes',
            name='registered_quizzes',
        ),
        migrations.AddField(
            model_name='userregisteredquizzes',
            name='registered_quizzes',
            field=models.ManyToManyField(null=True, to='quiz.Quiz'),
        ),
    ]