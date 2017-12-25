from django import forms
from .models import Person, Question_choice, Question_free, Choice, Answer
from django.utils.translation import ugettext_lazy as _

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ()

class AnswerForm1(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('person', 'question')

class AnswerForm2(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('person','question')

class AnswerForm3(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('person', 'question')

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ()





        
         
        


    
