# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mobiles.models import PatientDemograph, User, Encounter, VitalSign, PatientVisitNotes, PatientAllergen, EncounterAddendum, Clinic
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime
import socket, os

from utilities.robots import render_to_pdf


@login_required()
def get_all_encounters(request):
    """
    :param request:
    :return all the patient's encounters
    """
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])
    encounters = Encounter.objects.raw(
        'SELECT d.name, e.id, e.start_date, s.staff_type, st.firstname, st.lastname From encounter e LEFT JOIN staff_specialization s ON e.specialization_id=s.id LEFT JOIN departments d ON d.id=e.department_id  LEFT JOIN staff_directory st ON st.staffid=e.initiator_id WHERE e.patient_id= %s ORDER BY e.id ASC ',
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
    return render_to_response('encounters.html', {'encounters': encounters, 'patient': p_obj, 'user':user, 'pic':pic}, RequestContext(request))


@login_required()
def view_encounter(request, id):
    """
     Patient encounter
    :param request:
    :param id:
    :return:
    """
    pic = None
    user = User.objects.get(id=request.session['user_id'])
    obj = PatientDemograph.objects.get(patient_id=user.username)
    p_obj = PatientDemograph.objects.raw(
        'SELECT p.*, d.name AS dist_name, i.scheme_name As insurance_name FROM patient_demograph p LEFT JOIN district d ON d.id=p.district_id LEFT JOIN insurance_schemes i ON i.id=p.scheme_at_registration_id WHERE p.patient_id=%s',
        [user.username])

    enc_obj = Encounter.objects.raw(
        'SELECT e.id, sf.firstname, sf.lastname, e.signed_on, e.start_date, d.name AS depart_name, s.staff_type AS staff_special_name FROM encounter e LEFT JOIN departments d ON e.department_id=d.id LEFT JOIN encounter_addendum ed ON ed.encounter_id=e.id LEFT JOIN staff_specialization s ON e.specialization_id=s.id LEFT JOIN staff_directory sf ON e.signed_by=sf.staffId WHERE e.id=%s',
        [id])

    vitals = VitalSign.objects.raw(
        'SELECT vs.id, v.name AS type_name, v.unit AS type_unit, UNIX_TIMESTAMP(vs.read_date)*1000 AS dDate FROM vital_sign vs LEFT JOIN vital v ON vs.type_id=v.id WHERE encounter_id=%s',
        [id])
    complain = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type IN ("s", "d")', [id])

    sys_review = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="v" ', [id])

    p_medic_history = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="t" ', [id])

    p_drug_history = PatientVisitNotes.objects.raw(
        'SELECT pr.id, pd.comment, dg.name AS gen_name, dg.weight as gen_weight, dg.form AS gen_form FROM patient_regimens pr LEFT JOIN patient_regimens_data pd ON pr.group_code=pd.group_code LEFT JOIN drug_generics dg ON pd.drug_generic_id=dg.id WHERE pr.encounter_id=%s',
        [id])

    allergies = PatientAllergen.objects.raw(
        'SELECT pa.id, pa.allergen, pa.severity, pa.reaction, ds.name AS drug_super_gen, ac.name AS category FROM patient_allergen pa LEFT JOIN allergen_category ac ON pa.category_id=ac.id LEFT JOIN drug_super_generic ds ON pa.drug_super_gen_id=ds.id  WHERE pa.encounter_id=%s AND pa.active IS TRUE',
        [id])

    family_history = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="hx" ', [id])
    physical_exam = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="x" ', [id])

    exam_notes = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="e" ', [id])

    diagnoses = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="a" ', [id])

    investigations = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="i" ', [id])

    plans = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="p" ', [id])

    medications = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="m" ', [id])

    addenda = EncounterAddendum.objects.raw(
        'SELECT ed.*, s.username FROM encounter_addendum ed LEFT JOIN staff_directory s ON ed.user_id=s.staffId WHERE encounter_id=%s',
        [id])
    exists = os.path.isfile(
        # settings.PROFILE_PHOTOS_DIR + '/' + str(user.username).zfill(11) + '_profile.jpg'
        '/var/www/html/medicplus/img/profiles/' + str(user.username).zfill(11) + '_profile.jpg'
    )
    if exists:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + str(user.username).zfill(
            11) + '_profile.jpg'
    else:
        pic = 'http://' + socket.gethostname() + ':81' + '/img/profiles/' + obj.sex + '.jpg'
    return render_to_response('view_encounter.html',
                              {'enc_obj': enc_obj, 'vitals': vitals, 'complain': complain, 'sys_review': sys_review,
                               'p_medic_history': p_medic_history, 'p_drug_history': p_drug_history,
                               'allergies': allergies, 'family_hist': family_history, 'physical_exam': physical_exam,
                               'exam_notes': exam_notes, 'diagnoses': diagnoses, 'investigations': investigations,
                               'plans': plans, 'medications': medications, 'addenda': addenda, 'patient': p_obj, 'user':user, 'pic':pic},
                              RequestContext(request))


@login_required()
def print_encounter(request, param):
    id = int(param)
    hospital = Clinic.objects.get(clinicid=1)
    enc_obj = Encounter.objects.raw(
        'SELECT e.id, ins.scheme_name, inso.company_name, i.enrollee_number, pd.title, pd.fname, pd.mname, pd.lname, pd.sex, pd.email, pd.address, pd.work_address, pd.occupation, pd.date_of_birth, pd.phonenumber, pd.legacy_patient_id,   sf.firstname, sf.lastname, e.signed_on, e.start_date, d.name AS depart_name, s.staff_type AS staff_special_name FROM encounter e LEFT JOIN departments d ON e.department_id=d.id LEFT JOIN encounter_addendum ed ON ed.encounter_id=e.id LEFT JOIN staff_specialization s ON e.specialization_id=s.id LEFT JOIN staff_directory sf ON e.signed_by=sf.staffId LEFT JOIN patient_demograph pd ON e.patient_id=pd.patient_ID LEFT JOIN insurance i ON pd.patient_ID=i.patient_id LEFT JOIN insurance_schemes ins ON i.insurance_scheme=ins.id LEFT JOIN insurance_owners inso ON ins.scheme_owner_id=inso.id  WHERE e.id=%s',
        [id])

    vitals = VitalSign.objects.raw(
        'SELECT vs.id, v.name AS type_name, v.unit AS type_unit, UNIX_TIMESTAMP(vs.read_date)*1000 AS dDate FROM vital_sign vs LEFT JOIN vital v ON vs.type_id=v.id WHERE encounter_id=%s',
        [id])
    complain = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type IN ("s", "d")', [id])

    sys_review = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="v" ', [id])

    p_medic_history = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="t" ', [id])

    p_drug_history = PatientVisitNotes.objects.raw(
        'SELECT pr.id, pd.comment, dg.name AS gen_name, dg.weight as gen_weight, dg.form AS gen_form FROM patient_regimens pr LEFT JOIN patient_regimens_data pd ON pr.group_code=pd.group_code LEFT JOIN drug_generics dg ON pd.drug_generic_id=dg.id WHERE pr.encounter_id=%s',
        [id])

    allergies = PatientAllergen.objects.raw(
        'SELECT pa.id, pa.allergen, pa.severity, pa.reaction, ds.name AS drug_super_gen, ac.name AS category FROM patient_allergen pa LEFT JOIN allergen_category ac ON pa.category_id=ac.id LEFT JOIN drug_super_generic ds ON pa.drug_super_gen_id=ds.id  WHERE pa.encounter_id=%s AND pa.active IS TRUE',
        [id])

    family_history = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="hx" ', [id])
    physical_exam = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="x" ', [id])

    exam_notes = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="e" ', [id])

    diagnoses = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="a" ', [id])

    investigations = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="i" ', [id])

    plans = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="p" ', [id])

    medications = PatientVisitNotes.objects.raw(
        'SELECT pvn.* FROM patient_visit_notes pvn WHERE pvn.encounter_id = %s AND pvn.note_type="m" ', [id])

    addenda = EncounterAddendum.objects.raw(
        'SELECT ed.*, s.username FROM encounter_addendum ed LEFT JOIN staff_directory s ON ed.user_id=s.staffId WHERE encounter_id=%s',
        [id])
    return render_to_pdf('print_encounter.html',
                         {'pagesize': 'A4', 'enc_obj': enc_obj, 'vitals': vitals, 'complain': complain,
                          'sys_review': sys_review, 'p_medic_history': p_medic_history,
                          'p_drug_history': p_drug_history, 'allergies': allergies, 'family_hist': family_history,
                          'physical_exam': physical_exam, 'exam_notes': exam_notes, 'diagnoses': diagnoses,
                          'investigations': investigations, 'plans': plans, 'medications': medications,
                          'addenda': addenda, 'hospital':hospital}, )
