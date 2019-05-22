from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^bills/$', bills, name='bills'),
    url('^filter/bills/$', filter_bills, name='filter_head'),
 ]