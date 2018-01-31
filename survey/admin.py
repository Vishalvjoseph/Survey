from django.contrib import admin
from adminsortable.admin import SortableAdmin


# Register your models here.

from .models import Person, Question, Answer_Center, Answer_Worker, Answer_Employer, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0

class AnswerCenterAdmin(admin.ModelAdmin):
    list_display = ('person', 'question', 'answer_text')

class AnswerWorkerAdmin(admin.ModelAdmin):
    list_display = ('person', 'question', 'answer_text')

class AnswerEmployerAdmin(admin.ModelAdmin):
    list_display = ('person', 'question', 'answer_text')

class QuestionAdmin(SortableAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        (None,               {'fields': ['questionnaire_type']}),
        (None,               {'fields': ['question_category']}),
        (None,               {'fields': ['question_type']}),
    ]
    list_display = ('question_text', 'questionnaire_type', 'question_category')
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Person)
admin.site.register(Answer_Center, AnswerCenterAdmin)
admin.site.register(Answer_Worker, AnswerWorkerAdmin)
admin.site.register(Answer_Employer, AnswerEmployerAdmin)
