# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from mobiles.models import  PatientDemograph, User, Contact
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import datetime
from django.conf import settings


# Create your views here.


@login_required()
def get_patient_profile(request):
    """
    Return Patient profile
    :param request:
    :return:
    """
    import socket
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    profile = PatientDemograph.objects.raw(
        'SELECT p.*, n.country_name AS country, iy.name AS industry_name, st.name AS region, r.name AS relgion_name, isc.scheme_name As insurance_name, i.insurance_expiration AS ins_expire, i.policy_number, i.enrollee_number, it.name AS ins_type, kr.name AS relationship FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN state st ON p.state_id=st.id LEFT JOIN countries n ON p.nationality=n.id LEFT JOIN insurance i ON i.patient_id=p.patient_ID LEFT JOIN insurance_schemes isc ON i.insurance_scheme=isc.id LEFT JOIN religion r ON p.religion_id=r.id LEFT JOIN insurance_type it ON isc.insurance_type_id=it.id LEFT JOIN industry iy ON p.industry_id = iy.id LEFT JOIN kin_relation kr ON p.kin_relation_id = kr.id WHERE p.patient_id=%s', [user.username])
    contacts = Contact.objects.filter(patient=user.username)

    exists = os.path.isfile(
        # settings.PROFILE_PHOTOS_DIR + '/' + str(user.username).zfill(11) + '_profile.jpg'
        '/var/www/html/medicplus/img/profiles/' + str(user.username).zfill(11) + '_profile.jpg'
    )
    if exists:
        pic = 'http://' + socket.gethostname()+':81' + '/img/profiles/' + str(user.username).zfill(
            11) + '_profile.jpg'
    else:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + obj.sex + '.jpg'

    return render_to_response('profile.html', {'patient': profile, 'contacts':contacts, 'pic':pic, 'user':user}, RequestContext(request))

