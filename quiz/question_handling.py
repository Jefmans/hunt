from django.shortcuts import get_object_or_404, get_list_or_404
from quiz.models import Quiz, Question, Answer
from  users.models import UserAnswers, UserRegisteredQuizzes
from datetime import datetime

REAL_BIG_NUMBER = 999999999999999

class AnsweredQuestionHandling():
	def __init__(self, instance):
		self.current_question = get_object_or_404(Question, slug= instance.kwargs['slug'])
		self.correct_answer = get_object_or_404(Answer, question=self.current_question, is_correct=True)
		self.quiz = get_object_or_404(Quiz, slug = instance.kwargs['quiz_slug'])
		self.user_quiz = get_object_or_404(UserRegisteredQuizzes, user=instance.request.user, registered_quiz=self.quiz)
		
		self.user = instance.request.user
		self.saved_answer = None
		self.next_question = None

		if 'possible_answers' in instance.request.POST:
			self.answered = instance.request.POST['possible_answers']
		elif 'answer' in instance.request.POST:
			self.answered = instance.request.POST['answer']

	# def print_all(self):
	# 	print(self.current_question, self.correct_answer, self.quiz, self.user_quiz, self.answered, self.user)
	
	def _question_exists(self):
		try:
			print('-----------3--------------')
			saved_answer = get_object_or_404(UserAnswers, user=self.user, question=self.current_question)
			self.saved_answer = saved_answer
			print('-----------3--------------')
			return True
		except:
			print('-----------4--------------')
			return False

	def open_or_create_answer(self):
		if self._question_exists():
			print('-----------1--------------')
			# saved_answer = get_object_or_404(UserAnswers, user=self.user, question=self.current_question)
			self.saved_answer.answered = self.answered
			self.saved_answer.working_time = datetime.utcnow()
			self.saved_answer.save()
			return self.saved_answer
		else:
			print('-----------2--------------')
			self.saved_answer = UserAnswers(user=self.user, question=self.current_question, quiz=self.current_question.quiz, answered = self.answered, working_time = datetime.utcnow())
			self.saved_answer.save()
			return self.saved_answer

	def check_answer(self, saved_answer):
		print('-----------5--------------')
		question_type = saved_answer.question.question_type
		if question_type == 0:
			if int(self.answered) == int(self.correct_answer.id):
				print('-----------6--------------')
				print(self.quiz.title)
				print(self.user_quiz.current_question)
				saved_answer.working_time = datetime(1900,1,1)
				saved_answer.save()

				# user_quiz.save()

				print('-/-/-/-//-', saved_answer.working_time)
				return True

			else:
				print('-----------7--------------')
				return False
		else:
			if self.correct_answer.answer_title in self.answered:
				print('-----------66--------------')
				print(self.quiz.title)
				print(self.user_quiz.current_question)
				saved_answer.working_time = datetime(1900,1,1)
				saved_answer.save()

				# user_quiz.save()

				print('-/-/-/-//-', saved_answer.working_time)
				return True

			else:
				print('-----------77--------------')
				return False



	def check_if_still_closed(self):
		if self._question_exists():
			return self.saved_answer.is_still_closed
		else:
			return False

	def get_next_question(self):
		print('-----------111--------------')
		current_sequence_number = self.current_question.sequence_number
		questions = get_list_or_404(Question, quiz=self.quiz)
		# print(questions)

		new_question_number = REAL_BIG_NUMBER
		for question in questions:
			print(new_question_number, current_sequence_number, '1')
			question_number = question.sequence_number
			if question_number > current_sequence_number:
				print(new_question_number, current_sequence_number, '2')
				if question_number < new_question_number:
					print(new_question_number, current_sequence_number, '3')
					new_question_number = question_number
		
		print(new_question_number, current_sequence_number)
		print('-----------122--------------')
		if new_question_number == REAL_BIG_NUMBER:
			self.user_quiz.is_finished = True
			self.user_quiz.save()
			print('-----------133--------------')
			return None

		else:
			print('-----------144--------------')
			self.next_question =  get_object_or_404(Question, quiz=self.quiz, sequence_number=new_question_number)
			self.user_quiz.current_question = self.next_question
			self.user_quiz.save()
			# print(self.next_question)
			return self.next_question









# form = super(QuestionView, self).post(request, *args, **kwargs)
# current_question = get_object_or_404(Question, slug= self.kwargs['slug'])
# answered = self.request.POST['possible_answers']
# correct_answer = get_object_or_404(Answer, question=current_question, is_correct=True)

# print(current_question, self.request.user)
# saved_answer = open_or_create_answer(self, request)

# print("saved_answer : ", saved_answer)

# quiz = get_object_or_404(Quiz, slug = self.kwargs['quiz_slug'])
# req = get_object_or_404(UserRegisteredQuizzes, user=self.request.user, registered_quiz=quiz)
# user_quiz = get_object_or_404(UserRegisteredQuizzes, user=self.request.user, registered_quiz=quiz)