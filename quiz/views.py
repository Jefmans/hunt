from django.shortcuts import render, redirect, get_object_or_404, reverse
from quiz.models import Quiz, Question, Answer
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from users.models import UserRegisteredQuizzes, UserAnswers
from django.contrib.auth.models import User
from django.views.generic import TemplateView, FormView
from users.forms import MultipleAnswerForm, SingleAnswerForm
from datetime import datetime
from quiz.question_handling import AnsweredQuestionHandling

# , SingleAnswerForm

from django.views.generic.edit import FormMixin

# Create your views here.



# def quiz_list(request):
# 	all_quizzes = Quiz.objects.all()

# 	template = 'quiz/quiz_list.html'
# 	context = {
# 		"meta_title": 'Overview of all quizzes',
# 		'quizzes': all_quizzes,
# 		'user': request.user
# 	}

# 	return render(request, template, context)

class QuizListView(ListView):
	template_name = 'quiz/quiz_list.html'
	context_object_name = 'quizzes'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = self.request.user
		context['questions'] = Question.objects.all()
		if self.request.user.is_authenticated:
			context['registered_quizzes'] = Quiz.objects.filter(userregisteredquizzes__user = self.request.user)
		else:
			context['registered_quizzes'] = Quiz.objects.none()
		return context

	def get_queryset(self):
		return Quiz.objects.is_active_and_published()

@method_decorator(login_required, name='dispatch')
class MyQuizListView(ListView):
	template_name = 'quiz/my_quiz_list.html'
	context_object_name = 'quizzes'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = self.request.user
		context['questions'] = Question.objects.all()
		return context

	# def get_queryset(self):
	# 	return Quiz.objects.filter(userregisteredquizzes__user=self.request.user)

	def get_queryset(self):
		return UserRegisteredQuizzes.objects.filter(user = self.request.user)



class QuizDetailView(DetailView):
	model = Quiz
	context_object_name = 'quiz'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context 


@login_required
def start_new_quiz(request, slug):
	# print('SLUG SLUG SLUG SLUG SLUG SLUG', slug)
	quiz = Quiz.objects.get(slug=slug)
	# print('QUIZ QUIZ quiz quiz', quiz)
	# print('&&&&&&&&&&&&&&&', Question.objects.filter(quiz__title=quiz.title))

	try:
		# print('-------------1----------------')
		UserRegisteredQuizzes.objects.get(user=request.user)
	except:
		# print('-------------2----------------')
		saved_user = UserRegisteredQuizzes(user=request.user, registered_quiz=quiz)
	try:
		# print('-------------3----------------')
		# saved_user = UserRegisteredQuizzes.objects.filter(user=user).get(registered_quiz=quiz)
		saved_user = get_object_or_404(UserRegisteredQuizzes, user=user, registered_quiz=quiz)
	except:
		# print('-------------4----------------')
		saved_user = UserRegisteredQuizzes(user=request.user, registered_quiz=quiz)
	# print(quiz, user, saved_user)
	saved_user.save()
	# print(quiz.slug, saved_user.current_question.slug)
	
	return redirect('quiz:question', quiz_slug=quiz.slug, slug=saved_user.current_question.slug)




class QuestionView(FormView):
	template_name = 'quiz/question_detail.html'

	def get_form_class(self, **kwargs):
		current_question = get_object_or_404(Question, slug= self.kwargs['slug'])
		question_type = current_question.question_type
		if question_type == 0 : 
			form_class = MultipleAnswerForm
		else:
			form_class = SingleAnswerForm
		return form_class

	def get_success_url(self, **kwargs):
		return reverse('quiz:question', kwargs={'quiz_slug': self.kwargs['quiz_slug'] , 'slug':self.kwargs['slug']})


	def get_form(self, *args, **kwargs):
		form = super(QuestionView, self).get_form(*args, **kwargs)
		current_question = get_object_or_404(Question, slug= self.kwargs['slug'])
		question_type = current_question.question_type
		if question_type == 0 : 
			form.fields["possible_answers"].queryset = Answer.objects.filter(question=current_question)
		else:
			return form
		return form

	def form_valid(self, *args, **kwargs):
		form = super(QuestionView, self).form_valid(*args, **kwargs)
		return form

	def post(self, request, *args, **kwargs):
		form = super(QuestionView, self).post(request, *args, **kwargs)
		current_question = get_object_or_404(Question, slug= self.kwargs['slug'])
		question_type = current_question.question_type
		
		checking_answer = AnsweredQuestionHandling(self)
		print(checking_answer.saved_answer)
		print('-----------0--------------')

		closed = checking_answer.check_if_still_closed()

		if closed:
			return form
		else:
			pass

		if self.form_invalid(form):
			saved_answer = checking_answer.open_or_create_answer()
			is_correct_answer = checking_answer.check_answer(saved_answer)
			print("correct_answer : ",is_correct_answer)
			print("saved_answer.is_still_closed : ", saved_answer.is_still_closed)
			if is_correct_answer:
				saved_answer.working_time = datetime(1900,1,1)
				saved_answer.save()
				next_question = checking_answer.get_next_question()
				print('-----------222--------------')
				if next_question is not None:
					return redirect('quiz:question', quiz_slug=checking_answer.quiz.slug, slug=next_question.slug)
				else:
					return redirect('/')
			else:
				return form
		else:
			return form


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		current_question = get_object_or_404(Question, slug= self.kwargs['slug'])
		try:
			save_answer = get_object_or_404(UserAnswers, user=self.request.user, question=current_question)
			context['timer'] = save_answer.reopen_date
			context['saved_answer'] = save_answer
		except:
			pass

		context['question'] = current_question
		return context