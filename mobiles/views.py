import json
import random
import os
from django.conf import settings

from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db.models import Sum
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from .serializers import *
from .models import *
from django.contrib.humanize.templatetags import humanize

class JSONResponse(HttpResponse):
    """
    An HttpResponse class that render its data  content   into JSON
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def get_patient_profile(request):
    """
        Retrieve patient info
        :param request:
        :param pk:
        :return:
        """
    to_json = dict()

    if request.method == 'POST':
        data = json.loads(request.body)
        user_token = data['token']
        token_id = Token.objects.get(key=user_token)
        user_id = User.objects.get(pk=token_id.user_id)
        if not user_id.is_superuser:
            patient = PatientDemograph.objects.get(patient_id=user_id.username)
            if patient is not None:
                to_json['title'] = patient.title
                to_json['user_id'] = patient.patient_id
                to_json['fname'] = patient.fname
                to_json['mname'] = patient.mname
                to_json['lname'] = patient.lname
                to_json['phonenumber'] = patient.phonenumber
                to_json['foreign_number'] = patient.foreign_number
                to_json['email'] = patient.email
                to_json['legacy_patient_id'] = patient.legacy_patient_id
                to_json['date_of_birth'] = (patient.date_of_birth).strftime('%b %d %y')
                to_json['bloodgroup'] = patient.bloodgroup
                to_json['bloodtype'] = patient.bloodtype
                scheme = InsuranceSchemes.objects.get(id=patient.scheme_at_registration_id)
                to_json['scheme'] = scheme.scheme_name

                exists = os.path.isfile(
                    settings.PROFILE_PHOTOS_DIR + '/' + str(patient.patient_id).zfill(11) + '_profile.jpg')
                if exists:
                    to_json['pic'] = 'http://' + request.get_host() + '/img/profiles/' + str(patient.patient_id).zfill(
                        11) + '_profile.jpg'
                else:
                    to_json['pic'] = 'http://' + request.get_host() + '/img/profiles/' + patient.sex + '.jpg'
    return HttpResponse(json.dumps(to_json))


@csrf_exempt
def get_doctors(request):
    try:
        doctors = StaffDirectory.objects.filter(profession='Doctor', status='ACTIVE')
    except StaffDirectory.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = DoctorsSerializer(doctors, many=True)
        response = JSONResponse(serializer.data)

        return response


def get_a_doctor(request, pk):
    """
    Function that fetch only one doctor information
    :param request:
    :param pk:
    :return:
    """
    try:
        doctor = StaffDirectory.objects.get(staffid=pk)
    except StaffDirectory.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        parent_holder = []
        dr_sp = StaffSpecialization.objects.get(id=doctor.specialization_id)
        serializer = DoctorsSerializer(doctor)
        parent_holder.append(serializer.data)
        parent_holder.append(dr_sp.staff_type)
        response = JSONResponse(parent_holder)
        return response


def staff_specialization(request):
    """
    function returns the hospital staff specialization
    :param request:
    :return:
    """
    try:
        specialization = StaffSpecialization.objects.all()
    except StaffSpecialization.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        serializer = SpecializationSerializer(specialization, many=True)
        response = JSONResponse(serializer.data)
        return response


def get_drs_on_specialization(request, pk):
    """
    Funtion returns doctors that has the specialization id
    :param request:
    :param pk:
    :return:
    """
    try:
        dr_sp = StaffDirectory.objects.filter(specialization_id=pk)
    except StaffDirectory.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        serializer = DoctorsSerializer(dr_sp, many=True)
        response = JSONResponse(serializer.data)
        return response


@csrf_exempt
def get_inbox_messages(request):
    parent_json = []
    if request.method == "POST":
        data = json.loads(request.body)
        token = data['token']
        aut_token = Token.objects.get(key=token)
        if aut_token is not None:
            user = User.objects.get(id=aut_token.user_id)
            inbox = Message.objects.inbox_for(user)
            for x in inbox:
                to_json = dict()
                to_json['id'] = x.id
                to_json["sender"] = x.sender.last_name
                to_json["subject"] = x.subject
                to_json["body"] = x.body
                to_json["sent_at"] = (x.sent_at).strftime('%d/%m/%y')
                if str(x.read_at) != 'None':
                    color = '#898989'
                    font_style1 = ''
                    font_style2 = ''
                    icon = 'ion-android-drafts'
                else:
                    color = ''
                    font_style1 = 'ex1'
                    font_style2 = 'ex2'
                    icon = 'ion-email-unread'
                to_json["color"] = color
                to_json['font_style1'] = font_style1
                to_json['font_style2'] = font_style2
                to_json['icon'] = icon
                parent_json.append(to_json)
    return HttpResponse(json.dumps(parent_json))


@csrf_exempt
def get_inbox_messages_by_dates(request):
    parent_json = []
    if request.method == "POST":
        data = json.loads(request.body)
        token = data['token']
        start = data['start_date']
        end = data['end_date']
        aut_token = Token.objects.get(key=token)
        if aut_token is not None:
            user = User.objects.get(id=aut_token.user_id)
            inbox = Message.objects.inbox_for(user).filter(sent_at__range=(start, end))
            for x in inbox:
                to_json = dict()
                to_json['id'] = x.id
                to_json["sender"] = x.sender.last_name
                to_json["subject"] = x.subject
                to_json["body"] = x.body
                to_json["sent_at"] = (x.sent_at).strftime('%b %d, %y')
                if str(x.read_at) != 'None':
                    color = '#898989'
                    font_style1 = ''
                    font_style2 = ''
                    icon = 'icon ion-android-drafts'
                else:
                    color = ''
                    font_style1 = 'ex1'
                    font_style2 = 'ex2'
                    icon = 'icon ion-email-unread'
                to_json["color"] = color
                to_json['font_style1'] = font_style1
                to_json['font_style2'] = font_style2
                to_json['icon'] = icon
                parent_json.append(to_json)
    return HttpResponse(json.dumps(parent_json))


@csrf_exempt
def get_number_unread_messages(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_token = data['token']
        token_id = Token.objects.get(key=user_token)
        user = User.objects.get(pk=token_id.user_id)
        to_json = dict()
        if user:
            unread = Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()
            to_json['unread_count'] = unread
    return HttpResponse(json.dumps(to_json))



@csrf_exempt
def delete_inbox_message(request):
    """
    function which deletes/changes message status so that patient will not see it again
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        pk = data['id']
        now = timezone.now()
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            to_json = dict()
            obj = Message.objects.filter(pk=pk).update(recipient_deleted_at=now)
            if obj:
                to_json['status'] = 'success'
            else:
                to_json['status'] = 'error'
    return HttpResponse(json.dumps(to_json))


