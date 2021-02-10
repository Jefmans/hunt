from django.db import models
from django.contrib.auth.models import User
from quiz.models import Quiz, Question, Answer
from django.db.models import Min
from datetime import datetime, timezone, time, timedelta
from django.shortcuts import get_object_or_404

# Create your models here.



class UserRegisteredQuizzes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	registered_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

	current_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

	is_finished = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user)

	def get_user_email(self):
		return self.user.email
	get_user_email.short_description = 'Email'

	def save(self):
		if Question.objects.filter(quiz__title=self.registered_quiz.title).exists():
			if self.current_question is None:
				get_seq_num = Question.objects.filter(quiz__title=self.registered_quiz.title).aggregate(Min('sequence_number'))
				get_question = Question.objects.filter(quiz__title=self.registered_quiz.title).get(sequence_number=get_seq_num['sequence_number__min'])
				self.current_question = get_question
			else:
				check_sequence = self.current_question.sequence_number
				print(check_sequence)
				check_sequence += 1
				print(check_sequence)
				# if Question.objects.filter(quiz__title=self.registered_quiz.title).filter(sequence_number=check_sequence).exists():
				# 	self.current_question = get_object_or_404(Question, quiz__title=self.registered_quiz, sequence_number=check_sequence)
				# else:
				# 	print("/-/-/-/-/-/-+/+/++/+")


		else:
			self.current_question = None

		super(UserRegisteredQuizzes, self).save()


class UserAnswers(models.Model):
	# correct_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answered = models.CharField(max_length=128)

	working_time = models.DateTimeField()
	last_updated = models.DateTimeField(auto_now=True)


	def get_correct_answer(self):
		return Answer.objects.filter(question=self.question).get(is_correct=True)

	def __str__(self):
		return f'{self.user} - {self.quiz} - {self.question} - {self.answered} - {self.working_time} - {self.reopen_date} - {self.is_still_closed} '

	def _get_reopen_date(self):
		reopen_date = (self.working_time + timedelta(hours=0, minutes=0, seconds=1))
		print(reopen_date)
		return reopen_date
	reopen_date = property(_get_reopen_date)

	def _is_still_closed(self):
		current_time = datetime.utcnow()
		reopen_date = self.reopen_date.replace(tzinfo=None)
		remaining_time = reopen_date - current_time

		if remaining_time > timedelta(hours=0) :
			return True
		else:
			return False
	is_still_closed = property(_is_still_closed)


