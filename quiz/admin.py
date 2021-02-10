from django.contrib import admin
from . import models
from hashlib import sha256


# Register your models here.


class QuestionAnswerInline(admin.TabularInline):
	model = models.Answer

	extra = 0
	show_change_link = True


class QuestionAdmin(admin.ModelAdmin):	
	list_display = ('id', 'title', 'question_type', 'sequence_number', 'quiz', 'answer_count', )
	list_editable = ('title', 'question_type', 'quiz', 'sequence_number', )
	list_filter = (
		('quiz', admin.RelatedOnlyFieldListFilter), 
		('quiz__is_active', admin.BooleanFieldListFilter),
		('quiz__is_published', admin.BooleanFieldListFilter),
		)

	fieldsets = (
		(None, {"fields":('title', 'question_type','answer_count', 'quiz', 'description', 'slug')}),)

	readonly_fields = ('answer_count', 'slug')

	search_fields = ("quiz",)

	ordering = ('quiz', 'sequence_number')

	inlines = [QuestionAnswerInline]

	# def get_readonly_fields(self, request, obj=None):
	# 	if obj:
	# 		if obj.question_type == 0:
	# 			return []
	# 		else:
	# 			return ["number_of_answers"]
	# 	else:
	# 		return []


class QuizQuestionInline(admin.TabularInline):
	model = models.Question

	fields = ('title', 'question_type', 'answer_count', 'sequence_number')					
	readonly_fields = ('answer_count',)

	extra = 0
	show_change_link = True


class QuizAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'is_published', 'get_formatted_create_date', 'question_count', 'start_date', 'slug',)
	list_editable = ('is_active', 'is_published')
	# fields = ('title', 'description', 'is_active', 'is_published', 'date_created')
	readonly_fields =('get_formatted_create_date', 'slug')

	inlines = [QuizQuestionInline]

	date_hierarchy = 'date_created'

	def get_formatted_create_date(self, obj):
		if obj:
			return obj.date_created.date()
	get_formatted_create_date.admin_order_field = 'date_created'
	get_formatted_create_date.short_description = 'Created Date'



admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question, QuestionAdmin)
# admin.site.register(models.QuestionType)
admin.site.register(models.Answer)