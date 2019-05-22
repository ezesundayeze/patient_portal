# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mobiles.models import Bills, PatientDemograph, User, Claim
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime
import socket, os
# Create your views here.



@login_required()
def bills(request):
    """
    :param request:
    :returns bill heads in a chart format
    """
    now = datetime.datetime.now()
    start_date = '%s-01-01' % now.year
    end_date = '%s-%s-%s' % (now.year, now.month, now.day)
    filter_date_range = 'January %s To Date' % now.year
    total = 0
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    claims_obj = Claim.objects.raw('SELECT c.*, i.scheme_name FROM claim c LEFT JOIN insurance_schemes i ON c.scheme_id=i.id WHERE c.patient_id=%s  ORDER BY c.scheme_id', [user.username])
    bill_stmt = Bills.objects.raw(
        'SELECT b.*, b.bill_id AS id, ANY_VALUE(iic.type) AS type FROM bills b LEFT JOIN insurance_items_cost iic ON iic.item_code=b.item_code LEFT JOIN insurance_schemes ON insurance_schemes.id = b.billed_to WHERE patient_id = %s AND insurance_schemes.pay_type = "self" AND b.cancelled_by IS NULL AND b.transaction_type = "credit" AND (b.transaction_date BETWEEN %s AND %s)', [user.username, start_date, end_date])

    bill_stmt_cop = Bills.objects.raw(
        "SELECT b.*, b.bill_id AS id, ins.pay_type, ANY_VALUE(iic.type) AS type FROM bills b LEFT JOIN insurance_items_cost iic ON iic.item_code=b.item_code LEFT JOIN insurance_schemes ins ON ins.id = b.billed_to WHERE b.patient_id = %s AND b.billed_to > 1 AND b.cancelled_by IS NULL AND (b.transaction_date BETWEEN %s AND %s)", [user.username, start_date, end_date])

    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])

    bill_head = Bills.objects.raw(
        'SELECT b.bill_id, SUM(REPLACE(b.amount, ",", " ")) AS amount, s.name FROM bills b LEFT JOIN bills_source s ON b.bill_source_id=s.id WHERE b.patient_id= %s AND b.cancelled_on IS NULL AND b.transaction_type="credit" AND (b.transaction_date BETWEEN %s AND %s) GROUP By s.id DESC ', [user.username, start_date, end_date])

    bill_head_v = Bills.objects.raw(
        'SELECT b.bill_id, SUM(REPLACE(b.amount, ",", " ")) AS amount, s.name FROM bills b LEFT JOIN bills_source s ON b.bill_source_id=s.id WHERE b.patient_id= %s AND b.cancelled_on IS NULL AND b.transaction_type="credit" AND (b.transaction_date BETWEEN %s AND %s)', [user.username, start_date, end_date])

    bills_paid = Bills.objects.raw(
        'SELECT b.* FROM bills b WHERE b.cancelled_on IS NULL AND b.parent_id IS NULL AND b.transaction_type="debit" AND b.patient_id=%s  AND (b.transaction_date BETWEEN %s AND %s)', [user.username, start_date, end_date])
    for a in bill_head:
        total = total + a.amount

    exists = os.path.isfile(
        # settings.PROFILE_PHOTOS_DIR + '/' + str(user.username).zfill(11) + '_profile.jpg'
        '/var/www/html/medicplus/img/profiles/' + str(user.username).zfill(11) + '_profile.jpg'
    )
    if exists:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + str(user.username).zfill(
            11) + '_profile.jpg'
    else:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + obj.sex + '.jpg'
    return render_to_response('bills.html', {'bills': bills_paid, 'patient': p_obj, 'bill_head': bill_head,
                                             'bill_head_v': bill_head_v, 'total': total, 'statements': bill_stmt,
                                             'bill_stmt_cop': bill_stmt_cop, 'filter_date_range':filter_date_range, 'user':user, 'pic':pic, 'claims':claims_obj}, RequestContext(request))


