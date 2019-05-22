# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.db import IntegrityError
from django.db.models import Sum

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt

from mobiles.models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json
from .form import *
from django.http import HttpResponse
import datetime, socket, os



@csrf_exempt
def login_(request):
    message = m_type = None
    if request.method == 'POST':
        if request.POST.get('username') != ''  and request.POST.get('password') != '':
                if User.objects.filter(username=request.POST.get('username')):
                        check_login = User.objects.get(username=request.POST.get('username'))  # To be reviewed
                        # if check_login.last_login != None and check_login.last_login != '':  # To be reviewed
                        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
                        if user is not None and user.is_active:
                            login(request, user)
                            request.session['user_id'] = user.id
                            return HttpResponseRedirect('/dashboard/', RequestContext(request))
                        else:
                            message = 'You are not active on this portal, please contact your health care center.'
                            m_type = 'error'
                    # else:
                    #message = "first"
                    # return HttpResponseRedirect('/change/pin/', RequestContext(request))
                else:
                    message = 'Invalid Username'
                    m_type = 'error'

        else:
            message = 'Username or password cannot be empty'
            m_type = 'error'

    return render_to_response('login2.html', {'message': message, 'm_type': m_type}, RequestContext(request))


@login_required()
def logout_(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def home(request):
    return render_to_response('home_cont.html', {}, RequestContext(request))


@login_required()
def dashboard(request):
    """
    Patient dash board
    :param request:
    :return:
    """
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])
    patient_bill = Bills.objects.filter(patient_id=user.username, billed_to__pay_type='self',
                                        cancelled_on=None).aggregate(
        Sum('amount')).get(
        'amount__sum', 0.00)
    insured_bill = Bills.objects.filter(patient_id=user.username, billed_to__pay_type='insurance',
                                        cancelled_on=None).aggregate(Sum('amount')).get(
        'amount__sum', 0.00)
    enc_c = get_encounter_count(user.username)
    admi_c = get_admission_count(user.username)

    # patient encounter
    encounter = Encounter.objects.raw(
        'SELECT d.name, e.id, e.start_date, s.staff_type, st.firstname, st.lastname From encounter e LEFT JOIN staff_specialization s ON e.specialization_id=s.id LEFT JOIN departments d ON d.id=e.department_id LEFT JOIN staff_directory st ON st.staffid=e.initiator_id WHERE e.patient_id= %s ORDER BY e.id DESC LIMIT 3',
        [user.username])
    labs = PatientLabs.objects.raw(
        'SELECT p.id, p.lab_group_id, p.test_date, p.performed_by from patient_labs p LEFT JOIN lab_result re ON p.id=re.patient_lab_id WHERE p.patient_id=%s AND re.approved=TRUE  ORDER BY p.id DESC LIMIT 3',
        [user.username])
    scans = PatientScan.objects.raw(
        'SELECT s.id, s.requestcode, s.approved_date, t.name FROM patient_scan s LEFT JOIN scan t ON s.scan_ids=t.id WHERE s.approved=TRUE AND s.cancelled=FALSE AND s.patient_id=%s ORDER BY s.id DESC LIMIT 3',
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
    return render_to_response('dashboard.html',
                              {'patient': p_obj, 'p_bill': patient_bill,
                               'ins_bill': insured_bill, 'encounter_c': enc_c, 'admi_c': admi_c,
                               'encounters': encounter, 'labs': labs, 'scans': scans, 'user':user, 'pic':pic}, RequestContext(request))

def printer(request):

    return render_to_response('bill_charts.html')


def get_encounter_count(pid):
    """
    :param request:
    :return:
    """
    obj = Encounter.objects.filter(patient_id=pid).count()
    return obj


def get_admission_count(pid):
    """
    :param pid:
    :return: number of times a patient has been admitted
    """
    obj = InPatient.objects.filter(patient_id=pid).count()
    return obj



@csrf_exempt
def create_a_patient(request):
    """
    This method is triggered from medicplus
    :param request, patient_id
    :return:
    """
    if request.method == 'OPTION':
        pass
    server_host = request.get_host()
    print(server_host)
    message = None
    p_w_d = generate_Password()
    print(request.POST)
    if request.method == 'POST':
        print("posting",request.POST.get('pid'))
        pid = request.POST.get('pid')
        if pid is not None:
            try:
                User.objects.get(username=pid)
            except (IntegrityError):
                return HttpResponse("error:Patient already exists!")
            except(Exception, User.DoesNotExist):
                obj = PatientDemograph.objects.get(patient_id=pid)
                user = User.objects.create(username=obj.patient_id, email=obj.email, password=p_w_d,
                                        first_name=p_w_d,
                                        is_staff=False,
                                        last_name=str(obj.fname + " " + obj.lname))
                patientName = obj.title + ' ' + obj.fname + ' ' + obj.mname + ' ' + obj.lname
                from_email = 'issoftdevp@gmail.com'
                user.set_password(p_w_d)
                user.save()
                update_p = PatientDemograph.objects.get(patient_id=pid)
                update_p.portal = "enabled"
                update_p.save()
                if user.email != '' and user.email is not None:
                    subject = 'Patient Portal Enabled'
                    message = "" 
                    html_content = '<html><body> <div>Hello %s, you have been enabled to use a portal for your health care information. <p> Your Login details:</p> <p> Username: %s </p> <p> password: %s. </p> You are advised to change your password as soon as possible through your portal. </div><a href="http://portal.medicplus.com.ng/change/pin/">Please Click here to confirm.</a></body></html>' % (patientName, user.username, p_w_d)
                    
                    mail =  send_mail(subject, message, from_email, [user.email], fail_silently=True, auth_user=None, auth_password=None, connection=None, html_message=html_content)
                

                message = ('success:' + str(obj.fname) + ', portal has been enabled successfully,\n Login into your email for confirmation.')

        else:
            message = ('error:Could not get the patient info')    

    return HttpResponse(message)


@csrf_exempt
def deactivate_a_patient(request):
    """
    call on the function disables the patient from accessing the portal
    :param request:
    :return:
    """
    message = None
    if request.method == 'POST':
        pid = request.POST.get('pid')
        if pid is not None:
            try:
                user = User.objects.get(username=pid)
                user.is_active = False
                user.save()
                message = 'Patient has been disabled from the portal'
            except User.DoesNotExist:
                message = 'Patient does not exist on the portal'
    return HttpResponse(message)


def generate_Password():
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    output = []
    chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
    for x in range(0, 4):
        output.append(str(nums[random.randint(0, len(nums) - 1)]))

    for x in range(0, 3):
        output.append(str(chars[random.randint(0, len(chars) - 1)]))
    return ''.join(output)


@csrf_exempt
def changePassword(request):
    message=mtype = None
    if request.method == 'POST':
       if request.POST.get('username') is not None:
           username = User.objects.filter(username=request.POST.get('username'))
           if username:
               users = User.objects.get(username=request.POST.get('username'))
               users.password = request.POST.get('password2')
               users.set_password(request.POST.get('password2'))
               users.save()
               message = 'Congrats, You have successfully changed your password'
               mtype = 'success'
               return HttpResponseRedirect(reverse('login'))
           else:
               message='Sorry, You are not yet enebled to use this application, please contact your health care provider'
               mtype = 'error'
    return render_to_response('change_pwd.html',  {'message':message, 'mtype':mtype}, RequestContext(request))


def contacts(request):
    return render_to_response('contact.html', {})


@csrf_exempt
def create_patient(request):
    register = True
    message = m_type = None
    form_c = FakeContactForm
    form_ = FakePatientForm()
    if request.method == 'POST' and request.is_ajax():
        form_ = FakePatientForm(request.POST)
        contact_lists = request.POST.getlist('patientContacts')
        print("patient contact list::",contact_lists)
        if contact_lists is not None and len(contact_lists[0]) > 0:
            titles = request.POST.getlist('title')
            title = filter(None, titles)
            titles_ = '|'.join(title)
            if form_.is_valid():
                fp = form_.save(commit=False)
                if request.POST.get('lga_id') is not None and request.POST.get('lga_id') != "":
                    fp.lga = Lga.objects.get(id=request.POST.get('lga_id'))
                if request.POST.get('district_id') is not None and request.POST.get('district_id') != "":
                    fp.district_id = request.POST.get('district_id')
                if request.POST.get('res_lga_id') is not None and request.POST.get('res_lga_id') != "":
                    fp.res_lga = Lga.objects.get(id=request.POST.get('res_lga_id'))
                if request.POST.get('res_dist_id') is not None and request.POST.get('res_dist_id') != "":
                    fp.res_dist_id = request.POST.get('res_dist_id')
                if request.POST.getlist('title') is not None and request.POST.getlist('title') != "":
                    fp.title = titles_
                fp.save()
                contact = json.loads(contact_lists[0])
                for x in contact:
                    country_id = Countries.objects.get(country_name=x['nation_id'])
                    if ('primary' in x):
                        primary = True
                    else:
                        primary = False
                    form_c = FakeContactForm(
                        {'nation': country_id.id, 'phone': x['patient_phones'], 'type': x['type'], 'primary': primary})
                    fc = form_c.save(commit=False)
                    fc.search_phone = x['patient_phones'][0]
                    fc.fake_patient = fp
                    fc.save()
                    message = "success"

        else:
            message = "error"
        return HttpResponse(message)

    return render_to_response('register.html', {'form': form_, 'register': register, 'form_c': form_c, 'message': message, 'm_type': m_type},
                              RequestContext(request))



def get_country_id(request):
    if request.is_ajax():
        param = request.GET['country']
        if param is not None and param != "":
            obj = Countries.objects.get(country_name=param)
            id = obj.id
            return HttpResponse(id)


def getStateDistrict(request):
    if request.is_ajax():
        param = request.GET['state_id']
        paren_holder = []
        if param is not None and param != "":
            # try:
            obj = District.objects.filter(state=State.objects.get(id=param))
            for x in obj:
                to_json = dict()
                to_json['text'] = x.name
                to_json['id'] = x.id
                paren_holder.append(to_json)
        return HttpResponse(json.dumps(paren_holder))


def getStateLga(request):
    if request.is_ajax():
        param = request.GET['state_id']
        paren_holder = []
        if param is not None and param != "":
            lga = Lga.objects.filter(state=State.objects.get(id=param))
            for y in lga:
                lga_json = dict()
                lga_json['id'] = y.id
                lga_json['text'] = y.name
                paren_holder.append(lga_json)

        return HttpResponse(json.dumps(paren_holder))
