from django.conf.urls import url
from . import views
from .forms import AnswerForm1, AnswerForm2, AnswerForm3, PersonForm
from survey.views import Demographics_free, Demographics_choice, Demographics_mix, Network_free, Network_choice, Network_mix, Work_free, Work_choice, Work_mix, Skills_free, Skills_choice, Skills_mix, PersonDelete, PersonCreate, Update_demo, Update_network, Update_work, Update_skills, PersonUpdate, Index


app_name = 'survey'
urlpatterns = [
    url(r'^$', views.Index, name='index'),
    url(r'^latest/$', views.PersonList.as_view(), name='latest'),
    url(r'^personcreate/$', views.PersonCreate, name='personcreate'),
    url(r'^(?P<person_id>[0-9]+)/demofree/$', views.Demographics_free, name='demographics-free'),
    url(r'^(?P<person_id>[0-9]+)/demochoice/$', views.Demographics_choice, name='demographics-choice'),
    url(r'^(?P<person_id>[0-9]+)/demomix/$', views.Demographics_mix, name='demographics-mix'),
    url(r'^(?P<person_id>[0-9]+)/netfree/$', views.Network_free, name='network-free'),
    url(r'^(?P<person_id>[0-9]+)/netchoice/$', views.Network_choice, name='network-choice'),
    url(r'^(?P<person_id>[0-9]+)/netmix/$', views.Network_mix, name='network-mix'),
    url(r'^(?P<person_id>[0-9]+)/workfree/$', views.Work_free, name='work-free'),
    url(r'^(?P<person_id>[0-9]+)/workchoice/$', views.Work_choice, name='work-choice'),
    url(r'^(?P<person_id>[0-9]+)/workmix/$', views.Work_mix, name='work-mix'),
    url(r'^(?P<person_id>[0-9]+)/skillsfree/$', views.Skills_free, name='skills-free'),
    url(r'^(?P<person_id>[0-9]+)/skillschoice/$', views.Skills_choice, name='skills-choice'),
    url(r'^(?P<person_id>[0-9]+)/skillsmix/$', views.Skills_mix, name='skills-mix'),
    url(r'^(?P<pk>[0-9]+)/personupdate/$', views.PersonUpdate, name='person-update'),
    url(r'^(?P<person_id>[0-9]+)/updatedemo/$', views.Update_demo, name='update-demo'),
    url(r'^(?P<person_id>[0-9]+)/updatenetwork/$', views.Update_network, name='update-network'),
    url(r'^(?P<person_id>[0-9]+)/updatework/$', views.Update_work, name='update-work'),
    url(r'^(?P<person_id>[0-9]+)/updateskills/$', views.Update_skills, name='update-skills'),
    url(r'^(?P<pk>[0-9]+)/persondelete/$', views.PersonDelete.as_view(), name='person-delete'),
    ]
