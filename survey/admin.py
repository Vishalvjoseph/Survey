from django.contrib import admin

# Register your models here.

from .models import Person, Question, Answer, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        (None,               {'fields': ['questionnaire_type']}),
        (None,               {'fields': ['question_category']}),
        (None,               {'fields': ['question_subcategory']}),
        (None,               {'fields': ['question_type']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Person)
admin.site.register(Answer)
