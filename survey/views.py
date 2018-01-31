from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.views import generic
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Person, Question, Choice, Answer_Center, Answer_Worker, Answer_Employer
from .forms import PersonForm, AnswerCenterForm, AnswerWorkerForm, AnswerEmployerForm


class PersonList(ListView):       #lists out the latest surveys
    model = Person  
    template_name = 'survey/latest.html'


def Index(request):                #displays the homepage

    return render(request, 'survey/index.html')



def PersonCreate(request):          #creates the Person object

    if request.method == 'POST':
        form = PersonForm(request.POST)    #uses the PersonForm which is based on the Person model
        val = request.POST.getlist('form-answer_text', '')
        if form.is_valid():
            form.save()
            assign = Person.objects.all().latest('id').id
            start = 0
            finish = 3
            return HttpResponseRedirect(reverse('survey:detail-create', args=(assign,)))

    else:
        form = PersonForm(prefix="form")

    return render(request, 'survey/person.html', {'form':form})


def PersonUpdate(request, pk):    # The view that helps in editing the name of a person already enetred into the db

    person = get_object_or_404(Person, pk=pk)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)

        if form.is_valid():
            form.save()
            start = 0
            finish = 3

            return HttpResponseRedirect(reverse('survey:detail-update', args=(person.id,)))

    else:
        form = PersonForm(instance=person)

    return render(request, 'survey/person.html', {'form':form})


class PersonDelete(DeleteView):   #view for deleting the required Person objects
    model = Person
    template_name = 'survey/delete.html'
    success_url = reverse_lazy('survey:latest')



# Training Center code


def DetailCenter_create(request, person_id):    #this view displays the various sections of the survey and redirects to the Create view 

    start = 0
    finish = 3
    status_1 = 1
    status_2 = 2
    status_3 = 3
    status_4 = 4
    
    context = {'start':start, 'finish':finish, 'person_id':person_id, 'status_1':status_1, 'status_2':status_2, 'status_3':status_3, 'status_4':status_4}
    
    return render(request, 'survey/detail_create.html', context)



def Create_Center(request, person_id, start, finish, status):      #This is the view in which all answer objects are created

    start = int(start)
    finish = int(finish)
    status = int(status)

    if status == 1:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")[start:finish]
    elif status == 2:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")[start:finish]
    elif status == 3:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")[start:finish]
    else:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")[start:finish]
    
##    question_all = Question.objects.filter(question_category=str(category['string1'])).filter(question_category=str(category['string2']))
##    question_list = Question.objects.filter(question_category=str(category['string1'])).filter(question_category=str(category['string2']))[start:finish]
    
    person = get_object_or_404(Person, pk=person_id)
    start = start + 3
    finish = finish + 3
    total = len(question_all)


    if request.method == 'POST':
            
        print(request.POST)
        i = 0
        j = 0

        for q in question_list:
            print(i)
            if q.question_type == 'free':
                form = AnswerForm(request.POST, prefix="form")
                if form.is_valid():
                    values = request.POST.getlist('form-answer_text', '')
                    answer = Answer.objects.create(person=person, question=q, answer_text=values[i])
                    i = i+1
                        
            elif q.question_type == 'choice':
                s1 = q.choice_set.get(pk=request.POST.get(str(q.id)))
                if str(s1) == 'Other':
                    form_other = AnswerForm(request.POST, prefix="form_choice")
                    if form_other.is_valid():
                        values_other = request.POST.getlist('form_choice-answer_text', '')
                        answer = Answer.objects.create(person=person, question=q, answer_text=values_other[j])
                        j = j+1

                else:
                    answer = Answer.objects.create(person=person, question=q, answer_text=s1)
    
            else:
                print(request.POST.getlist(str(q.id), ''))
                li = request.POST.getlist(str(q.id), '')
                tot=len(li)
                for k in range(0,tot):
                    s1 = q.choice_set.get(pk=li[k])
                    answer = Answer.objects.create(person=person, question=q, answer_text=s1)

                

        if finish >= total+3:
            return HttpResponseRedirect(reverse('survey:detail-create', args=(person.id,)))

        else:
            return HttpResponseRedirect(reverse('survey:create', args=(person.id, start, finish, status)))


    else:
        form = AnswerForm(prefix="form")
        form_other = AnswerForm(prefix="form_choice")
        
        context = {'form':form, 'form_other':form_other, 'question_list':question_list}

        return render(request, 'survey/create.html', context)