@csrf_exempt
def mark_as_read_message(request):
    now = timezone.now()
    to_json = dict()
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data['token']
        pk = data['id']
        token_id = Token.objects.get(key=token)
        user = User.objects.get(pk=token_id.user_id)
        if user is not None:
            Message.objects.filter(pk=pk).update(read_at=now)
            get_msg_ = Message.objects.get(pk=pk)
            to_json['id'] = get_msg_.id
            to_json['sender'] = get_msg_.sender.last_name
            to_json['subject'] = get_msg_.subject
            to_json['body'] = get_msg_.body
            to_json['send_at'] = get_msg_.sent_at.strftime('%d, %b %Y')
    return HttpResponse(json.dumps(to_json))


def save_message_from_medicplus(request):
    data = {}
    now = timezone.now()
    if request.method == 'POST':
        data = json.load(request.body)
        if data != '' and data != None:
            sender = data['sender_id']
            subject = data['subject']
            recipient = data['recipient']
            message = data['message']
            obj = Message.objects.create(sender_id=sender, subject=subject, recipient_id=recipient, body=message,
                                         sent_at=now)
            if obj:
                sender_ = User.objects.get(pk=recipient)
                recipient_ = User.objects.get(pk=recipient)
                send_mail('Mail Notification:', "You have a new message on your %s Inbox" % "Clinic Name",
                          sender_.email, [recipient_.email])

                return HttpResponse('Success')


