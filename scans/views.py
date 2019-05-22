# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import unicode_literals
from mobiles.models import PatientDemograph, User, PatientScan, Clinic
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from utilities.robots import render_to_pdf
import datetime, socket, os

from django.shortcuts import render

# Create your views here.



@login_required()
def get_scans(request):
    """
    :param request:
    :return all the patient's scans
    """
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])
    scans = PatientScan.objects.raw(
        'SELECT s.id, s.requestcode, s.approved_date, t.name FROM patient_scan s LEFT JOIN scan t ON s.scan_ids=t.id WHERE s.approved=TRUE AND s.cancelled=FALSE AND s.patient_id=%s ORDER BY s.id DESC ',
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
    return render_to_response('scan.html', {'scan': scans, 'patient': p_obj, 'user':user, 'pic':pic}, RequestContext(request))


@login_required()
def scan_result(request, param):
    param_ = int(param)
    """
    :param request: allow patient to view result
    :param param:
    :return patient imaging result
    """
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])
    patient_obj = PatientScan.objects.raw(
        'SELECT ps.id, ps.requestCode, ps.approved_date, ps.request_date, c.country_name, ins.scheme_name AS insurance_name, ref.name AS referral_name, staf.profession, staf.firstname, staf.lastname, rc.name AS referral_company, p.title, p.fname AS patient_fname, p.lname AS patient_lname, p.sex, p.email, p.phonenumber, p.patient_ID FROM patient_scan ps LEFT JOIN patient_demograph p ON ps.patient_id=p.patient_ID LEFT JOIN referral ref ON ref.id=ps.referral_id LEFT JOIN referral_company rc ON rc.id=ref.referral_company_id LEFT JOIN insurance_schemes ins ON p.scheme_at_registration_id=ins.id LEFT JOIN countries c ON p.nationality=c.id LEFT JOIN staff_directory staf ON ps.approved_by_id=staf.staffId WHERE ps.id=%s',
        [param_])

    scan_res = PatientScan.objects.raw(
        'SELECT  ps.* FROM patient_scan s LEFT JOIN scan t ON s.scan_ids=t.id LEFT JOIN patient_scan_notes ps ON ps.patient_scan_id=s.id WHERE s.id=%s',
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
    return render_to_response('scan_result.html',
                              {'patient_obj': patient_obj, 'scan_result': scan_res, 'patient': p_obj, 'user':user, 'pic':pic}, RequestContext(request))


@login_required()
def print_scan_result(request, param):
    param_ = int(param)
    """
    :param request:
    :param param:
    :return patient imaging result
    """
    hospital = Clinic.objects.get(clinicid=1)

    patient_obj = PatientScan.objects.raw(
        'SELECT ps.id, s.name AS scan_name,  ps.requestCode, ps.approved_date, ps.request_date, c.country_name, ins.scheme_name AS insurance_name, ref.name AS referral_name, staf.profession, staf.firstname, staf.lastname, rc.name AS referral_company, p.title, p.fname AS patient_fname, p.lname AS patient_lname, p.sex, p.email, p.phonenumber, p.patient_ID FROM patient_scan ps LEFT JOIN scan s ON ps.scan_ids=s.id LEFT JOIN patient_demograph p ON ps.patient_id=p.patient_ID LEFT JOIN referral ref ON ref.id=ps.referral_id LEFT JOIN referral_company rc ON rc.id=ref.referral_company_id LEFT JOIN insurance_schemes ins ON p.scheme_at_registration_id=ins.id LEFT JOIN countries c ON p.nationality=c.id LEFT JOIN staff_directory staf ON ps.approved_by_id=staf.staffId WHERE ps.id=%s',
        [param_])
    scan_res = PatientScan.objects.raw(
        'SELECT  ps.* FROM patient_scan s LEFT JOIN scan t ON s.scan_ids=t.id LEFT JOIN patient_scan_notes ps ON ps.patient_scan_id=s.id WHERE s.id=%s',
        [param_])
    return render_to_pdf('print-scan-result.html',
                         {'pagesize': 'A4', 'patient_obj': patient_obj, 'scan_result': scan_res, 'hospital':hospital})