def DetailCenter_update(request, person_id):     # Displays the various sections of the survey that can be edited/updated

    start = 0
    finish = 3
    status_1 = 1
    status_2 = 2
    status_3 = 3
    status_4 = 4

    context = {'start':start, 'finish':finish, 'status_1':status_1, 'status_2':status_2, 'status_3':status_3, 'status_4':status_4, 'person_id':person_id}
    
    return render(request, 'survey/detail_update.html', context)


def Update_Center(request, person_id, start, finish, status):   # Updates the answer objects

    start = int(start)
    finish = int(finish)
    status = int(status)

    if status == 1:              #The necessary question lists are generated depending on the link clicked in the previous view
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")[start:finish]
    elif status == 2:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")[start:finish]
    elif status == 3:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")[start:finish]
    else:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")[start:finish]


    if len(question_list) == 3:   # This block assigns the questions from the list to individual objects
        q1 = question_list[0]
        q2 = question_list[1]
        q3 = question_list[2]

    elif len(question_list) == 2:
        q1 = question_list[0]
        q2 = question_list[1]
        q3 = None 

    else:
        q1 = question_list[0]
        q2 = None
        q3 = None

    
    person = get_object_or_404(Person, pk=person_id)
    start = start + 3  # increments the value of start and finish to proceed to the next set of question_list
    finish = finish + 3
    total = len(question_all)
    
    ans1 = None
    ans2 = None
    ans3 = None
    ans_list_choice1 = list() #list declared for storing choices
    ans_list_multi1 = list()  #list declared for storing multiple choice objects
    ans_list_choice2 = list()
    ans_list_multi2 = list()
    ans_list_choice3 = list()
    ans_list_multi3 = list()

    if q1 is not None:
        if q1.question_type == 'multiple':
            multi = Answer.objects.filter(person=person).filter(question=q1) 
            print(multi)
            for i in range(0,len(multi)):
                ans_list_multi1.append(multi[i].answer_text)
        elif q1.question_type == 'choice':
            ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
            choice_list = q1.choice_set.all()
            for i in range(0,len(choice_list)):
                ans_list_choice1.append(choice_list[i].choice_text)
        else:
            ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
        
        
    if q2 is not None:
        if q2.question_type == 'multiple':
            multi = Answer.objects.filter(person=person).filter(question=q2)
            for i in range(0,len(multi)):
                ans_list_multi2.append(multi[i].answer_text)
        elif q2.question_type == 'choice':
            ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
            choice_list = q2.choice_set.all()
            for i in range(0,len(choice_list)):
                ans_list_choice2.append(choice_list[i].choice_text)
        else:
            ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
        

    if q3 is not None:
        if q3.question_type == 'multiple':
            multi = Answer.objects.filter(person=person).filter(question=q3)
            for i in range(0,len(multi)):
                ans_list_multi3.append(multi[i].answer_text)
        elif q3.question_type == 'choice':
            ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
            choice_list = q3.choice_set.all()
            for i in range(0,len(choice_list)):
                ans_list_choice3.append(choice_list[i].choice_text)
        else:
            ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
           
        
    if request.method == 'POST':
        if q1 is not None:
            if q1.question_type == 'free':
                form1 = AnswerForm(request.POST, prefix="form1", instance=ans1)
                if form1.is_valid():
                    ans1 = form1.save(commit=False)
                    ans1.question = q1
                    ans1.person = person
                    ans1.save()

            elif q1.question_type == 'choice':
                s1 = q1.choice_set.get(pk=request.POST['choice1'])
                if str(s1) == 'Other':
                    form1 = AnswerForm(request.POST, prefix="form1", instance=ans1)
                    if form1.is_valid():
                        ans1 = form1.save(commit=False)
                        ans1.question = q1
                        ans1.person = person
                        ans1.save()
                else:
                    ans1.answer_text = s1.choice_text
                    print(ans1)
                    ans1.question = q1
                    ans1.person = person
                    ans1.save()
                    

            else:
                li = request.POST.getlist("choice1", '')
                multi = Answer.objects.filter(person=person).filter(question=q1)
                multi.delete()
                tot=len(li)
                for i in range(0,tot):
                    s1 = q1.choice_set.get(pk=li[i])
                    answer = Answer.objects.create(person=person, question=q1, answer_text=s1)
                    


        if q2 is not None:

            if q2.question_type == 'free':
                form2 = AnswerForm(request.POST, prefix="form2", instance=ans2)
                if form2.is_valid():
                    ans2 = form2.save(commit=False)
                    ans2.question = q2
                    ans2.person = person
                    ans2.save()

            elif q2.question_type == 'choice':
                s2 = q2.choice_set.get(pk=request.POST['choice2'])
                if str(s2) == 'Other':
                    form2 = AnswerForm(request.POST, prefix="form2", instance=ans2)
                    if form2.is_valid():
                        ans2 = form2.save(commit=False)
                        ans2.question = q2
                        ans2.person = person
                        ans2.save()
                else:
                    ans2.answer_text = s2.choice_text
                    ans2.question = q2
                    ans2.person = person
                    ans2.save()

            else:
                li = request.POST.getlist("choice2", '')
                multi = Answer.objects.filter(person=person).filter(question=q2)
                multi.delete()
                tot=len(li)
                for i in range(0,tot):
                    s2 = q2.choice_set.get(pk=li[i])
                    answer = Answer.objects.create(person=person, question=q2, answer_text=s2)


        if q3 is not None:

            if q3.question_type == 'free':
                form3 = AnswerForm(request.POST, prefix="form3", instance=ans3)
                if form3.is_valid():  
                    ans3 = form3.save(commit=False)
                    ans3.question = q3
                    ans3.person = person
                    ans3.save()   #updates answer
                    
            elif q3.question_type == 'choice':
                s3 = q3.choice_set.get(pk=request.POST['choice3'])
                if str(s3) == 'Other':
                    form3 = AnswerForm(request.POST, prefix="form3", instance=ans3)
                    if form3.is_valid():
                        ans3 = form3.save(commit=False)
                        ans3.question = q3
                        ans3.person = person
                        ans3.save()
                else:
                    ans3.answer_text = s3.choice_text
                    ans3.question = q3
                    ans3.person = person
                    ans3.save()  #updates answer 

            else:
                li = request.POST.getlist("choice3", '')
                multi = Answer.objects.filter(person=person).filter(question=q3)
                multi.delete()
                tot=len(li)
                for i in range(0,tot):
                    s3 = q3.choice_set.get(pk=li[i])
                    answer = Answer.objects.create(person=person, question=q3, answer_text=s3) #creates new objects after deleting the old ones so that there is no redundancy

        if finish >= total+3:   #checks if condition has been met to generate next list of questions
            return HttpResponseRedirect(reverse('survey:detail-update', args=(person.id,)))

        else:
            return HttpResponseRedirect(reverse('survey:update', args=(person.id, start, finish, status))) #redirects back to same view to process/display next set of questions in the same list
        

    else:
        form1 = AnswerForm(prefix="form1", instance=ans1)
        form2 = AnswerForm(prefix="form2", instance=ans2)
        form3 = AnswerForm(prefix="form3", instance=ans3)

        context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'ans1':ans1, 'ans2':ans2, 'ans3':ans3, 'ans_list_choice1':ans_list_choice1, 'ans_list_multi1':ans_list_multi1, 'ans_list_choice2':ans_list_choice2, 'ans_list_multi2':ans_list_multi2, 'ans_list_choice3':ans_list_choice3, 'ans_list_multi3':ans_list_multi3}

        return render(request, 'survey/update.html', context)


