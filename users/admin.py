from django.contrib import admin
from .models import UserRegisteredQuizzes, UserAnswers

# Register your models here.

class UserRegisteredQuizzesAdmin(admin.ModelAdmin):	
	list_display = ('user', 'get_user_email', 'registered_quiz', 'current_question', 'is_finished')


admin.site.register(UserRegisteredQuizzes, UserRegisteredQuizzesAdmin)
admin.site.register(UserAnswers)