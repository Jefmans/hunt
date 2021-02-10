from django import forms
from quiz.models import Answer
from .models import UserAnswers
from django.contrib.auth.models import User



class MultipleAnswerForm(forms.Form):
	possible_answers = forms.ModelChoiceField(queryset=Answer.objects.all(), widget = forms.RadioSelect,)


class SingleAnswerForm(forms.Form):
	answer = forms.CharField(max_length=255)


