from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^patient/profile/$', get_patient_profile, name='profiles'),
]