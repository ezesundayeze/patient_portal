from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^labs/$', get_labs, name='labs'),
    url('^view/lab/results/(\d+)/$', get_lab_result, name='lab_result'),
    url('^print/lab/results/(\d+)/$', print_lab_result, name='print_result'),
 ]