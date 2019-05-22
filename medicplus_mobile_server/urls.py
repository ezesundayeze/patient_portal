"""medicplus_mobile_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from portal import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  url(r'^mobile/', include('mobiles.urls')),

                  # for patient portal web.
                  url(r'^$', views.login_, name='login'),
                  url(r'^logout/$', views.logout_, name='logout'),
                  url('^home/$', views.home, name='home'),
                  url('^dashboard/$',  views.dashboard, name='dashboard'),
                  url('^change/pin/$', views.changePassword, name='changePwd'),
                  url('profiles/', include('profiles.urls')),
                  url('appointments/', include('appointments.urls')),
                  url('bills/', include('bills.urls')),
                  url('labs/', include('labs.urls')),
                  url('encounters/', include('encounters.urls')),
                  url('imaging/', include('scans.urls')),
                  url('adminAct/', include('adminAct.urls')),
                  url('test/printer/$', views.printer, name='test_printer'),
                  url(r'^patient/contact/$', views.contacts, name='contact'),
                  url(r'^registration/$', views.create_patient, name='register_me'),
                  url(r'^get/user/district/$', views.getStateDistrict, name='district'),
                  url(r'^get/user/lga/$', views.getStateLga, name='lgas'),
                  url(r'^country/dial/code/$', views.get_country_id, name='country_id'),

                  url(r'^create/patient/$', views.create_a_patient, name='new_patient'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
