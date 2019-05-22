from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^patient/scans/$', get_scans, name='scans'),
    url('^view/scan/result/(\d+)/$', scan_result, name='scan_result'),
    url('^print/scan/result/(\d+)/$', print_scan_result, name='print_s_result'),
 ]