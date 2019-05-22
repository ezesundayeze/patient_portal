from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^patient/appointments/$', get_appointments, name='appointments'),
    url('^book/appointments/$',    book_appointments, name='book'),
    url('^booked/appointments/$', booked_appointments, name='booked'),
 ]