# Generated by Django 3.1.5 on 2021-02-03 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_question_slug'),
        ('users', '0007_userregisteredquizzes_current_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.answer')),
            ],
        ),
    ]