@csrf_exempt
@login_required()
def filter_bills(request):
    """
    :param request:
    :return bills heads by dates
    """
    total = 0
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    if request.method == 'POST':
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        filter_date_range = '%s To %s' % (start_date, end_date)
        claims_obj = Claim.objects.raw('SELECT * FROM claim WHERE patient_id=%s ORDER BY scheme_id', [user.username])
        bill_head = Bills.objects.raw(
            'SELECT b.bill_id, SUM(REPLACE(b.amount, ",", " ")) AS amount, s.name FROM bills b LEFT JOIN bills_source s ON b.bill_source_id=s.id WHERE b.patient_id= %s AND b.cancelled_on IS NULL AND b.transaction_type="credit" AND (b.transaction_date BETWEEN %s AND %s) GROUP By s.id',
            [user.username, start_date, end_date])
        for a in bill_head:
            total = total + a.amount

        bill_head_v = Bills.objects.raw(
            'SELECT b.bill_id, SUM(REPLACE(b.amount, ",", " ")) AS amount, s.name FROM bills b LEFT JOIN bills_source s ON b.bill_source_id=s.id WHERE b.patient_id= %s AND b.cancelled_on IS NULL AND b.transaction_type="credit" AND (b.transaction_date BETWEEN %s AND %s)  GROUP By s.id',
            [user.username, start_date, end_date])

        bills_paid = Bills.objects.raw(
            'SELECT b.* FROM bills b WHERE b.cancelled_on IS NULL AND b.parent_id IS NULL AND b.transaction_type="credit" AND b.patient_id=%s AND (b.transaction_date BETWEEN %s AND %s) ORDER BY b.bill_id DESC',
            [user.username, start_date, end_date])

        p_obj = PatientDemograph.objects.raw(
            'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
            [user.username])

        bill_stmt = Bills.objects.raw(
            "SELECT b.*, b.bill_id AS id, ANY_VALUE(iic.type) AS type FROM bills b LEFT JOIN insurance_items_cost iic ON iic.item_code=b.item_code LEFT JOIN insurance_schemes ON insurance_schemes.id = b.billed_to WHERE patient_id = %s AND insurance_schemes.pay_type = 'self' AND b.cancelled_by IS NULL AND b.transaction_type = 'credit' AND (b.transaction_date BETWEEN %s AND %s)", [user.username, start_date, end_date])

        bill_stmt_cop = Bills.objects.raw(
            "SELECT b.*, b.bill_id AS id, ins.pay_type, ANY_VALUE(iic.type) AS type FROM bills b LEFT JOIN insurance_items_cost iic ON iic.item_code=b.item_code LEFT JOIN insurance_schemes ins ON ins.id = b.billed_to WHERE b.patient_id = %s AND ins.pay_type = 'insurance' AND b.cancelled_by IS NULL  AND (b.transaction_date BETWEEN %s AND %s)",
            [user.username, start_date, end_date])
        exists = os.path.isfile(
            # settings.PROFILE_PHOTOS_DIR + '/' + str(user.username).zfill(11) + '_profile.jpg'
            '/var/www/html/medicplus/img/profiles/' + str(user.username).zfill(11) + '_profile.jpg'
        )
        if exists:
            pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + str(user.username).zfill(
                11) + '_profile.jpg'
        else:
            pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + obj.sex + '.jpg'

        return render_to_response('bills.html',
                                  {'bills': bills_paid, 'patient': p_obj, 'bill_head': bill_head,
                                   'bill_head_v': bill_head_v, 'total': total,
                                   'statements': bill_stmt, 'bill_stmt_cop': bill_stmt_cop, 'start_date': start_date,
                                   'end_date': end_date, 'filter_date_range':filter_date_range, 'user':user, 'pic':pic, 'claims':claims_obj}, RequestContext(request))

