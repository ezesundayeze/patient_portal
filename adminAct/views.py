# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from .form import *
from time import gmtime, strftime


# Create your views here.

@csrf_exempt
def addNotes(request):
    m_type = message = None
    created_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    form_obj = UserAgreementForm()
    if request.method == 'POST':
        form = UserAgreementForm(request.POST)
        if form.is_valid():
            # check is if any exists an active
            agree_obj = UserAgreement.objects.filter(active=True)
            if agree_obj:
                m_type = 'error'
                message = 'You have an active existing patient agreement'
            else:
                obj = form.save(commit=False)
                obj.created_on = created_date
                obj.save()
        else:
            m_type = 'error'
            message = "error occurred!"
            form_obj = UserAgreementForm()
    return render_to_response('addNotes.html', {'form': form_obj, 'm_type': m_type, 'message': message},
                              RequestContext(request))


@csrf_exempt
def editNotes(request, param):
    m_type = message = None
    created_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if param:
        id = UserAgreement.objects.get(pk=param)
    else:
        id = None
    if request.method == 'POST':
        form = UserAgreementForm(request.POST, instance=id)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_on = created_date
            obj.save()
            return HttpResponseRedirect('/adminAct/view/user/agreements/')
        else:
            m_type = 'error'
            message = "error occurred!"
    else:

        form = UserAgreementForm(instance=id)
    return render_to_response('addNotes.html', {'form': form, 'm_type': m_type, 'message': message},
                              RequestContext(request))


def viewAgreement(request):
    obj = UserAgreement.objects.all()
    return render_to_response('user_agreements.html', {'obj': obj}, RequestContext(request))
