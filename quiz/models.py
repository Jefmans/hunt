from django.db import models
from django.db.models.signals import pre_save
from quiz.utils import pre_save_receiver_slugify


# Create your models here.

class IsActiveManager(models.Manager):
	def is_active(self):
		return self.filter(is_active=True)
	def is_published(self):
		return self.filter(is_published=True)
	def is_active_and_published(self):
		return self.filter(is_active=True).filter(is_published=True)



class Quiz(models.Model):
	title = models.CharField(max_length=64)
	description = models.TextField(blank=True)

	is_active = models.BooleanField('Quiz is Active', default=True)
	is_published = models.BooleanField('Quiz is Published', default=False)

	date_created = models.DateTimeField(auto_now_add=True)

	start_date = models.DateTimeField(null=True, default=None) 	

	slug = models.SlugField()

	objects = IsActiveManager()

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = "Quizzes"

	def question_count(self, ):
		return self.question_set.count()

pre_save.connect(pre_save_receiver_slugify, sender=Quiz)


class Question(models.Model):
	MULTIPLE_CHOICE = 0
	SINGLE_ANSWER = 1
	IMAGE = 2

	QUESTION_TYPE_CHOICES = (
		(MULTIPLE_CHOICE, "Multiple Choice"),
		(SINGLE_ANSWER, "Open Vraag"),
		(IMAGE, "Foto"),)

	title = models.CharField(max_length=64)
	description = models.TextField(blank=True)

	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, verbose_name='Quiz Name')

	question_type = models.IntegerField(choices=QUESTION_TYPE_CHOICES, default=MULTIPLE_CHOICE)

	sequence_number = models.IntegerField('seq #', null=True)

	slug = models.SlugField()

	def __str__(self):
		return self.title

	def answer_count(self, ):									# you can also add this in ModelAdmin class --> (self, obj)
		return self.answer_set.count()							# --> obj.answer_set.count()

pre_save.connect(pre_save_receiver_slugify, sender=Question)


class Answer(models.Model):
	INTEGER = 0
	TEXT = 1
	DATE = 2
	TYPE_CHOICES = (
		(INTEGER, "Getal"),
		(TEXT, "Tekst"),
		(DATE, "Datum"),)

	answer_title = models.CharField(max_length=128)

	answer_type = models.IntegerField(choices=TYPE_CHOICES, default=TEXT)
	
	question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.answer_title