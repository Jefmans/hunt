"""hunt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
	# path('quizzes/', views.quiz_list, name='quiz_list'),
	path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),
	path('my_quizzes/', views.MyQuizListView.as_view(), name='my_quiz_list'),
    
	path('<slug:slug>/', views.QuizDetailView.as_view(), name='quiz'),
	path('<slug:slug>/add', views.start_new_quiz, name='start_new_quiz'),
	# path('<slug:quiz_slug>/<slug:slug>', views.QuestionDetailView.as_view(), name='question'),
    path('<slug:quiz_slug>/<slug:slug>', views.QuestionView.as_view(), name='question'),


]