# Worker Code


def DetailWorker_create(request, person_id):    #this view displays the various sections of the survey and redirects to the Create view 

    start = 0
    finish = 3
    status_1 = 1
    status_2 = 2
    status_3 = 3
    status_4 = 4
    
    context = {'start':start, 'finish':finish, 'person_id':person_id, 'status_1':status_1, 'status_2':status_2, 'status_3':status_3, 'status_4':status_4}
    
    return render(request, 'survey/detail_create.html', context)


def Create_Worker(request, person_id, start, finish, status):      #This is the view in which all answer objects are created

    start = int(start)
    finish = int(finish)
    status = int(status)

    if status == 1:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")[start:finish]
    elif status == 2:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")[start:finish]
    elif status == 3:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")[start:finish]
    else:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")[start:finish]
    
##    question_all = Question.objects.filter(question_category=str(category['string1'])).filter(question_category=str(category['string2']))
##    question_list = Question.objects.filter(question_category=str(category['string1'])).filter(question_category=str(category['string2']))[start:finish]
    
    person = get_object_or_404(Person, pk=person_id)
    start = start + 3
    finish = finish + 3
    total = len(question_all)


    if request.method == 'POST':
            
        print(request.POST)
        i = 0
        j = 0

        for q in question_list:
            print(i)
            if q.question_type == 'free':
                form = AnswerForm(request.POST, prefix="form")
                if form.is_valid():
                    values = request.POST.getlist('form-answer_text', '')
                    answer = Answer.objects.create(person=person, question=q, answer_text=values[i])
                    i = i+1
                        
            elif q.question_type == 'choice':
                s1 = q.choice_set.get(pk=request.POST.get(str(q.id)))
                if str(s1) == 'Other':
                    form_other = AnswerForm(request.POST, prefix="form_choice")
                    if form_other.is_valid():
                        values_other = request.POST.getlist('form_choice-answer_text', '')
                        answer = Answer.objects.create(person=person, question=q, answer_text=values_other[j])
                        j = j+1

                else:
                    answer = Answer.objects.create(person=person, question=q, answer_text=s1)
    
            else:
                print(request.POST.getlist(str(q.id), ''))
                li = request.POST.getlist(str(q.id), '')
                tot=len(li)
                for k in range(0,tot):
                    s1 = q.choice_set.get(pk=li[k])
                    answer = Answer.objects.create(person=person, question=q, answer_text=s1)

                

        if finish >= total+3:
            return HttpResponseRedirect(reverse('survey:detail-create', args=(person.id,)))

        else:
            return HttpResponseRedirect(reverse('survey:create', args=(person.id, start, finish, status)))


    else:
        form = AnswerForm(prefix="form")
        form_other = AnswerForm(prefix="form_choice")
        
        context = {'form':form, 'form_other':form_other, 'question_list':question_list}

        return render(request, 'survey/create.html', context)