@csrf_exempt
def sign_out(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = data['token']
        aut_token = Token.objects.get(key=token)
        if aut_token is not None:
            logout(request)
    return HttpResponse(json.dumps(True))


@csrf_exempt
def userLogin(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        message = dict()
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            token_id = Token.objects.get(user_id=request.user.id)
            message['token'] = token_id.key
            message['status'] = "success"
        else:
            message['status'] = 'error'
            message[
                'details'] = 'Invalid user credentials: Please verify you have access to the portal from your clinic'
        return HttpResponse(json.dumps(message))


@csrf_exempt
def message_from_patient(request):
    """
    save the message from  the patient
    :param request:
    :return:
    """
    now = timezone.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        if data != '' and data is not None:
            recipient = data['recipient']
            subject = data['subject']
            message_ = data['message']
            token_id = data['token']
            user_token = Token.objects.get(key=token_id)
            sender = User.objects.get(pk=user_token.user_id)
            save_obj = Message.objects.create(sender=sender, recipient=User.objects.get(username=recipient),
                                              subject=subject,
                                              body=message_,
                                              sent_at=now)
            if save_obj:
                message = "success"
            else:
                message = "message failed"

        else:
            message = "empty message sent"

        return HttpResponse(message)
    return HttpResponse('bad thing')


@csrf_exempt
def get_patient_documents(request):
    doc_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            pat_doc = PatientAttachment.objects.filter(patient_id=user.username).order_by('-id')
            for x in pat_doc:
                to_json = dict()
                cat_ob = AttachmentCategory.objects.filter(id=x.category_id)
                for a in cat_ob:
                    to_json['category_name'] = a.name
                to_json['id'] = x.id
                to_json['name'] = x.note
                to_json['date_add'] = (x.date_added).strftime('%d, %b %Y')
                to_json['attach'] = x.document_url
                if x.document_url != '':
                    to_json['attach_icon'] = 'ion-android-attach'
                else:
                    to_json['attach_icon'] = ''
                doc_holder.append(to_json)
    return HttpResponse(json.dumps(doc_holder))


@csrf_exempt
def get_doc_by_dates(request):
    doc_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        start = data['start_date']
        end = data['end_date']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            pat_doc = PatientAttachment.objects.filter(patient_id=user.username,
                                                       date_added__range=(start, end)).order_by('-id')
            for x in pat_doc:
                to_json = dict()
                cat_ob = AttachmentCategory.objects.filter(id=x.category_id)
                for a in cat_ob:
                    to_json['category_name'] = a.name
                to_json['id'] = x.id
                to_json['name'] = x.note
                to_json['date_add'] = (x.date_added).strftime('%d, %b %Y')
                to_json['attach'] = x.document_url
                if x.document_url != '':
                    to_json['attach_icon'] = 'ion-android-attach'
                else:
                    to_json['attach_icon'] = ''
                doc_holder.append(to_json)
    return HttpResponse(json.dumps(doc_holder))


def download_attachment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        doc_id = data['id']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            file_dir = PatientAttachment.objects.get(id=doc_id)
            filename = file_dir.document_url
            obj = dict()
            # obj['url'] = 'http://192.168.1.52:81%s' % filename
            obj['status'] = 'success'
    return HttpResponse(json.dumps(obj))


@csrf_exempt
def get_patient_bills(request):
    """
    get the all bills relating to patients
    :param request:
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(id=token.user_id)
        bills = Bills.objects.filter(patient_id=user.username, billed_to__pay_type='self', cancelled_on=None).order_by(
            '-bill_id')
        for x in bills:
            to_json = dict()
            to_json['description'] = x.description
            to_json['transaction_date'] = x.transaction_date.strftime('%d, %b %Y')
            to_json['transaction_type'] = x.transaction_type
            to_json['price_type'] = x.price_type
            to_json['billed_to'] = "Self"
            to_json['amount'] = str(abs(x.amount))
            parent_holder.append(to_json)
    return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_patient_bills_date_range(request):
    """
    returns the results of patients bills
    between the requested date range
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        start = data['start_date']
        end = data['end_date']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        bills = Bills.objects.filter(patient_id=user.username, billed_to__pay_type='self', cancelled_on=None,
                                     transaction_date__range=(start, end)).order_by('-bill_id')
        if bills:
            for x in bills:
                to_json = dict()
                to_json['start_date'] = str(start)
                to_json['end_date'] = str(end)
                to_json['description'] = x.description
                to_json['transaction_date'] = x.transaction_date.strftime('%d, %b %Y')
                to_json['transaction_type'] = x.transaction_type
                to_json['price_type'] = x.price_type
                to_json['billed_to'] = "Self"
                to_json['amount'] = str(abs(x.amount))
                parent_holder.append(to_json)
    return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_patient_insured_bill_date_range(request):
    """
    returns the results of patients bills
    between the requested date range
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        start = data['start_date']
        end = data['end_date']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        bills = Bills.objects.filter(patient_id=user.username, billed_to__pay_type='insurance', cancelled_on=None,
                                     transaction_date__range=(start, end)).order_by('-bill_id')
        if bills:
            for x in bills:
                to_json = dict()
                to_json['start_date'] = str(start)
                to_json['end_date'] = str(end)
                to_json['description'] = x.description
                to_json['transaction_type'] = x.transaction_type
                to_json['transaction_date'] = x.transaction_date.strftime('%d, %b %Y')
                to_json['price_type'] = x.price_type
                to_json['billed_to'] = x.billed_to.scheme_name
                to_json['amount'] = str(abs(x.amount))
                parent_holder.append(to_json)
    return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_patient_insurance_bills(request):
    """
    return the patient insurance bills
    :param request:
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(id=token.user_id)
        bill = Bills.objects.filter(patient_id=user.username, billed_to__pay_type='insurance',
                                    cancelled_on=None).order_by(
            '-bill_id')
        if bill:
            for x in bill:
                to_json = dict()
                to_json['description'] = x.description
                to_json['transaction_date'] = x.transaction_date.strftime('%d, %b %Y')
                to_json['transaction_type'] = x.transaction_type
                to_json['price_type'] = x.price_type
                to_json['amount'] = str(abs(x.amount))
                to_json['billed_to'] = x.billed_to.scheme_name
                parent_holder.append(to_json)

    return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_patient_outstanding_balance(request):
    """
    return the patient outstanding balance
    :param request:
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(id=token.user_id)
        bill = Bills.objects.filter(patient_id=user.username, billed_to__pay_type='self', cancelled_on=None).aggregate(
            Sum('amount')).get(
            'amount__sum', 0.00)
        to_json = dict()
        to_json['bill'] = str(abs(bill))
        if bill > 0:
            color = '#fff'
        elif bill < 0:
            color = '#ef473a'
        else:
            color = '#fff'
        to_json['color'] = color
        parent_holder.append(to_json)
        return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_insurance_outstanding_balance(request):
    """
    return the patient outstanding balance
    :param request:
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(id=token.user_id)
        bill = Bills.objects.filter(patient_id=user.username, billed_to__pay_type='insurance',
                                    cancelled_on=None).aggregate(Sum('amount')).get(
            'amount__sum', 0.00)
        to_json = dict()
        to_json['bill'] = str(abs(bill))
        if bill > 0:
            color = '#fff'
        elif bill < 0:
            color = '#ef473a'
        else:
            color = '#fff'
        to_json['color'] = color
        parent_holder.append(to_json)
        return HttpResponse(json.dumps(parent_holder))



@csrf_exempt
def get_patient_appointment(request):
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            app_grp = AppointmentGroup.objects.filter(patient_id=user.username).order_by('-id')
            if app_grp:
                for x in app_grp:
                    to_json = dict()
                    if x.department_id is not None:
                        dept = Departments.objects.get(id=x.department_id)
                        to_json['department'] = dept.name
                    app_invitee = AppointmentInvitee.objects.filter(group_id=x.id)
                    if app_invitee:
                        for a in app_invitee:
                            staff = StaffDirectory.objects.get(staffid=a.staff_id)
                            to_json['invitee'] = str(staff.firstname + ", " + staff.lastname)
                    clinic = AppointmentClinic.objects.get(id=x.clinic_id)
                    to_json['clinic'] = clinic.name
                    to_json['type'] = x.type
                    app_ob = Appointment.objects.filter(group_id=x.id, status='SCHEDULED')
                    for y in app_ob:
                        to_json['start_time'] = humanize.naturaltime(y.start_time)
                        parent_holder.append(to_json)
    return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_patient_appointment_by_dates(request):
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        start = data['start_date']
        end = data['end_date']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            app_grp = AppointmentGroup.objects.filter(patient_id=user.username).order_by('-id')
            if app_grp:
                for x in app_grp:
                    to_json = dict()
                    if x.department_id is not None:
                        dept = Departments.objects.get(id=x.department_id)
                        to_json['department'] = dept.name
                    app_invitee = AppointmentInvitee.objects.filter(group_id=x.id)
                    if app_invitee:
                        for a in app_invitee:
                            staff = StaffDirectory.objects.get(staffid=a.staff_id)
                            to_json['invitee'] = str(staff.firstname + ", " + staff.lastname)
                    clinic = AppointmentClinic.objects.get(id=x.clinic_id)
                    to_json['clinic'] = clinic.name
                    to_json['type'] = x.type
                    app_ob = Appointment.objects.filter(group_id=x.id, status='SCHEDULED',
                                                        start_time__range=(start, end))
                    for y in app_ob:
                        to_json['start_time'] = y.start_time.strftime('%d, %b %Y, %H:%M %p')
                        parent_holder.append(to_json)
    return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_patient_labs(request):
    """
    return patient lab info
    :param request:
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            lab_re = LabRequests.objects.filter(patient_id=user.username)
            if lab_re:
                for l in lab_re:
                    to_json = dict()
                    labs = PatientLabs.objects.filter(patient_id=l.patient_id, field_status='open', ).order_by('-id')
                    if labs:

                        to_json['request_date'] = l.time_entered.strftime('%d, %b %Y')
                        for x in labs:
                            if x.test_specimen_ids is not None and x.test_specimen_ids is not '':
                                specimen = LabSpecimen.objects.filter(id__in=x.test_specimen_ids.split(','))
                                if specimen:
                                    specs = []
                                    for spec in specimen:
                                        specs.append(spec.name)
                                    to_json['specimen'] = specs
                            lab_t = LabtestsConfig.objects.get(id=x.test_id)
                            to_json['lab_test'] = lab_t.name
                            to_json['lab_id'] = x.id
                            l_r_s = LabResult.objects.filter(patient_lab=x.id, approved=1)
                            lent = len(l_r_s)
                            if lent is not 0:
                                to_json['lab_status'] = 'Ready'
                            else:
                                to_json['lab_status'] = 'Pending'
                        parent_holder.append(to_json)
    return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_patient_labs_by_range(request):
    """
    return patient lab infos
    :param request:
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        start = data['start_date']
        end = data['end_date']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            lab_re = LabRequests.objects.filter(patient_id=user.username, time_entered__range=(start, end))
            if lab_re:
                for l in lab_re:
                    to_json = dict()
                    labs = PatientLabs.objects.filter(patient_id=l.patient_id, field_status='open', ).order_by('-id')
                    if labs:
                        to_json['id'] = l.id
                        to_json['request_date'] = l.time_entered.strftime('%d, %b %Y')
                        for x in labs:
                            if x.test_specimen_ids is not None and x.test_specimen_ids is not '':
                                specimen = LabSpecimen.objects.filter(id__in=x.test_specimen_ids.split(','))
                                if specimen:
                                    specs = []
                                    for spec in specimen:
                                        specs.append(spec.name)
                                    to_json['specimen'] = specs
                            lab_t = LabtestsConfig.objects.get(id=x.test_id)
                            to_json['lab_test'] = lab_t.name
                            l_r_s = LabResult.objects.filter(patient_lab=x.id, approved=1)
                            lent = len(l_r_s)
                            if lent is not 0:
                                to_json['lab_status'] = 'Ready'
                            else:
                                to_json['lab_status'] = 'Pending'
                        parent_holder.append(to_json)
    return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_patient_lab_result(request):
    """
    return the patient requested result
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        lab_id = data['lab_id']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            p_lab = PatientLabs.objects.get(pk=lab_id)
            test = dict()
            if p_lab:
                hospital = dict()
                lab_test = LabtestsConfig.objects.get(id=p_lab.test_id)
                clinic = Clinic.objects.get(clinicid=lab_test.hospid)
                hospital['name'] = clinic.name
                hospital['address'] = clinic.address
                hospital['phone'] = clinic.phone_no
                test['hospital'] = hospital

                test['test'] = lab_test.name
                spec = LabSpecimen.objects.filter(id=p_lab.test_specimen_ids)
                if spec:
                    specs = []
                    for sp in spec:
                        specs.append(sp.name)
                    test['specimen'] = specs
                lab_r = LabResult.objects.filter(patient_lab=p_lab.id, approved=1)
                if lab_r:
                    result = []
                    for x in lab_r:
                        lab_data = LabResultData.objects.filter(lab_result=x.id)
                        if lab_data:
                            for lab in lab_data:
                                result_data = dict()
                                result_data['value'] = lab.value
                                result_data['template_label'] = lab.lab_template_data.label
                                result.append(result_data)
                    test['result'] = result
                    response = (json.dumps(test))
                else:
                    response = 'error'
        return HttpResponse(response)


@csrf_exempt
def get_patient_allergies(request):
    """
    This method returns the patient allergies if exists
    :param request:
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            p_allergy = PatientAllergen.objects.filter(patient_id=user.username).order_by('-id')
            for x in p_allergy:
                to_json = dict()
                to_json['id'] = x.id
                to_json['allergen'] = x.allergen
                to_json['reaction'] = x.reaction
                to_json['severity'] = x.severity
                to_json['date_noted'] = x.date_noted.strftime('%d, %b %Y')
                responsible = StaffDirectory.objects.get(staffid=x.noted_by)
                to_json['firstname'] = responsible.firstname
                to_json['lastname'] = responsible.lastname
                to_json['profession'] = responsible.profession
                parent_holder.append(to_json)
        return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_patient_allergies_by_dates(request):
    """
    This method returns the patient allergies if exists
    :param request:
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        start = data['start_date']
        end = data['end_date']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            p_allergy = PatientAllergen.objects.filter(patient_id=user.username,
                                                       date_noted__range=(start, end)).order_by('-id')
            for x in p_allergy:
                to_json = dict()
                to_json['id'] = x.id
                to_json['allergen'] = x.allergen
                to_json['reaction'] = x.reaction
                to_json['severity'] = x.severity
                to_json['date_noted'] = x.date_noted.strftime('%d, %b %Y')
                responsible = StaffDirectory.objects.get(staffid=x.noted_by)
                to_json['firstname'] = responsible.firstname
                to_json['lastname'] = responsible.lastname
                to_json['profession'] = responsible.profession
                parent_holder.append(to_json)
        return HttpResponse(json.dumps(parent_holder))


def get_an_allergen(request, pk):
    """
    get the value for the patient clicked allergen
    :param request:
    :param pk:
    :return:
    """
    try:
        allergy = PatientAllergen.objects.get(pk=pk)

    except PatientAllergen.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        parent_holder = []
        if allergy:
            to_json = dict()
            to_json['allergen'] = allergy.allergen
            to_json['reaction'] = allergy.reaction
            to_json['severity'] = allergy.severity
            parent_holder.append(to_json)
            return HttpResponse(json.dumps(parent_holder))


def update_allergy_by_patient(request):
    """
    patient sends request to update a particular allergen here
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        patient = 22  # should be got from session
        data = json.loads(request.body)
        allergy_id = data['id']
        allergen = data['allergen']
        reaction = data['reaction']
        severity = data['severity']
        date_update = timezone.now()
        obj = dict()
        if allergen is not '' and allergy_id is not '' and reaction is not ' ' and severity is not '':
            try:
                pat = PatientAllergen.objects.filter(id=allergy_id).update(allergen=allergen, reaction=reaction,
                                                                           severity=severity, noted_by=patient,
                                                                           date_noted=date_update)
                if pat:
                    obj['status'] = 'success'
                else:
                    obj['status'] == 'error'
                return HttpResponse(json.dumps(obj))
            except PatientAllergen.DoesNotExist:
                return HttpResponse(status=404)


@csrf_exempt
def get_patient_active_medications(request):
    """
    this gets all the medication the patient is active on
    :param request:
    :return:
    """
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            pat_reg = PatientRegimens.objects.filter(patient_id=user.username).order_by('-id')
            for rgm in pat_reg:
                to_json = dict()
                to_json['when'] = rgm.when.strftime('%d, %b %Y')
                reg_data = PatientRegimensData.objects.filter(group_code=rgm.group_code, status='open',
                                                              cancelled_on=None)
                for rgd in reg_data:
                    to_json['id'] = rgd.id  # if the patient need to update the id can be used
                    to_json['dose'] = rgd.dose
                    to_json['duration'] = rgd.duration
                    to_json['frequency'] = rgd.frequency
                    to_json['comment'] = rgd.comment
                    request_by = StaffDirectory.objects.get(staffid__contains=rgd.requested_by)
                    to_json['profession'] = request_by.profession
                    to_json['responsible'] = request_by.firstname + ' '+ request_by.lastname
                    gen = DrugGenerics.objects.filter(id=rgd.drug_generic_id)
                    if gen:
                        for g in gen:
                            to_json['generic'] = g.name
                            drug = Drugs.objects.filter(id=rgd.drug_id)
                            if drug:
                                for x in drug:
                                    to_json['drug'] = x.name
                            parent_holder.append(to_json)
        return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_active_medications_by_dates(request):
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        start = data['start_date']
        end = data['end_date']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            pat_reg = PatientRegimens.objects.filter(patient_id=user.username, when__range=(start, end)).order_by('-id')
            for rgm in pat_reg:
                to_json = dict()
                to_json['when'] = rgm.when.strftime('%d, %b %Y')
                reg_data = PatientRegimensData.objects.filter(group_code=rgm.group_code, status='open',
                                                              cancelled_on=None, refillable=0)
                for rgd in reg_data:
                    to_json['id'] = rgd.id  # if the patient need to update the id can be used
                    to_json['dose'] = rgd.dose
                    to_json['duration'] = rgd.duration
                    to_json['frequency'] = rgd.frequency
                    to_json['comment'] = rgd.comment
                    request_by = StaffDirectory.objects.get(staffid__contains=rgd.requested_by)
                    to_json['profession'] = request_by.profession
                    to_json['responsible'] = request_by.firstname + ' ' + request_by.lastname
                    gen = DrugGenerics.objects.filter(id=rgd.drug_generic_id)
                    if gen:
                        for g in gen:
                            to_json['generic'] = g.name
                            # drug = Drugs.objects.filter(id=rgd.drug_id)
                            # if drug:
                            #     for x in drug:
                            #         to_json['drug'] = x.name
                            parent_holder.append(to_json)
        return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_refillables(request):
    parent_holder = []
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        if user is not None:
            pat_reg = PatientRegimens.objects.filter(patient_id=user.username).order_by('-id')
            for rgm in pat_reg:
                to_json = dict()
                to_json['when'] = rgm.when.strftime('%d, %b %Y')
                reg_data = PatientRegimensData.objects.filter(group_code=rgm.group_code, status='open',
                                                              cancelled_on=None, refillable=1)

                for rgd in reg_data:
                    to_json['id'] = rgd.id  # if the patient need to update the id can be used
                    to_json['dose'] = rgd.dose
                    to_json['duration'] = rgd.duration
                    to_json['refill_number'] = ''  # sync with d latest database
                    to_json['frequency'] = rgd.frequency
                    to_json['comment'] = rgd.comment
                    request_by = StaffDirectory.objects.get(staffid__contains=rgd.requested_by)
                    to_json['profession'] = request_by.profession
                    to_json['firstname'] = request_by.firstname
                    to_json['lastname'] = request_by.lastname
                    gen = DrugGenerics.objects.filter(id=rgd.drug_generic_id)
                    if gen:
                        for g in gen:
                            to_json['generic'] = g.name
                    parent_holder.append(to_json)
        return HttpResponse(json.dumps(parent_holder))


@csrf_exempt
def get_medic_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        pre_id = data['id']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(id=token.user_id)
        if user is not None:
            to_json = dict()
            rgd = PatientRegimensData.objects.get(id=pre_id)
            patient = PatientDemograph.objects.get(patient_id=user.username)
            to_json['patient_name'] = patient.title + ' ' + patient.fname + ' ' + patient.mname + ' ' + patient.lname
            to_json['sex'] = patient.sex
            to_json['dose'] = rgd.dose
            to_json['duration'] = rgd.duration
            to_json['frequency'] = rgd.frequency
            to_json['comment'] = rgd.comment
            # to_json['refil_date'] = rgd.refill_date.strftime('%d, %b %Y')
            to_json['refill_number'] = rgd.refill_number
            request_staf = StaffDirectory.objects.get(staffid__contains=rgd.requested_by)
            if request_staf:
                dr_sp = StaffSpecialization.objects.get(id=request_staf.specialization_id)
                to_json['specialty'] = dr_sp.staff_type
                to_json['responsible'] = request_staf.firstname + ' ' + request_staf.lastname
                to_json['profession'] = request_staf.profession
            else:
                gen = DrugGenerics.objects.filter(id=rgd.drug_generic_id)
            if gen:
                for g in gen:
                    to_json['generic'] = g.name
                    drug = Drugs.objects.filter(id=rgd.drug_id)
                    if drug:
                        for x in drug:
                            to_json['drug'] = x.name

        return HttpResponse(json.dumps(to_json))


@csrf_exempt
def get_allergen_count(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user = User.objects.get(pk=token.user_id)
        to_json = dict()
        if user:
            allergen_count = PatientAllergen.objects.filter(patient_id=user.username).count()
            patient = PatientDemograph.objects.get(patient_id=user.username)
            to_json['allergyCount'] = allergen_count
            to_json['pa_name'] = patient.fname + ' ' + patient.mname + ' ' + patient.lname
    return HttpResponse(json.dumps(to_json))


@csrf_exempt
def get_open_medication_count(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token = Token.objects.get(key=token_id)
        user  = User.objects.get(pk=token.user_id)
        regim = PatientRegimens.objects.filter(patient_id=user.username)
        to_json = dict()
        for reg in regim:
            medic_count = PatientRegimensData.objects.filter(group_code=reg.group_code, status='open', cancelled_on=None).count()
            to_json['medic_count'] = medic_count
    return HttpResponse(json.dumps(to_json))


def generate_Password():
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    output = []
    chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
    for x in xrange(0, 4):
        output.append(str(nums[random.randint(0, len(nums) - 1)]))

    for x in xrange(0, 3):
        output.append(str(chars[random.randint(0, len(chars) - 1)]))
    return ''.join(output)


def create_patient_user(request):
    """
    this function automatically gets all the registered patients
    and create user name and password for each on exection of this
    function
    :param request:
    :return:
    """
    p_w_d = generate_Password()
    if request.method == 'GET':
        patients = PatientDemograph.objects.all()
        for p in patients:
            user = User.objects.create(username=p.patient_id, email=p.email, password=p_w_d, first_name=p_w_d, is_staff=False,
                                              last_name=str(p.fname + " " + p.lname))
            user.set_password(p_w_d)
            user.save()

    return HttpResponse("yes done")


@csrf_exempt
def patient_change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token_id = data['token']
        token_id = data['new_password']
        token = Token.objects.get(key=token_id)
        if token is not None:
            user_ob = User.objects.filter()
