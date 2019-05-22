from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^add/notes/$',  addNotes, name='add'),
    url('^edit/notes/(\d+)/$',  editNotes, name='edit'),
    url('^view/user/agreements/$', viewAgreement, name='agreements')
 ]