def DetailWorker_update(request, person_id):     # Displays the various sections of the survey that can be edited/updated

    start = 0
    finish = 3
    status_1 = 1
    status_2 = 2
    status_3 = 3
    status_4 = 4

    context = {'start':start, 'finish':finish, 'status_1':status_1, 'status_2':status_2, 'status_3':status_3, 'status_4':status_4, 'person_id':person_id}
    
    return render(request, 'survey/detail_update.html', context)


def Update_Worker(request, person_id, start, finish, status):   # Updates the answer objects

    start = int(start)
    finish = int(finish)
    status = int(status)

    if status == 1:              #The necessary question lists are generated depending on the link clicked in the previous view
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")[start:finish]
    elif status == 2:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")[start:finish]
    elif status == 3:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")[start:finish]
    else:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")[start:finish]


    if len(question_list) == 3:   # This block assigns the questions from the list to individual objects
        q1 = question_list[0]
        q2 = question_list[1]
        q3 = question_list[2]

    elif len(question_list) == 2:
        q1 = question_list[0]
        q2 = question_list[1]
        q3 = None 

    else:
        q1 = question_list[0]
        q2 = None
        q3 = None

    
    person = get_object_or_404(Person, pk=person_id)
    start = start + 3  # increments the value of start and finish to proceed to the next set of question_list
    finish = finish + 3
    total = len(question_all)
    
    ans1 = None
    ans2 = None
    ans3 = None
    ans_list_choice1 = list() #list declared for storing choices
    ans_list_multi1 = list()  #list declared for storing multiple choice objects
    ans_list_choice2 = list()
    ans_list_multi2 = list()
    ans_list_choice3 = list()
    ans_list_multi3 = list()

    if q1 is not None:
        if q1.question_type == 'multiple':
            multi = Answer.objects.filter(person=person).filter(question=q1) 
            print(multi)
            for i in range(0,len(multi)):
                ans_list_multi1.append(multi[i].answer_text)
        elif q1.question_type == 'choice':
            ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
            choice_list = q1.choice_set.all()
            for i in range(0,len(choice_list)):
                ans_list_choice1.append(choice_list[i].choice_text)
        else:
            ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
        
        
    if q2 is not None:
        if q2.question_type == 'multiple':
            multi = Answer.objects.filter(person=person).filter(question=q2)
            for i in range(0,len(multi)):
                ans_list_multi2.append(multi[i].answer_text)
        elif q2.question_type == 'choice':
            ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
            choice_list = q2.choice_set.all()
            for i in range(0,len(choice_list)):
                ans_list_choice2.append(choice_list[i].choice_text)
        else:
            ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
        

    if q3 is not None:
        if q3.question_type == 'multiple':
            multi = Answer.objects.filter(person=person).filter(question=q3)
            for i in range(0,len(multi)):
                ans_list_multi3.append(multi[i].answer_text)
        elif q3.question_type == 'choice':
            ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
            choice_list = q3.choice_set.all()
            for i in range(0,len(choice_list)):
                ans_list_choice3.append(choice_list[i].choice_text)
        else:
            ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
           
        
    if request.method == 'POST':
        if q1 is not None:
            if q1.question_type == 'free':
                form1 = AnswerForm(request.POST, prefix="form1", instance=ans1)
                if form1.is_valid():
                    ans1 = form1.save(commit=False)
                    ans1.question = q1
                    ans1.person = person
                    ans1.save()

            elif q1.question_type == 'choice':
                s1 = q1.choice_set.get(pk=request.POST['choice1'])
                if str(s1) == 'Other':
                    form1 = AnswerForm(request.POST, prefix="form1", instance=ans1)
                    if form1.is_valid():
                        ans1 = form1.save(commit=False)
                        ans1.question = q1
                        ans1.person = person
                        ans1.save()
                else:
                    ans1.answer_text = s1.choice_text
                    print(ans1)
                    ans1.question = q1
                    ans1.person = person
                    ans1.save()
                    

            else:
                li = request.POST.getlist("choice1", '')
                multi = Answer.objects.filter(person=person).filter(question=q1)
                multi.delete()
                tot=len(li)
                for i in range(0,tot):
                    s1 = q1.choice_set.get(pk=li[i])
                    answer = Answer.objects.create(person=person, question=q1, answer_text=s1)
                    


        if q2 is not None:

            if q2.question_type == 'free':
                form2 = AnswerForm(request.POST, prefix="form2", instance=ans2)
                if form2.is_valid():
                    ans2 = form2.save(commit=False)
                    ans2.question = q2
                    ans2.person = person
                    ans2.save()

            elif q2.question_type == 'choice':
                s2 = q2.choice_set.get(pk=request.POST['choice2'])
                if str(s2) == 'Other':
                    form2 = AnswerForm(request.POST, prefix="form2", instance=ans2)
                    if form2.is_valid():
                        ans2 = form2.save(commit=False)
                        ans2.question = q2
                        ans2.person = person
                        ans2.save()
                else:
                    ans2.answer_text = s2.choice_text
                    ans2.question = q2
                    ans2.person = person
                    ans2.save()

            else:
                li = request.POST.getlist("choice2", '')
                multi = Answer.objects.filter(person=person).filter(question=q2)
                multi.delete()
                tot=len(li)
                for i in range(0,tot):
                    s2 = q2.choice_set.get(pk=li[i])
                    answer = Answer.objects.create(person=person, question=q2, answer_text=s2)


        if q3 is not None:

            if q3.question_type == 'free':
                form3 = AnswerForm(request.POST, prefix="form3", instance=ans3)
                if form3.is_valid():  
                    ans3 = form3.save(commit=False)
                    ans3.question = q3
                    ans3.person = person
                    ans3.save()   #updates answer
                    
            elif q3.question_type == 'choice':
                s3 = q3.choice_set.get(pk=request.POST['choice3'])
                if str(s3) == 'Other':
                    form3 = AnswerForm(request.POST, prefix="form3", instance=ans3)
                    if form3.is_valid():
                        ans3 = form3.save(commit=False)
                        ans3.question = q3
                        ans3.person = person
                        ans3.save()
                else:
                    ans3.answer_text = s3.choice_text
                    ans3.question = q3
                    ans3.person = person
                    ans3.save()  #updates answer 

            else:
                li = request.POST.getlist("choice3", '')
                multi = Answer.objects.filter(person=person).filter(question=q3)
                multi.delete()
                tot=len(li)
                for i in range(0,tot):
                    s3 = q3.choice_set.get(pk=li[i])
                    answer = Answer.objects.create(person=person, question=q3, answer_text=s3) #creates new objects after deleting the old ones so that there is no redundancy

        if finish >= total+3:   #checks if condition has been met to generate next list of questions
            return HttpResponseRedirect(reverse('survey:detail-update', args=(person.id,)))

        else:
            return HttpResponseRedirect(reverse('survey:update', args=(person.id, start, finish, status))) #redirects back to same view to process/display next set of questions in the same list
        

    else:
        form1 = AnswerForm(prefix="form1", instance=ans1)
        form2 = AnswerForm(prefix="form2", instance=ans2)
        form3 = AnswerForm(prefix="form3", instance=ans3)

        context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'ans1':ans1, 'ans2':ans2, 'ans3':ans3, 'ans_list_choice1':ans_list_choice1, 'ans_list_multi1':ans_list_multi1, 'ans_list_choice2':ans_list_choice2, 'ans_list_multi2':ans_list_multi2, 'ans_list_choice3':ans_list_choice3, 'ans_list_multi3':ans_list_multi3}

        return render(request, 'survey/update.html', context)



