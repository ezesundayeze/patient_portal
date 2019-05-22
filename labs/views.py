# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mobiles.models import PatientLabs, PatientDemograph, User, Clinic
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from utilities.robots import render_to_pdf
import datetime
import socket, os
# Create your views here.



@login_required()
def get_labs(request):
    """
    :param request:
    :return approved  patient lab results
    """
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])
    labs = PatientLabs.objects.raw(
        'SELECT p.id, p.lab_group_id, p.test_date, p.performed_by, lt.name from patient_labs p LEFT JOIN lab_result re ON p.id=re.patient_lab_id LEFT JOIN labtests_config lt ON p.test_id=lt.id WHERE p.patient_id=%s AND re.approved=TRUE ',
        [user.username])
    exists = os.path.isfile(
        # settings.PROFILE_PHOTOS_DIR + '/' + str(user.username).zfill(11) + '_profile.jpg'
        '/var/www/html/medicplus/img/profiles/' + str(user.username).zfill(11) + '_profile.jpg'
    )
    if exists:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + str(user.username).zfill(
            11) + '_profile.jpg'
    else:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + obj.sex + '.jpg'

    return render_to_response('labs.html', {'labs': labs, 'patient': p_obj, 'user':user, 'pic':pic})


@login_required()
def get_lab_result(request, param):
    param_ = int(param)
    """
    :param request:
    :param param:
    :return return patient demograph and lab result parameters
    """
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])
    patient_obj = PatientLabs.objects.raw(
        'SELECT pl.id, p.title, p.fname AS patient_fname, p.lname AS patient_lname, p.sex, p.email, p.phonenumber, p.patient_ID, ref.name AS referral_name, c.country_name, lr.lab_group_id, lc.name AS test_name, ins.scheme_name AS insurance_name, lr.time_entered AS request_date, lres.approved_date, st.profession, st.firstname, st.lastname, rc.name AS referral_company FROM patient_labs pl LEFT JOIN patient_demograph p ON pl.patient_id=p.patient_ID LEFT JOIN insurance_schemes ins ON p.scheme_at_registration_id=ins.id LEFT JOIN countries c ON p.nationality=c.id LEFT JOIN lab_requests lr ON pl.lab_group_id=lr.lab_group_id LEFT JOIN lab_result lres ON pl.id=lres.patient_lab_id LEFT JOIN staff_directory st ON lres.approved_by=st.staffId LEFT JOIN referral ref ON lr.referral_id=ref.id LEFT JOIN referral_company rc ON rc.id=ref.referral_company_id LEFT  JOIN labtests_config lc ON pl.test_id=lc.id  WHERE pl.id=%s',
        [param_])
    lab_specimen = PatientLabs.objects.raw(
        'SELECT pl.id, sp.* FROM patient_labs pl LEFT JOIN lab_specimen sp ON pl.test_specimen_ids=sp.id WHERE pl.id=%s',
        [param_])
    result_obj = PatientLabs.objects.raw(
        'SELECT rd.*, lt.* FROM patient_labs pl LEFT JOIN lab_result lr ON pl.id=lr.patient_lab_id LEFT JOIN lab_result_data rd ON rd.lab_result_id=lr.id LEFT JOIN lab_template_data lt ON lt.id=rd.lab_template_data_id WHERE pl.id=%s',
        [param_])
    exists = os.path.isfile(
        # settings.PROFILE_PHOTOS_DIR + '/' + str(user.username).zfill(11) + '_profile.jpg'
        '/var/www/html/medicplus/img/profiles/' + str(user.username).zfill(11) + '_profile.jpg'
    )
    if exists:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + str(user.username).zfill(
            11) + '_profile.jpg'
    else:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + obj.sex + '.jpg'
    return render_to_response('lab_result.html',
                              {'patient_obj': patient_obj, 'patient': p_obj, 'lab_specimen': lab_specimen,
                               'result_obj': result_obj, 'user':user, 'pic':pic}, RequestContext(request))


@login_required()
def print_lab_result(request, param):
    param_ = int(param)
    """
    :param request:
    :param param:
    :return return patient demograph and lab result parameters
    """
    hospital = Clinic.objects.get(clinicid=1)
    patient_obj = PatientLabs.objects.raw(
        'SELECT pl.id, p.title, p.fname AS patient_fname, p.lname AS patient_lname, p.sex, p.email, p.phonenumber, p.patient_ID, ref.name AS referral_name, c.country_name, lr.lab_group_id, lc.name AS test_name, ins.scheme_name AS insurance_name, lr.time_entered AS request_date, lres.approved_date, st.profession, st.firstname, st.lastname, rc.name AS referral_company FROM patient_labs pl LEFT JOIN patient_demograph p ON pl.patient_id=p.patient_ID LEFT JOIN insurance_schemes ins ON p.scheme_at_registration_id=ins.id LEFT JOIN countries c ON p.nationality=c.id LEFT JOIN lab_requests lr ON pl.lab_group_id=lr.lab_group_id LEFT JOIN lab_result lres ON pl.id=lres.patient_lab_id LEFT JOIN staff_directory st ON lres.approved_by=st.staffId LEFT JOIN referral ref ON lr.referral_id=ref.id LEFT JOIN referral_company rc ON rc.id=ref.referral_company_id LEFT  JOIN labtests_config lc ON pl.test_id=lc.id  WHERE pl.id=%s',
        [param_])

    lab_specimen = PatientLabs.objects.raw(
        'SELECT pl.id, sp.* FROM patient_labs pl LEFT JOIN lab_specimen sp ON pl.test_specimen_ids=sp.id WHERE pl.id=%s',
        [param_])
    result_obj = PatientLabs.objects.raw(
        'SELECT rd.*, lt.* FROM patient_labs pl LEFT JOIN lab_result lr ON pl.id=lr.patient_lab_id LEFT JOIN lab_result_data rd ON rd.lab_result_id=lr.id LEFT JOIN lab_template_data lt ON lt.id=rd.lab_template_data_id WHERE pl.id=%s',
        [param_])
    return render_to_pdf( 'print_lab_result.html',
        {'pagesize': 'A4', 'patient_obj': patient_obj, 'lab_specimen': lab_specimen,'result_obj': result_obj, 'hospital':hospital,})

