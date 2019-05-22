# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mobiles.models import AppointmentGroup, AppointmentClinic, Appointment, FakeAppointment, PatientDemograph, User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime
import socket, os
# Create your views here.



@login_required()
def get_appointments(request):
    """
    :param request:
    :return: patient appointments
    """
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])
    appoints = AppointmentGroup.objects.raw(
        'SELECT ag.id, ag.type, ap.start_time, ap.end_time FROM appointment_group ag LEFT JOIN appointment ap ON ag.id=ap.group_id WHERE ag.patient_id=%s',
        [user.username]);
    exists = os.path.isfile(
        # settings.PROFILE_PHOTOS_DIR + '/' + str(user.username).zfill(11) + '_profile.jpg'
        '/var/www/html/medicplus/img/profiles/' + str(user.username).zfill(11) + '_profile.jpg'
    )
    if exists:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + str(user.username).zfill(
            11) + '_profile.jpg'
    else:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + obj.sex + '.jpg'
    return render_to_response('appointmets.html', {'appintments': appoints, 'patient': p_obj, 'pic':pic, 'user':user}, RequestContext(request))


@csrf_exempt
@login_required()
def book_appointments(request):
    """
    :param request:
    :return null
    """
    message = None
    user = User.objects.get(id=request.session['user_id'])
    clinics = AppointmentClinic.objects.all()
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])
    if request.method == 'POST':
        clinic = AppointmentClinic.objects.get(id=request.POST.get('clinic'))
        obj = AppointmentGroup.objects.filter(clinic_id=clinic.id)
        for c in obj:
            app = Appointment.objects.filter(group_id=c.id, start_time=request.POST.get('start_time'),
                                             end_time=request.POST.get('end_time'))
            if len(app) > 0 and app[0].status != 'Active' and app[0].status != 'Scheduled':
                print('the clinic is free for booking')

            else:
                message = 'This Clinic Has been booked within this time'
    return render_to_response('book-appointment.html', {'patient': p_obj, 'clinics': clinics, 'user':user, 'message': message},
                              RequestContext(request))


@login_required()
def booked_appointments(request):
    """
    :param request:
    :return null
    """
    user = User.objects.get(id=request.session['user_id'])
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])

    appoints = FakeAppointment.objects.filter(patient_id=user.username)
    return render_to_response('booked_appointment.html', {'patient': p_obj, 'appoints': appoints},
                              RequestContext(request))
