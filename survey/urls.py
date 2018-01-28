from django.conf.urls import url
from . import views
from .forms import AnswerForm, PersonForm
from survey.views import Create, Update, Detail_create, Detail_update, PersonDelete, PersonCreate, PersonUpdate, Index, PersonList


app_name = 'survey'
urlpatterns = [
    url(r'^$', views.Index, name='index'),
    url(r'^latest/$', views.PersonList.as_view(), name='latest'),
    url(r'^personcreate/$', views.PersonCreate, name='personcreate'),  #view in which person objects are created
    url(r'^(?P<person_id>[0-9]+)/detailcreate/$', views.Detail_create, name='detail-create'),  #view which displays the various sections of the survey and redirects to Create view
    url(r'^(?P<person_id>[0-9]+)/(?P<start>[0-9]+)/(?P<finish>[0-9]+)/(?P<status>[0-9]+)/create/$', views.Create, name='create'),  #view in which answer objects are created
    url(r'^(?P<pk>[0-9]+)/personupdate/$', views.PersonUpdate, name='person-update'),#view in which person objects are updated
    url(r'^(?P<person_id>[0-9]+)/detailupdate/$', views.Detail_update, name='detail-update'),  #view which displays the various sections of the survey and redirects to Update view
    url(r'^(?P<person_id>[0-9]+)/(?P<start>[0-9]+)/(?P<finish>[0-9]+)/(?P<status>[0-9]+)/update/$', views.Update, name='update'),   #view in which answer objects are updated
    url(r'^(?P<pk>[0-9]+)/persondelete/$', views.PersonDelete.as_view(), name='person-delete'),
    ]
