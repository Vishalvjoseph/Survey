from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=100,
                                          verbose_name="Name",
                                          null=False,
                                          default=None,unique=True
                                          )
    
    def __str__(self):
        return self.name
    

class Question_choice(models.Model):
    person = models.ManyToManyField(Person)
    question_text = models.CharField(max_length=200,
                                     verbose_name="Question name",
                                     default=None
                                     )
    def __str__(self):
        return self.question_text


class Question_free(models.Model):
    question_text = models.CharField(max_length=200,
                                     verbose_name="Question name",
                                     default=None,
                                    )
    person = models.ManyToManyField(Person, through='Answer')
    
    def __str__(self):
        return self.question_text

    
class Answer(models.Model):
    person = models.ForeignKey(Person)
    question = models.ForeignKey(Question_free)
    answer_text = models.CharField(max_length=200, verbose_name="", blank=True)
    def __str__(self):
        return self.answer_text


class Choice(models.Model):
    question_choice = models.ForeignKey(Question_choice, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text

class Answer_choice(models.Model):
    person = models.ForeignKey(Person)
    question = models.ForeignKey(Question_choice)
    answer_text = models.CharField(max_length=200)
    def __str__(self):
        return self.answer_text


    




    
