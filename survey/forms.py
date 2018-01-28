from django import forms
from .models import Person, Question, Choice, Answer
from django.utils.translation import ugettext_lazy as _

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ()

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('person', 'question')

        
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ()





        
         
        


    
