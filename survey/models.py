from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

#The app has 4 models - Person(stores the name of the person/training centre and the type of survey being taken), Question(stores all the question objects of all types of surveys)
#Answer model(which stores answer objects of all questions of all people/training centers of all surveys, Choice(stores the choices corresponding to a question and is plugged into the Question Admin


CATEGORY = (
        ('training center', 'Training center'),
        ('worker', 'Worker'),
        ('recruiter', 'Recruiter'),)
TYPE = (
    ('free', 'Free'),
    ('choice', 'Choice'),
    ('multiple', 'Multiple'),)


class Person(models.Model):
    name = models.CharField(max_length=100,
                                          verbose_name="Name",
                                          null=False,
                                          default=None,unique=True
                                          )
    questionnaire_type = models.CharField(max_length=100, verbose_name="Questionnaire type", choices=CATEGORY)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.CharField(max_length=500,
                                     verbose_name="Question name",
                                     default=None,
                                    )
    questionnaire_type = models.CharField(max_length=200, verbose_name="Questionnaire type", choices=CATEGORY)
                                    
    question_category = models.CharField(max_length=200,
                                     verbose_name="Category",
                                     default=None,
                                    )
    question_subcategory = models.CharField(max_length=200,
                                     verbose_name="Sub Category",
                                     default=None,
                                    )
    question_type = models.CharField(max_length=200, verbose_name="Question Type", choices=TYPE)

    person = models.ManyToManyField(Person, through='Answer')
    
    def __str__(self):
        return self.question_text

    
class Answer(models.Model):
    person = models.ForeignKey(Person)
    question = models.ForeignKey(Question)
    answer_text = models.CharField(max_length=200, verbose_name="", blank=True)
    def __str__(self):
        return self.answer_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text


    




    
