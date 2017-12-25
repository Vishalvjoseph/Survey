from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import formset_factory
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms.models import inlineformset_factory
from django.views import generic
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Person, Question_choice, Question_free, Choice, Answer, Answer_choice
from .forms import AnswerForm1, AnswerForm2, AnswerForm3, PersonForm
from formtools.wizard.views import SessionWizardView


class PersonList(ListView):
    model = Person
    template_name = 'survey/latest.html'


def Index(request):

    return render(request, 'survey/index.html')

    

def PersonCreate(request):

    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            form.save()
            assign = Person.objects.all().latest('id').id

            return HttpResponseRedirect('/survey/'+str(assign)+'/demofree/')

    else:
        form = PersonForm()

    return render(request, 'survey/person.html', {'form':form})



def Demographics_free(request, person_id):

    question_list = Question_free.objects.all()
    q1 = question_list[0]
    q2 = question_list[1]
    q3 = question_list[2]
    person = get_object_or_404(Person, pk=person_id)
    string = "Demographics - Page 1"

    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1")
        form2 = AnswerForm2(request.POST, prefix="form2")
        form3 = AnswerForm3(request.POST, prefix="form3")
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            answer.save()
        if form2.is_valid():
            answer = form2.save(commit=False)
            answer.question = q2
            answer.person = person
            answer.save()
        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            answer.save()

            return HttpResponseRedirect(reverse('survey:demographics-choice', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1")
        form2 = AnswerForm2(prefix="form2")
        form3 = AnswerForm3(prefix="form3")

    context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/create.html', context)


def Demographics_choice(request, person_id):

    question_list = Question_choice.objects.all()
    q1 = question_list[0]
    q2 = question_list[1]
    q3 = question_list[2]
    person = get_object_or_404(Person, pk=person_id)
    string = "Demographics - Page 2"

    if request.method == 'POST':
        print(request.POST)
        s1 = q1.choice_set.get(pk=request.POST['choice1'])
        s2 = q2.choice_set.get(pk=request.POST['choice2'])
        s3 = q3.choice_set.get(pk=request.POST['choice3'])
        answer = Answer_choice.objects.create(person=person, question=q1, answer_text=s1)
        answer = Answer_choice.objects.create(person=person, question=q2, answer_text=s2)
        answer = Answer_choice.objects.create(person=person, question=q3, answer_text=s3)
        
        return HttpResponseRedirect(reverse('survey:demographics-mix', args=(person.id,)))
    
    else:

        context = {'q1':q1, 'q2':q2, 'q3':q3, 'string':string}

        return render(request, 'survey/choice.html', context)


def Demographics_mix(request, person_id):

    question_list = Question_free.objects.all()
    question_list_choice = Question_choice.objects.all()
    q1 = question_list[3]
    q2 = question_list_choice[3]
    q3 = question_list[4]
    person = get_object_or_404(Person, pk=person_id)
    string = "Demographics - Page 3"

    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1")
        form3 = AnswerForm3(request.POST, prefix="form3")
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            answer.save()

        s2 = q2.choice_set.get(pk=request.POST['choice2'])
        answer = Answer_choice.objects.create(person=person, question=q2, answer_text=s2)

        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            answer.save()
            

        return HttpResponseRedirect(reverse('survey:network-free', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1")
        form3 = AnswerForm3(prefix="form3")

    context = {'form1':form1, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/mix.html', context)


def Network_free(request, person_id):

    question_list = Question_free.objects.all()
    q1 = question_list[5]
    q2 = question_list[6]
    q3 = question_list[7]
    person = get_object_or_404(Person, pk=person_id)
    string = "Job Search - Page 1"

    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1")
        form2 = AnswerForm2(request.POST, prefix="form2")
        form3 = AnswerForm3(request.POST, prefix="form3")
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            answer.save()
        if form2.is_valid():
            answer = form2.save(commit=False)
            answer.question = q2
            answer.person = person
            answer.save()
        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            answer.save()

            return HttpResponseRedirect(reverse('survey:network-choice', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1")
        form2 = AnswerForm2(prefix="form2")
        form3 = AnswerForm3(prefix="form3")

    context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/create.html', context)


def Network_choice(request, person_id):

    question_list = Question_choice.objects.all()
    q1 = question_list[4]
    q2 = question_list[5]
    q3 = question_list[6]
    person = get_object_or_404(Person, pk=person_id)
    string = "Job Search - Page 2"

    if request.method == 'POST':
        print(request.POST)
        s1 = q1.choice_set.get(pk=request.POST['choice1'])
        s2 = q2.choice_set.get(pk=request.POST['choice2'])
        s3 = q3.choice_set.get(pk=request.POST['choice3'])
        answer = Answer_choice.objects.create(person=person, question=q1, answer_text=s1)
        answer = Answer_choice.objects.create(person=person, question=q2, answer_text=s2)
        answer = Answer_choice.objects.create(person=person, question=q3, answer_text=s3)
        
        return HttpResponseRedirect(reverse('survey:network-mix', args=(person.id,)))
    
    else:

        context = {'q1':q1, 'q2':q2, 'q3':q3, 'string':string}

        return render(request, 'survey/choice.html', context)


def Network_mix(request, person_id):

    question_list = Question_free.objects.all()
    question_list_choice = Question_choice.objects.all()
    q1 = question_list[8]
    q2 = question_list_choice[7]
    q3 = question_list[9]
    person = get_object_or_404(Person, pk=person_id)
    string = "Job Search - Page 3"

    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1")
        form3 = AnswerForm3(request.POST, prefix="form3")
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            answer.save()

        s2 = q2.choice_set.get(pk=request.POST['choice2'])
        answer = Answer_choice.objects.create(person=person, question=q2, answer_text=s2)

        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            answer.save()
            

        return HttpResponseRedirect(reverse('survey:work-free', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1")
        form3 = AnswerForm3(prefix="form3")

    context = {'form1':form1, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/mix.html', context)


def Work_free(request, person_id):

    question_list = Question_free.objects.all()
    q1 = question_list[10]
    q2 = question_list[11]
    q3 = question_list[12]
    person = get_object_or_404(Person, pk=person_id)
    string = "Work Experience - Page 1"

    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1")
        form2 = AnswerForm2(request.POST, prefix="form2")
        form3 = AnswerForm3(request.POST, prefix="form3")
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            answer.save()
        if form2.is_valid():
            answer = form2.save(commit=False)
            answer.question = q2
            answer.person = person
            answer.save()
        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            answer.save()

            return HttpResponseRedirect(reverse('survey:work-choice', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1")
        form2 = AnswerForm2(prefix="form2")
        form3 = AnswerForm3(prefix="form3")

    context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/create.html', context)


def Work_choice(request, person_id):

    question_list = Question_choice.objects.all()
    q1 = question_list[8]
    q2 = question_list[9]
    q3 = question_list[10]
    person = get_object_or_404(Person, pk=person_id)
    string = "Work Experience - Page 2"

    if request.method == 'POST':
        print(request.POST)
        s1 = q1.choice_set.get(pk=request.POST['choice1'])
        s2 = q2.choice_set.get(pk=request.POST['choice2'])
        s3 = q3.choice_set.get(pk=request.POST['choice3'])
        answer = Answer_choice.objects.create(person=person, question=q1, answer_text=s1)
        answer = Answer_choice.objects.create(person=person, question=q2, answer_text=s2)
        answer = Answer_choice.objects.create(person=person, question=q3, answer_text=s3)
        
        return HttpResponseRedirect(reverse('survey:work-mix', args=(person.id,)))
    
    else:

        context = {'q1':q1, 'q2':q2, 'q3':q3, 'string':string}

        return render(request, 'survey/choice.html', context)


def Work_mix(request, person_id):

    question_list = Question_free.objects.all()
    question_list_choice = Question_choice.objects.all()
    q1 = question_list[13]
    q2 = question_list_choice[11]
    q3 = question_list[14]
    person = get_object_or_404(Person, pk=person_id)
    string = "Work Experience - Page 3"

    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1")
        form3 = AnswerForm3(request.POST, prefix="form3")
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            answer.save()

        s2 = q2.choice_set.get(pk=request.POST['choice2'])
        answer = Answer_choice.objects.create(person=person, question=q2, answer_text=s2)

        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            answer.save()
            

        return HttpResponseRedirect(reverse('survey:skills-free', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1")
        form3 = AnswerForm3(prefix="form3")

    context = {'form1':form1, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/mix.html', context)


def Skills_free(request, person_id):

    question_list = Question_free.objects.all()
    q1 = question_list[15]
    q2 = question_list[16]
    q3 = question_list[17]
    person = get_object_or_404(Person, pk=person_id)
    string = "Skills - Page 1"

    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1")
        form2 = AnswerForm2(request.POST, prefix="form2")
        form3 = AnswerForm3(request.POST, prefix="form3")
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            answer.save()
        if form2.is_valid():
            answer = form2.save(commit=False)
            answer.question = q2
            answer.person = person
            answer.save()
        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            answer.save()

            return HttpResponseRedirect(reverse('survey:skills-choice', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1")
        form2 = AnswerForm2(prefix="form2")
        form3 = AnswerForm3(prefix="form3")

    context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/create.html', context)


def Skills_choice(request, person_id):

    question_list = Question_choice.objects.all()
    q1 = question_list[12]
    q2 = question_list[13]
    q3 = question_list[14]
    person = get_object_or_404(Person, pk=person_id)
    string = "Skills - Page 2"

    if request.method == 'POST':
        print(request.POST)
        s1 = q1.choice_set.get(pk=request.POST['choice1'])
        s2 = q2.choice_set.get(pk=request.POST['choice2'])
        s3 = q3.choice_set.get(pk=request.POST['choice3'])
        answer = Answer_choice.objects.create(person=person, question=q1, answer_text=s1)
        answer = Answer_choice.objects.create(person=person, question=q2, answer_text=s2)
        answer = Answer_choice.objects.create(person=person, question=q3, answer_text=s3)
        
        return HttpResponseRedirect(reverse('survey:skills-mix', args=(person.id,)))
    
    else:

        context = {'q1':q1, 'q2':q2, 'q3':q3, 'string':string}

        return render(request, 'survey/choice.html', context)


def Skills_mix(request, person_id):

    question_list = Question_free.objects.all()
    question_list_choice = Question_choice.objects.all()
    q1 = question_list[18]
    q2 = question_list_choice[15]
    q3 = question_list[19]
    person = get_object_or_404(Person, pk=person_id)
    string = "Skills - Page 3"

    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1")
        form3 = AnswerForm3(request.POST, prefix="form3")
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            answer.save()

        s2 = q2.choice_set.get(pk=request.POST['choice2'])
        answer = Answer_choice.objects.create(person=person, question=q2, answer_text=s2)

        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            answer.save()
            

        return HttpResponseRedirect(reverse('survey:index'))

    else:
        form1 = AnswerForm1(prefix="form1")
        form3 = AnswerForm3(prefix="form3")

    context = {'form1':form1, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/mix.html', context)



def PersonUpdate(request, pk):

    person = get_object_or_404(Person, pk=pk)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('survey:update-demo', args=(person.id,)))

    else:
        form = PersonForm(instance=person)

    return render(request, 'survey/person.html', {'form':form})
        



def Update_demo(request, person_id):

    question_list = Question_free.objects.all()
    q1 = question_list[0]
    q2 = question_list[1]
    q3 = question_list[2]
    person = get_object_or_404(Person, pk=person_id)
    ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
    ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
    ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
    string = "Demographics"
    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1", instance=ans1)
        form2 = AnswerForm2(request.POST, prefix="form2", instance=ans2)
        form3 = AnswerForm3(request.POST, prefix="form3", instance=ans3)
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            print(answer)
            answer.save()
        if form2.is_valid():
            answer = form2.save(commit=False)
            answer.question = q2
            answer.person = person
            print(answer)
            answer.save()
        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            print(answer)
            answer.save()

            return HttpResponseRedirect(reverse('survey:update-network', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1", instance=ans1)
        form2 = AnswerForm2(prefix="form2", instance=ans2)
        form3 = AnswerForm3(prefix="form3", instance=ans3)

    context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/create.html', context)



def Update_network(request, person_id):

    question_list = Question_free.objects.all()
    q1 = question_list[5]
    q2 = question_list[6]
    q3 = question_list[7]
    person = get_object_or_404(Person, pk=person_id)
    string = "Job Search"

    ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
    ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
    ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1", instance=ans1)
        form2 = AnswerForm2(request.POST, prefix="form2", instance=ans2)
        form3 = AnswerForm3(request.POST, prefix="form3", instance=ans3)
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            print(answer)
            answer.save()
        if form2.is_valid():
            answer = form2.save(commit=False)
            answer.question = q2
            answer.person = person
            print(answer)
            answer.save()
        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            print(answer)
            answer.save()

            return HttpResponseRedirect(reverse('survey:update-work', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1", instance=ans1)
        form2 = AnswerForm2(prefix="form2", instance=ans2)
        form3 = AnswerForm3(prefix="form3", instance=ans3)

    context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/create.html', context)


def Update_work(request, person_id):

    question_list = Question_free.objects.all()
    q1 = question_list[10]
    q2 = question_list[11]
    q3 = question_list[12]
    person = get_object_or_404(Person, pk=person_id)
    string = "Work Experience"

    ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
    ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
    ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1", instance=ans1)
        form2 = AnswerForm2(request.POST, prefix="form2", instance=ans2)
        form3 = AnswerForm3(request.POST, prefix="form3", instance=ans3)
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            print(answer)
            answer.save()
        if form2.is_valid():
            answer = form2.save(commit=False)
            answer.question = q2
            answer.person = person
            print(answer)
            answer.save()
        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            print(answer)
            answer.save()

            return HttpResponseRedirect(reverse('survey:update-skills', args=(person.id,)))

    else:
        form1 = AnswerForm1(prefix="form1", instance=ans1)
        form2 = AnswerForm2(prefix="form2", instance=ans2)
        form3 = AnswerForm3(prefix="form3", instance=ans3)

    context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/create.html', context)


def Update_skills(request, person_id):

    question_list = Question_free.objects.all()
    q1 = question_list[15]
    q2 = question_list[16]
    q3 = question_list[17]
    person = get_object_or_404(Person, pk=person_id)
    string = "Skills"

    ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
    ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
    ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
    
    if request.method == 'POST':
        form1 = AnswerForm1(request.POST, prefix="form1", instance=ans1)
        form2 = AnswerForm2(request.POST, prefix="form2", instance=ans2)
        form3 = AnswerForm3(request.POST, prefix="form3", instance=ans3)
        if form1.is_valid():
            answer = form1.save(commit=False)
            answer.question = q1
            answer.person = person
            print(answer)
            answer.save()
        if form2.is_valid():
            answer = form2.save(commit=False)
            answer.question = q2
            answer.person = person
            print(answer)
            answer.save()
        if form3.is_valid():
            answer = form3.save(commit=False)
            answer.question = q3
            answer.person = person
            print(answer)
            answer.save()

            return HttpResponseRedirect(reverse('survey:index'))

    else:
        form1 = AnswerForm1(prefix="form1", instance=ans1)
        form2 = AnswerForm2(prefix="form2", instance=ans2)
        form3 = AnswerForm3(prefix="form3", instance=ans3)

    context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'string':string}


    return render(request, 'survey/create.html', context)



class PersonDelete(DeleteView):
    model = Person
    template_name = 'survey/delete.html'
    success_url = reverse_lazy('survey:index')





    



    

    




    

    


    



    



    

             
        


        
    
