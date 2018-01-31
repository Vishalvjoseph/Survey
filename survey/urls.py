from django.conf.urls import url
from . import views
from .forms import PersonForm, AnswerCenterForm, AnswerWorkerForm, AnswerEmployerForm
from survey.views import Index, PersonList, PersonCreate, PersonUpdate, PersonDelete, DetailCenter_create, Create_Center, DetailCenter_update, Update_Center, DetailWorker_create, Create_Worker, DetailWorker_update, Update_Worker, DetailEmployer_create, Create_Employer, DetailEmployer_update, Update_Employer   


app_name = 'survey'
urlpatterns = [
    url(r'^$', views.Index, name='index'),
    url(r'^latest/$', views.PersonList.as_view(), name='latest'),
    url(r'^personcreate/$', views.PersonCreate, name='personcreate'),  #view in which person objects are created
    url(r'^(?P<pk>[0-9]+)/personupdate/$', views.PersonUpdate, name='person-update'),#view in which person objects are updated
    url(r'^(?P<pk>[0-9]+)/persondelete/$', views.PersonDelete.as_view(), name='person-delete'),
    url(r'^(?P<person_id>[0-9]+)/detailcentercreate/$', views.DetailCenter_create, name='detail-center-create'),  #view which displays the various sections of the survey and redirects to Create view
    url(r'^(?P<person_id>[0-9]+)/(?P<start>[0-9]+)/(?P<finish>[0-9]+)/(?P<status>[0-9]+)/createcenter/$', views.Create_Center, name='create-center'),  #view in which answer objects are created
    url(r'^(?P<person_id>[0-9]+)/detailcenterupdate/$', views.DetailCenter_update, name='detail-center-update'),  #view which displays the various sections of the survey and redirects to Update view
    url(r'^(?P<person_id>[0-9]+)/(?P<start>[0-9]+)/(?P<finish>[0-9]+)/(?P<status>[0-9]+)/updatecenter/$', views.Update_Center, name='update-center'),   #view in which answer objects are updated
    url(r'^(?P<person_id>[0-9]+)/detailworkercreate/$', views.DetailWorker_create, name='detail-worker-create'),  #view which displays the various sections of the survey and redirects to Create view
    url(r'^(?P<person_id>[0-9]+)/(?P<start>[0-9]+)/(?P<finish>[0-9]+)/(?P<status>[0-9]+)/createworker/$', views.Create_Worker, name='create-worker'),  #view in which answer objects are created
    url(r'^(?P<person_id>[0-9]+)/detailworkerupdate/$', views.DetailWorker_update, name='detail-worker-update'),  #view which displays the various sections of the survey and redirects to Update view
    url(r'^(?P<person_id>[0-9]+)/(?P<start>[0-9]+)/(?P<finish>[0-9]+)/(?P<status>[0-9]+)/updateworker/$', views.Update_Worker, name='update-worker'),   #view in which answer objects are updated
    url(r'^(?P<person_id>[0-9]+)/detailemployercreate/$', views.DetailEmployer_create, name='detail-employer-create'),  #view which displays the various sections of the survey and redirects to Create view
    url(r'^(?P<person_id>[0-9]+)/(?P<start>[0-9]+)/(?P<finish>[0-9]+)/(?P<status>[0-9]+)/createemployer/$', views.Create_Employer, name='create-employer'),  #view in which answer objects are created
    url(r'^(?P<person_id>[0-9]+)/detailemployerupdate/$', views.DetailEmployer_update, name='detail-employer-update'),  #view which displays the various sections of the survey and redirects to Update view
    url(r'^(?P<person_id>[0-9]+)/(?P<start>[0-9]+)/(?P<finish>[0-9]+)/(?P<status>[0-9]+)/updateemployer/$', views.Update_Employer, name='update-employer'),   #view in which answer objects are updated
    ]