# Employer code


def DetailEmployer_create(request, person_id):    #this view displays the various sections of the survey and redirects to the Create view 

    start = 0
    finish = 3
    status_1 = 1
    status_2 = 2
    status_3 = 3
    status_4 = 4
    
    context = {'start':start, 'finish':finish, 'person_id':person_id, 'status_1':status_1, 'status_2':status_2, 'status_3':status_3, 'status_4':status_4}
    
    return render(request, 'survey/detail_create.html', context)



def Create_Employer(request, person_id, start, finish, status):      #This is the view in which all answer objects are created

    start = int(start)
    finish = int(finish)
    status = int(status)

    if status == 1:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")[start:finish]
    elif status == 2:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")[start:finish]
    elif status == 3:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")[start:finish]
    else:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")[start:finish]
    
##    question_all = Question.objects.filter(question_category=str(category['string1'])).filter(question_category=str(category['string2']))
##    question_list = Question.objects.filter(question_category=str(category['string1'])).filter(question_category=str(category['string2']))[start:finish]
    
    person = get_object_or_404(Person, pk=person_id)
    start = start + 3
    finish = finish + 3
    total = len(question_all)


    if request.method == 'POST':
            
        print(request.POST)
        i = 0
        j = 0

        for q in question_list:
            print(i)
            if q.question_type == 'free':
                form = AnswerForm(request.POST, prefix="form")
                if form.is_valid():
                    values = request.POST.getlist('form-answer_text', '')
                    answer = Answer.objects.create(person=person, question=q, answer_text=values[i])
                    i = i+1
                        
            elif q.question_type == 'choice':
                s1 = q.choice_set.get(pk=request.POST.get(str(q.id)))
                if str(s1) == 'Other':
                    form_other = AnswerForm(request.POST, prefix="form_choice")
                    if form_other.is_valid():
                        values_other = request.POST.getlist('form_choice-answer_text', '')
                        answer = Answer.objects.create(person=person, question=q, answer_text=values_other[j])
                        j = j+1

                else:
                    answer = Answer.objects.create(person=person, question=q, answer_text=s1)
    
            else:
                print(request.POST.getlist(str(q.id), ''))
                li = request.POST.getlist(str(q.id), '')
                tot=len(li)
                for k in range(0,tot):
                    s1 = q.choice_set.get(pk=li[k])
                    answer = Answer.objects.create(person=person, question=q, answer_text=s1)

                

        if finish >= total+3:
            return HttpResponseRedirect(reverse('survey:detail-create', args=(person.id,)))

        else:
            return HttpResponseRedirect(reverse('survey:create', args=(person.id, start, finish, status)))


    else:
        form = AnswerForm(prefix="form")
        form_other = AnswerForm(prefix="form_choice")
        
        context = {'form':form, 'form_other':form_other, 'question_list':question_list}

        return render(request, 'survey/create.html', context)



