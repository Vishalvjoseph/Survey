from django import forms
from .models import Person, Question, Choice, Answer_Center, Answer_Worker, Answer_Employer
from django.utils.translation import ugettext_lazy as _


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ()

class AnswerCenterForm(forms.ModelForm):
    class Meta:
        model = Answer_Center
        exclude = ('person', 'question')

class AnswerWorkerForm(forms.ModelForm):
    class Meta:
        model = Answer_Worker
        exclude = ('person', 'question')

class AnswerEmployerForm(forms.ModelForm):
    class Meta:
        model = Answer_Employer
        exclude = ('person', 'question')
        
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ()

        





        
         
        


    
