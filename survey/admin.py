from django.contrib import admin

# Register your models here.

from .models import Person, Question_free, Question_choice, Answer, Choice, Answer_choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class Question_choiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Person)
admin.site.register(Question_choice, Question_choiceAdmin)
admin.site.register(Question_free)
admin.site.register(Answer)
admin.site.register(Answer_choice)