def DetailEmployer_update(request, person_id):     # Displays the various sections of the survey that can be edited/updated

    start = 0
    finish = 3
    status_1 = 1
    status_2 = 2
    status_3 = 3
    status_4 = 4

    context = {'start':start, 'finish':finish, 'status_1':status_1, 'status_2':status_2, 'status_3':status_3, 'status_4':status_4, 'person_id':person_id}
    
    return render(request, 'survey/detail_update.html', context)


def Update_Employer(request, person_id, start, finish, status):   # Updates the answer objects

    start = int(start)
    finish = int(finish)
    status = int(status)

    if status == 1:              #The necessary question lists are generated depending on the link clicked in the previous view
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Job Characteristics")[start:finish]
    elif status == 2:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Skills and Worker Characteristics")[start:finish]
    elif status == 3:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Recruitment")[start:finish]
    else:
        question_all = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")
        question_list = Question.objects.filter(questionnaire_type="training center").filter(question_category="Placement")[start:finish]


    if len(question_list) == 3:   # This block assigns the questions from the list to individual objects
        q1 = question_list[0]
        q2 = question_list[1]
        q3 = question_list[2]

    elif len(question_list) == 2:
        q1 = question_list[0]
        q2 = question_list[1]
        q3 = None 

    else:
        q1 = question_list[0]
        q2 = None
        q3 = None

    
    person = get_object_or_404(Person, pk=person_id)
    start = start + 3  # increments the value of start and finish to proceed to the next set of question_list
    finish = finish + 3
    total = len(question_all)
    
    ans1 = None
    ans2 = None
    ans3 = None
    ans_list_choice1 = list() #list declared for storing choices
    ans_list_multi1 = list()  #list declared for storing multiple choice objects
    ans_list_choice2 = list()
    ans_list_multi2 = list()
    ans_list_choice3 = list()
    ans_list_multi3 = list()

    if q1 is not None:
        if q1.question_type == 'multiple':
            multi = Answer.objects.filter(person=person).filter(question=q1) 
            print(multi)
            for i in range(0,len(multi)):
                ans_list_multi1.append(multi[i].answer_text)
        elif q1.question_type == 'choice':
            ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
            choice_list = q1.choice_set.all()
            for i in range(0,len(choice_list)):
                ans_list_choice1.append(choice_list[i].choice_text)
        else:
            ans1 = Answer.objects.filter(person=person).filter(question=q1).first()
        
        
    if q2 is not None:
        if q2.question_type == 'multiple':
            multi = Answer.objects.filter(person=person).filter(question=q2)
            for i in range(0,len(multi)):
                ans_list_multi2.append(multi[i].answer_text)
        elif q2.question_type == 'choice':
            ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
            choice_list = q2.choice_set.all()
            for i in range(0,len(choice_list)):
                ans_list_choice2.append(choice_list[i].choice_text)
        else:
            ans2 = Answer.objects.filter(person=person).filter(question=q2).first()
        

    if q3 is not None:
        if q3.question_type == 'multiple':
            multi = Answer.objects.filter(person=person).filter(question=q3)
            for i in range(0,len(multi)):
                ans_list_multi3.append(multi[i].answer_text)
        elif q3.question_type == 'choice':
            ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
            choice_list = q3.choice_set.all()
            for i in range(0,len(choice_list)):
                ans_list_choice3.append(choice_list[i].choice_text)
        else:
            ans3 = Answer.objects.filter(person=person).filter(question=q3).first()
           
        
    if request.method == 'POST':
        if q1 is not None:
            if q1.question_type == 'free':
                form1 = AnswerForm(request.POST, prefix="form1", instance=ans1)
                if form1.is_valid():
                    ans1 = form1.save(commit=False)
                    ans1.question = q1
                    ans1.person = person
                    ans1.save()

            elif q1.question_type == 'choice':
                s1 = q1.choice_set.get(pk=request.POST['choice1'])
                if str(s1) == 'Other':
                    form1 = AnswerForm(request.POST, prefix="form1", instance=ans1)
                    if form1.is_valid():
                        ans1 = form1.save(commit=False)
                        ans1.question = q1
                        ans1.person = person
                        ans1.save()
                else:
                    ans1.answer_text = s1.choice_text
                    print(ans1)
                    ans1.question = q1
                    ans1.person = person
                    ans1.save()
                    

            else:
                li = request.POST.getlist("choice1", '')
                multi = Answer.objects.filter(person=person).filter(question=q1)
                multi.delete()
                tot=len(li)
                for i in range(0,tot):
                    s1 = q1.choice_set.get(pk=li[i])
                    answer = Answer.objects.create(person=person, question=q1, answer_text=s1)
                    


        if q2 is not None:

            if q2.question_type == 'free':
                form2 = AnswerForm(request.POST, prefix="form2", instance=ans2)
                if form2.is_valid():
                    ans2 = form2.save(commit=False)
                    ans2.question = q2
                    ans2.person = person
                    ans2.save()

            elif q2.question_type == 'choice':
                s2 = q2.choice_set.get(pk=request.POST['choice2'])
                if str(s2) == 'Other':
                    form2 = AnswerForm(request.POST, prefix="form2", instance=ans2)
                    if form2.is_valid():
                        ans2 = form2.save(commit=False)
                        ans2.question = q2
                        ans2.person = person
                        ans2.save()
                else:
                    ans2.answer_text = s2.choice_text
                    ans2.question = q2
                    ans2.person = person
                    ans2.save()

            else:
                li = request.POST.getlist("choice2", '')
                multi = Answer.objects.filter(person=person).filter(question=q2)
                multi.delete()
                tot=len(li)
                for i in range(0,tot):
                    s2 = q2.choice_set.get(pk=li[i])
                    answer = Answer.objects.create(person=person, question=q2, answer_text=s2)


        if q3 is not None:

            if q3.question_type == 'free':
                form3 = AnswerForm(request.POST, prefix="form3", instance=ans3)
                if form3.is_valid():  
                    ans3 = form3.save(commit=False)
                    ans3.question = q3
                    ans3.person = person
                    ans3.save()   #updates answer
                    
            elif q3.question_type == 'choice':
                s3 = q3.choice_set.get(pk=request.POST['choice3'])
                if str(s3) == 'Other':
                    form3 = AnswerForm(request.POST, prefix="form3", instance=ans3)
                    if form3.is_valid():
                        ans3 = form3.save(commit=False)
                        ans3.question = q3
                        ans3.person = person
                        ans3.save()
                else:
                    ans3.answer_text = s3.choice_text
                    ans3.question = q3
                    ans3.person = person
                    ans3.save()  #updates answer 

            else:
                li = request.POST.getlist("choice3", '')
                multi = Answer.objects.filter(person=person).filter(question=q3)
                multi.delete()
                tot=len(li)
                for i in range(0,tot):
                    s3 = q3.choice_set.get(pk=li[i])
                    answer = Answer.objects.create(person=person, question=q3, answer_text=s3) #creates new objects after deleting the old ones so that there is no redundancy

        if finish >= total+3:   #checks if condition has been met to generate next list of questions
            return HttpResponseRedirect(reverse('survey:detail-update', args=(person.id,)))

        else:
            return HttpResponseRedirect(reverse('survey:update', args=(person.id, start, finish, status))) #redirects back to same view to process/display next set of questions in the same list
        

    else:
        form1 = AnswerForm(prefix="form1", instance=ans1)
        form2 = AnswerForm(prefix="form2", instance=ans2)
        form3 = AnswerForm(prefix="form3", instance=ans3)

        context = {'form1':form1, 'form2':form2, 'form3':form3, 'q1':q1, 'q2':q2, 'q3':q3, 'ans1':ans1, 'ans2':ans2, 'ans3':ans3, 'ans_list_choice1':ans_list_choice1, 'ans_list_multi1':ans_list_multi1, 'ans_list_choice2':ans_list_choice2, 'ans_list_multi2':ans_list_multi2, 'ans_list_choice3':ans_list_choice3, 'ans_list_multi3':ans_list_multi3}

        return render(request, 'survey/update.html', context) 
    








    



    

    




    

    


    



    



    

             
        


        
    
