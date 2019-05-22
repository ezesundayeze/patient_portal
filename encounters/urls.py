from django.conf.urls import url
from .views import *


urlpatterns = [
    url('^patient/encounters/$', get_all_encounters, name='encounters'),
    url('^print/encounters/(\d+)/$', print_encounter, name='print_encounter'),
    url('^view/encounters/(\d+)/$', view_encounter, name='view_encounter'),
 ]