# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# This code is triggered whenever a new user has been created and saved to
# the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




class AdmissionConfig(models.Model):
    billing_code = models.CharField(max_length=16)
    item_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admission_config'


class AdmissionNote(models.Model):
    admission_id = models.IntegerField()
    medicament_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    note = models.CharField(max_length=2048)
    noted_by = models.CharField(max_length=20)
    note_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'admission_note'


class Alert(models.Model):
    patient_id = models.IntegerField()
    type = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=200, blank=True, null=True)
    read_by = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()
    read = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'alert'


class AllergenCategory(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'allergen_category'


class AntenatalAssessment(models.Model):
    create_date = models.DateTimeField()
    create_user_id = models.IntegerField()
    patient_id = models.IntegerField()
    enrollment_id = models.IntegerField()
    fundusheight = models.FloatField(db_column='fundusHeight', blank=True, null=True)  # Field name made lowercase.
    fhr = models.FloatField(blank=True, null=True)
    fetal_presentation_id = models.IntegerField(blank=True, null=True)
    fetal_brain_relationship_id = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    lab_request_code = models.CharField(max_length=20, blank=True, null=True)
    scan_request_code = models.CharField(max_length=20, blank=True, null=True)
    nextappointmentdate = models.DateTimeField(db_column='nextAppointmentDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'antenatal_assessment'


class AntenatalNotes(models.Model):
    patient_id = models.IntegerField()
    antenatal_enrollment_id = models.IntegerField()
    note = models.TextField()
    type = models.CharField(max_length=18)
    antenatal_assesment_id = models.IntegerField(blank=True, null=True)
    entered_on = models.DateTimeField(blank=True, null=True)
    entered_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'antenatal_notes'


class AntenatalPackageItems(models.Model):
    package_id = models.IntegerField()
    item_id = models.IntegerField()
    type = models.CharField(max_length=12, blank=True, null=True)
    item_usage = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'antenatal_package_items'
        unique_together = (('package_id', 'item_id', 'type'),)


class AntenatalPackages(models.Model):
    package = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'antenatal_packages'


class Appointment(models.Model):
    group_id = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    attended_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9)
    editor_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'appointment'


class AppointmentClinic(models.Model):
    name = models.CharField(max_length=50)
    a_limit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'appointment_clinic'


class AppointmentGroup(models.Model):
    create_time = models.DateTimeField()
    creator = models.IntegerField()
    type = models.CharField(max_length=11)
    clinic_id = models.IntegerField(blank=True, null=True)
    department_id = models.IntegerField(blank=True, null=True)
    is_all_day = models.IntegerField()
    resource_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    patient_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment_group'


class AppointmentInvitee(models.Model):
    group_id = models.IntegerField()
    staff_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'appointment_invitee'


class ApprovedQueue(models.Model):
    patient_id = models.IntegerField()
    type = models.CharField(max_length=14)
    request_id = models.IntegerField()
    approved_time = models.DateTimeField()
    queue_read = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'approved_queue'


class ArvConsulting(models.Model):
    patient_id = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    create_user_id = models.IntegerField()
    create_time = models.IntegerField()
    next_appointment = models.DateField()

    class Meta:
        managed = False
        db_table = 'arv_consulting'


class ArvConsultingData(models.Model):
    arv_consulting_id = models.IntegerField()
    type = models.CharField(max_length=50)
    type_data_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'arv_consulting_data'


class ArvDrug(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'arv_drug'


class ArvDrugData(models.Model):
    patient_id = models.IntegerField()
    arv_drug_id = models.IntegerField()
    type = models.CharField(max_length=13)
    dose = models.CharField(max_length=11)
    state = models.CharField(max_length=11)
    prescribed_by = models.IntegerField()
    date_prescribed = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'arv_drug_data'


class ArvHistory(models.Model):
    arv_template_id = models.IntegerField()
    category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arv_history'


class ArvHistoryTemplate(models.Model):
    label = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'arv_history_template'


class ArvHistoryTemplateData(models.Model):
    arv_history_template_id = models.IntegerField()
    label = models.CharField(max_length=200)
    datatype = models.CharField(max_length=9)
    relation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arv_history_template_data'


class ArvPatientHistory(models.Model):
    patient_id = models.IntegerField()
    arv_history_id = models.IntegerField()
    create_uid = models.IntegerField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'arv_patient_history'


class ArvPatientHistoryData(models.Model):
    arv_patient_history_id = models.IntegerField()
    arv_history_template_data_id = models.IntegerField()
    value = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'arv_patient_history_data'


class AttachmentCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'attachment_category'


class AuditLog(models.Model):
    user_id = models.IntegerField()
    object = models.CharField(max_length=50)
    object_id = models.IntegerField()
    field = models.CharField(max_length=50)
    old_value = models.TextField()
    new_value = models.TextField()
    update_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'audit_log'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthorizationCode(models.Model):
    patient_id = models.IntegerField()
    status = models.CharField(max_length=8)
    creator_id = models.IntegerField()
    create_date = models.DateTimeField()
    receive_date = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=70, blank=True, null=True)
    channel_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authorization_code'


class AuthorizationCodeNote(models.Model):
    authorization_code_id = models.IntegerField()
    note = models.TextField()
    create_time = models.DateTimeField()
    create_user = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'authorization_code_note'


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Badge(models.Model):
    name = models.CharField(max_length=70)
    icon = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'badge'


class Bed(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    room_id = models.IntegerField()
    available = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'bed'


class Bills(models.Model):
    bill_id = models.AutoField(primary_key=True)
    patient_id = models.IntegerField(blank=True, null=True)
    transaction_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    bill_source_id = models.IntegerField(blank=True, null=True)
    bill_sub_source_id = models.IntegerField(blank=True, null=True)
    in_patient_id = models.IntegerField(blank=True, null=True)
    transaction_type = models.CharField(max_length=19)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.FloatField()
    price_type = models.CharField(max_length=16)
    discounted = models.CharField(max_length=3, blank=True, null=True)
    discounted_by = models.IntegerField(blank=True, null=True)
    invoiced = models.CharField(max_length=3, blank=True, null=True)
    receiver = models.ForeignKey('StaffDirectory', models.DO_NOTHING, db_column='receiver', blank=True, null=True)
    auth_code = models.CharField(max_length=70, blank=True, null=True)
    reviewed = models.IntegerField()
    transferred = models.IntegerField()
    claimed = models.IntegerField()
    validated = models.IntegerField()
    voucher_id = models.IntegerField(blank=True, null=True)
    hospid = models.IntegerField(blank=True, null=True)
    billed_to = models.ForeignKey('InsuranceSchemes', models.DO_NOTHING, db_column='billed_to', blank=True, null=True)
    payment_method = models.ForeignKey('PaymentMethods', models.DO_NOTHING, blank=True, null=True)
    payment_reference = models.CharField(max_length=20, blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)
    cost_centre_id = models.IntegerField(blank=True, null=True)
    revenue_account_id = models.IntegerField(blank=True, null=True)
    item_code = models.CharField(max_length=20, blank=True, null=True)
    insurance_code = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.FloatField()
    unit_price = models.IntegerField()
    encounter_id = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    cancelled_by = models.IntegerField(blank=True, null=True)
    misc = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bills'


class BillsSource(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'bills_source'


class Block(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, blank=True, null=True)
    hospital_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'block'


class BodyPart(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'body_part'


class CareTeam(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'care_team'


class Channel(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128, blank=True, null=True)
    enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'channel'


class Claim(models.Model):
    create_date = models.DateTimeField()
    create_user_id = models.IntegerField()
    encounter_id = models.IntegerField()
    line_ids = models.TextField(blank=True, null=True)
    patient_id = models.IntegerField()
    signature_id = models.IntegerField(blank=True, null=True)
    scheme_id = models.IntegerField()
    type = models.CharField(max_length=2)
    status = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'claim'


class Clinic(models.Model):
    clinicid = models.AutoField(db_column='clinicID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=70)
    state_id = models.IntegerField()
    lga_id = models.CharField(max_length=50, blank=True, null=True)
    hosp_code = models.CharField(max_length=10, blank=True, null=True)
    folio_prefix = models.CharField(max_length=10, blank=True, null=True)
    location_lat = models.DecimalField(max_digits=20, decimal_places=10)
    location_long = models.DecimalField(max_digits=20, decimal_places=10)
    class_field = models.CharField(db_column='class', max_length=4)  # Field renamed because it was a Python reserved word.
    phone_no = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clinic'


class ClinicalTask(models.Model):
    patient_id = models.IntegerField()
    in_patient_id = models.IntegerField(blank=True, null=True)
    objective = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    source = models.CharField(max_length=10, blank=True, null=True)
    source_instance_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clinical_task'


class ClinicalTaskChart(models.Model):
    admission_id = models.IntegerField(blank=True, null=True)
    patient_id = models.IntegerField()
    clinical_task_data_id = models.IntegerField()
    nursing_service_id = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=10, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    collected_by = models.IntegerField()
    collected_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'clinical_task_chart'


class ClinicalTaskData(models.Model):
    clinical_task_id = models.IntegerField()
    drug_id = models.IntegerField(blank=True, null=True)
    drug_generic_id = models.IntegerField(blank=True, null=True)
    dose = models.CharField(max_length=11, blank=True, null=True)
    frequency = models.CharField(max_length=16)
    entry_time = models.DateTimeField()
    last_round_time = models.DateTimeField(blank=True, null=True)
    end_round_time = models.DateTimeField(blank=True, null=True)
    task_count = models.IntegerField()
    round_count = models.IntegerField()
    status = models.CharField(max_length=10)
    billed = models.IntegerField()
    type = models.CharField(max_length=21, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    cancel_reason = models.CharField(max_length=254, blank=True, null=True)
    cancelled_by = models.IntegerField(blank=True, null=True)
    cancel_time = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField()
    private = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'clinical_task_data'


class Company(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class Contact(models.Model):
    patient = models.ForeignKey('PatientDemograph', models.DO_NOTHING)
    country_id = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=6)
    primary = models.IntegerField()
    relation = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'contact'


class CostCentre(models.Model):
    name = models.CharField(max_length=25)
    analytical_code = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'cost_centre'


class Countries(models.Model):
    id = models.IntegerField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=50)
    iso_alpha2_code = models.CharField(max_length=2)
    iso_alpha3_code = models.CharField(max_length=3, blank=True, null=True)
    dialing_code = models.CharField(max_length=10, blank=True, null=True)
    iso_numeric = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class CreditLimit(models.Model):
    patient_id = models.CharField(unique=True, max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiration = models.DateField()
    set_by = models.IntegerField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'credit_limit'


class CreditLimitAudit(models.Model):
    patient_id = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiration = models.DateField()
    set_by = models.IntegerField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    date_field = models.DateTimeField(db_column='date_')  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'credit_limit_audit'


class Death(models.Model):
    cert_number = models.CharField(max_length=15, blank=True, null=True)
    age_at_death = models.IntegerField()
    datetime_of_death = models.DateTimeField()
    patient_id = models.IntegerField(unique=True)
    in_patient_id = models.IntegerField(blank=True, null=True)
    primary_cause_id = models.IntegerField(blank=True, null=True)
    secondary_cause_id = models.IntegerField(blank=True, null=True)
    validated_by_id = models.IntegerField(blank=True, null=True)
    validate_on = models.DateTimeField(blank=True, null=True)
    create_uid = models.IntegerField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'death'


class Dentistry(models.Model):
    name = models.CharField(max_length=100)
    billing_code = models.CharField(max_length=10)
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dentistry'


class DentistryCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'dentistry_category'


class DentistryTemplate(models.Model):
    category_id = models.IntegerField()
    title = models.CharField(max_length=50)
    body_part = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dentistry_template'


class Departments(models.Model):
    name = models.CharField(max_length=50)
    cost_centre_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'departments'


class Diagnoses(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=6)
    case = models.CharField(max_length=70, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    oi = models.IntegerField()
    hospid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'diagnoses'


class DiagnosesCopy(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=6)
    case = models.CharField(max_length=500, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    oi = models.IntegerField()
    hospid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'diagnoses_copy'
        unique_together = (('code', 'type'),)


class DiagnosesFull(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=6)
    case = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diagnoses_full'


class DischargeTemplate(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discharge_template'


class DispensedDrugs(models.Model):
    drug_id = models.IntegerField()
    batch_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField()
    unfilled_quantity = models.IntegerField()
    patient_id = models.IntegerField()
    transaction_type = models.CharField(max_length=20, blank=True, null=True)
    billed_to = models.IntegerField()
    date_dispensed = models.DateTimeField()
    pharmacist_id = models.CharField(max_length=11)
    service_center_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispensed_drugs'


class DistributionList(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    sql_query = models.TextField()
    date_added = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'distribution_list'


class DistributionListContacts(models.Model):
    list_id = models.IntegerField()
    patient_id = models.CharField(max_length=11)
    date_added = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'distribution_list_contacts'


class District(models.Model):
    state = models.ForeignKey('State', models.DO_NOTHING)
    name = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DoctorWhoSawWho(models.Model):
    doctor_id = models.IntegerField()
    patient_id = models.IntegerField()
    specialization_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    amount = models.FloatField()
    datetime = models.DateTimeField()
    scheme_id = models.IntegerField(blank=True, null=True)
    department_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor_who_saw_who'


class DoctorsSubscribed(models.Model):
    roomid = models.AutoField(db_column='roomID', primary_key=True)  # Field name made lowercase.
    staffid = models.CharField(db_column='staffID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.IntegerField(blank=True, null=True)
    specialization_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctors_subscribed'


class Drt(models.Model):
    name = models.CharField(max_length=70)
    billing_code = models.CharField(max_length=30, blank=True, null=True)
    create_date = models.DateTimeField()
    create_user_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drt'


class DrugBatch(models.Model):
    name = models.CharField(max_length=120)
    drug_id = models.IntegerField()
    quantity = models.IntegerField()
    expiration_date = models.DateField()
    service_centre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drug_batch'


class DrugBodySystems(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drug_body_systems'


class DrugCategory(models.Model):
    name = models.CharField(max_length=50)
    who_cat_label = models.CharField(max_length=15, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    complementary = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'drug_category'


class DrugFormulary(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drug_formulary'


class DrugFormularyData(models.Model):
    drug_formulary_id = models.IntegerField()
    generic_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'drug_formulary_data'
        unique_together = (('drug_formulary_id', 'generic_id'),)


class DrugGenerics(models.Model):
    active = models.IntegerField()
    name = models.CharField(max_length=30)
    category_ids = models.CharField(max_length=32, blank=True, null=True)
    service_centre_ids = models.CharField(max_length=32, blank=True, null=True)
    who_cat_labels = models.CharField(max_length=15, blank=True, null=True)
    body_systems_rel = models.CharField(max_length=50, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    form = models.CharField(max_length=70, blank=True, null=True)
    description = models.CharField(max_length=70, blank=True, null=True)
    low_stock_level = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'drug_generics'


class DrugManufacturers(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drug_manufacturers'


class DrugRequisition(models.Model):
    create_date = models.DateTimeField()
    create_user_id = models.IntegerField()
    status = models.CharField(max_length=9)
    last_action_user = models.IntegerField(blank=True, null=True)
    last_action = models.CharField(max_length=20, blank=True, null=True)
    last_action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'drug_requisition'


class DrugRequisitionAudit(models.Model):
    item_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20)
    last_action_user = models.IntegerField(blank=True, null=True)
    last_action = models.CharField(max_length=50, blank=True, null=True)
    last_action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'drug_requisition_audit'


class DrugRequisitionLine(models.Model):
    requisition_id = models.IntegerField()
    drug_id = models.IntegerField(blank=True, null=True)
    item_code = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.FloatField()
    batch_name = models.CharField(max_length=50, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drug_requisition_line'


class DrugSuperGeneric(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField()
    last_modified_by = models.IntegerField(blank=True, null=True)
    last_modified_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'drug_super_generic'


class DrugSuperGenericData(models.Model):
    super_generic = models.ForeignKey(DrugSuperGeneric, models.DO_NOTHING, blank=True, null=True)
    drug_generic = models.ForeignKey(DrugGenerics, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drug_super_generic_data'
        unique_together = (('super_generic', 'drug_generic'),)


class Drugs(models.Model):
    name = models.CharField(max_length=50)
    billing_code = models.CharField(max_length=10)
    drug_generic_id = models.IntegerField()
    manufacturer_id = models.IntegerField()
    stock_uom = models.CharField(max_length=30, blank=True, null=True)
    erp_product_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drugs'


class Encounter(models.Model):
    start_date = models.DateTimeField()
    initiator_id = models.IntegerField()
    department_id = models.IntegerField()
    patient_id = models.IntegerField()
    specialization_id = models.IntegerField(blank=True, null=True)
    open = models.IntegerField()
    canceled = models.IntegerField()
    follow_up = models.IntegerField()
    claimed = models.IntegerField()
    signed_by = models.IntegerField(blank=True, null=True)
    signed_on = models.DateTimeField(blank=True, null=True)
    triaged_on = models.DateTimeField(blank=True, null=True)
    triaged_by = models.IntegerField(blank=True, null=True)
    scheme_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'encounter'


class EncounterAddendum(models.Model):
    encounter_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField()
    user_id = models.IntegerField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'encounter_addendum'


class EnrollmentsAntenatal(models.Model):
    requestcode = models.CharField(db_column='requestCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField()
    patient_id = models.IntegerField()
    package_id = models.IntegerField(blank=True, null=True)
    enrolled_at = models.IntegerField()
    enrolled_on = models.DateTimeField()
    enrolled_by = models.IntegerField()
    booking_indication = models.CharField(max_length=15)
    complication_note = models.TextField(blank=True, null=True)
    obgyn_id = models.IntegerField(blank=True, null=True)
    lmp_date = models.DateField(blank=True, null=True)
    lmp_at_enrollment = models.DateField(blank=True, null=True)
    lmp_source = models.CharField(max_length=20, blank=True, null=True)
    ed_date = models.DateField(blank=True, null=True)
    baby_father_name = models.CharField(max_length=100, blank=True, null=True)
    baby_father_phone = models.CharField(max_length=50, blank=True, null=True)
    baby_father_blood_group = models.CharField(max_length=10, blank=True, null=True)
    gravida = models.CharField(max_length=3)
    para = models.CharField(max_length=3)
    alive = models.CharField(max_length=3)
    abortions = models.CharField(max_length=3)
    date_closed = models.DateTimeField(blank=True, null=True)
    close_note = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enrollments_antenatal'


class EnrollmentsImmunization(models.Model):
    patient_id = models.CharField(unique=True, max_length=15)
    enrolled_at = models.IntegerField()
    enrolled_on = models.DateTimeField()
    enrolled_by = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'enrollments_immunization'


class EnrollmentsIvf(models.Model):
    active = models.IntegerField()
    ivf_file_no = models.CharField(max_length=20)
    patient_id = models.IntegerField()
    husband_id = models.IntegerField(blank=True, null=True)
    date_enrolled = models.DateTimeField()
    enrolled_by_id = models.IntegerField()
    indication = models.TextField(blank=True, null=True)
    hormone_fsh = models.CharField(max_length=50, blank=True, null=True)
    hormone_lh = models.CharField(max_length=50, blank=True, null=True)
    hormone_prol = models.CharField(max_length=50, blank=True, null=True)
    hormone_amh = models.CharField(max_length=50, blank=True, null=True)
    husband_hormone_fsh = models.CharField(max_length=50, blank=True, null=True)
    husband_hormone_lh = models.CharField(max_length=50, blank=True, null=True)
    husband_hormone_prol = models.CharField(max_length=50, blank=True, null=True)
    husband_hormone_testosterone = models.CharField(max_length=50, blank=True, null=True)
    sfa_count = models.IntegerField(blank=True, null=True)
    sfa_motility = models.IntegerField(blank=True, null=True)
    sfa_morphology = models.IntegerField(blank=True, null=True)
    serology_hiv = models.CharField(max_length=50, blank=True, null=True)
    serology_hep_b = models.CharField(max_length=50, blank=True, null=True)
    serology_hep_c = models.CharField(max_length=50, blank=True, null=True)
    serology_vdrl = models.CharField(max_length=50, blank=True, null=True)
    serology_chlamydia = models.CharField(max_length=50, blank=True, null=True)
    husband_serology_hiv = models.CharField(max_length=50, blank=True, null=True)
    husband_serology_hep_b = models.CharField(max_length=50, blank=True, null=True)
    husband_serology_hep_c = models.CharField(max_length=50, blank=True, null=True)
    husband_serology_vdrl = models.CharField(max_length=50, blank=True, null=True)
    husband_serology_rbs = models.CharField(max_length=50, blank=True, null=True)
    andrology_details = models.TextField(blank=True, null=True)
    stimulation_cycle = models.CharField(max_length=10, blank=True, null=True)
    stimulation_lmp_date = models.DateField(blank=True, null=True)
    stimulation_method = models.IntegerField(blank=True, null=True)
    stimulation_suprefact = models.CharField(max_length=50, blank=True, null=True)
    stimulation_zoladex = models.CharField(max_length=50, blank=True, null=True)
    stimulation_fsh = models.CharField(max_length=50, blank=True, null=True)
    stimulation_hmg = models.CharField(max_length=50, blank=True, null=True)
    closed_on = models.DateTimeField(blank=True, null=True)
    closed_by = models.IntegerField(blank=True, null=True)
    package_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'enrollments_ivf'


class EnrollmentsLabour(models.Model):
    active = models.IntegerField()
    patient_id = models.IntegerField()
    enrolled_at = models.IntegerField(blank=True, null=True)
    enrolled_on = models.DateTimeField()
    enrolled_by = models.IntegerField(blank=True, null=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    lmpdate = models.DateField(db_column='lmpDate', blank=True, null=True)  # Field name made lowercase.
    baby_father_name = models.CharField(max_length=70, blank=True, null=True)
    baby_father_phone = models.CharField(max_length=13, blank=True, null=True)
    baby_father_blood_group = models.CharField(max_length=4, blank=True, null=True)
    gravida = models.IntegerField(blank=True, null=True)
    para = models.IntegerField(blank=True, null=True)
    alive = models.IntegerField(blank=True, null=True)
    abortions = models.IntegerField(blank=True, null=True)
    current_pregnancy = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enrollments_labour'
        unique_together = (('active', 'patient_id'),)


class EnrollmentsSti(models.Model):
    active = models.IntegerField()
    patient_id = models.IntegerField(unique=True)
    unique_id = models.CharField(max_length=20, blank=True, null=True)
    care_entry_point_id = models.IntegerField(blank=True, null=True)
    date_hiv_confirmed = models.DateField()
    mode_of_test_id = models.IntegerField(blank=True, null=True)
    location_of_test = models.TextField(blank=True, null=True)
    prior_art_id = models.IntegerField(blank=True, null=True)
    enrolled_on = models.DateField()
    enrolled_at = models.CharField(max_length=75)
    enrolled_by_id = models.IntegerField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'enrollments_sti'


class ExamReportTemplate(models.Model):
    title = models.CharField(max_length=50)
    body_part = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_report_template'


class ExamRooms(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=50)
    available = models.IntegerField()
    consultant_id = models.IntegerField(blank=True, null=True)
    specialization_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_rooms'


class ExamTemplate(models.Model):
    title = models.CharField(max_length=50)
    category_id = models.IntegerField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'exam_template'


class ExamTemplateCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'exam_template_category'


class Eye(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    shape = models.CharField(max_length=10, blank=True, null=True)
    coords = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eye'


class EyeReview(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eye_review'


class FakeContact(models.Model):
    phone = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    primary = models.IntegerField(blank=True, null=True)
    fake_patient = models.ForeignKey('FakePatient', models.DO_NOTHING, blank=True, null=True)
    nation = models.ForeignKey(Countries, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fake_contact'


class FakePatient(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    fname = models.CharField(max_length=150, blank=True, null=True)
    lname = models.CharField(max_length=150, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=20, blank=True, null=True)
    work_address = models.TextField(blank=True, null=True)
    res_address = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    geno_type = models.CharField(max_length=10, blank=True, null=True)
    next_kin_fname = models.CharField(max_length=30, blank=True, null=True)
    next_kin_lname = models.CharField(max_length=30, blank=True, null=True)
    next_kin_phone = models.CharField(max_length=15, blank=True, null=True)
    next_kin_address = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Countries, models.DO_NOTHING, blank=True, null=True)
    district = models.ForeignKey(District, models.DO_NOTHING, blank=True, null=True)
    industry = models.ForeignKey('Industry', models.DO_NOTHING, blank=True, null=True)
    lga = models.ForeignKey('Lga', models.DO_NOTHING, blank=True, null=True)
    relationship = models.ForeignKey('KinRelation', models.DO_NOTHING, blank=True, null=True)
    religion = models.ForeignKey('Religion', models.DO_NOTHING, blank=True, null=True)
    res_state = models.ForeignKey('State', models.DO_NOTHING, blank=True, null=True)
    state = models.ForeignKey('State', models.DO_NOTHING, blank=True, null=True)
    res_lga = models.ForeignKey('Lga', models.DO_NOTHING, blank=True, null=True)
    res_dist = models.ForeignKey(District, models.DO_NOTHING, blank=True, null=True)
    phone_search = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fake_patient'


class FetalBrainRelationship(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'fetal_brain_relationship'


class FetalPresentation(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'fetal_presentation'


class FluidChart(models.Model):
    patient_id = models.IntegerField()
    in_patient_id = models.IntegerField()
    route_id = models.IntegerField()
    vol = models.FloatField()
    type = models.CharField(max_length=11)
    user_id = models.IntegerField()
    time_entered = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fluid_chart'


class FluidRoute(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'fluid_route'


class Form(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'form'


class FormComponent(models.Model):
    form_id = models.IntegerField()
    form_question_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'form_component'


class FormPatientQuestion(models.Model):
    patient_id = models.IntegerField()
    form_id = models.IntegerField()
    form_question_id = models.IntegerField()
    create_uid = models.IntegerField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'form_patient_question'


class FormPatientQuestionAnswer(models.Model):
    form_patient_question_id = models.IntegerField()
    form_question_option_id = models.IntegerField()
    value = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'form_patient_question_answer'


class FormQuestion(models.Model):
    form_question_template_id = models.IntegerField()
    category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_question'


class FormQuestionOption(models.Model):
    form_question_template_id = models.IntegerField()
    label = models.CharField(max_length=200)
    datatype = models.CharField(max_length=9)
    relation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_question_option'


class FormQuestionTemplate(models.Model):
    label = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'form_question_template'


class GeneticLab(models.Model):
    name = models.CharField(max_length=50)
    billing_code = models.CharField(max_length=10)
    genetic_template_id = models.IntegerField()
    print_layout = models.CharField(max_length=9)
    quality_control_ids = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'genetic_lab'


class GeneticLabRequest(models.Model):
    request_code = models.CharField(max_length=20, blank=True, null=True)
    female_patient_id = models.IntegerField(blank=True, null=True)
    male_patient_id = models.IntegerField(blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)
    request_date = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    genetic_lab_id = models.IntegerField()
    genetic_specimen_id = models.IntegerField(blank=True, null=True)
    specimen_received_on = models.DateTimeField(blank=True, null=True)
    specimen_received_by = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'genetic_lab_request'


class GeneticLabResult(models.Model):
    genetic_lab_request_id = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    user_id = models.IntegerField()
    time_entered = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'genetic_lab_result'


class GeneticQualityControl(models.Model):
    request_id = models.IntegerField()
    quality_control_type_id = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genetic_quality_control'


class GeneticQualityControlTypes(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'genetic_quality_control_types'


class GeneticReagent(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'genetic_reagent'


class GeneticRequestReagent(models.Model):
    request_id = models.IntegerField()
    reagent_id = models.IntegerField()
    lot_number = models.CharField(max_length=20)
    date_used = models.DateTimeField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'genetic_request_reagent'


class GeneticSpecimen(models.Model):
    name = models.CharField(max_length=70)

    class Meta:
        managed = False
        db_table = 'genetic_specimen'


class GeneticTemplate(models.Model):
    name = models.CharField(max_length=75)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'genetic_template'


class History(models.Model):
    template_id = models.IntegerField()
    category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'history'


class HistoryTemplate(models.Model):
    label = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'history_template'


class HistoryTemplateData(models.Model):
    history_template_id = models.IntegerField()
    label = models.CharField(max_length=200)
    datatype = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'history_template_data'


class ImagingTemplate(models.Model):
    category_id = models.IntegerField()
    title = models.CharField(max_length=50)
    body_part = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imaging_template'


class ImagingTemplateCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'imaging_template_category'


class InPatient(models.Model):
    patient_id = models.IntegerField(blank=True, null=True)
    bed_id = models.IntegerField(blank=True, null=True)
    bed_assign_date = models.DateTimeField(blank=True, null=True)
    date_admitted = models.DateTimeField(blank=True, null=True)
    admitted_by = models.CharField(max_length=11, blank=True, null=True)
    status = models.CharField(max_length=11)
    reason = models.TextField(blank=True, null=True)
    date_discharged = models.DateTimeField(blank=True, null=True)
    date_discharged_full = models.DateTimeField(blank=True, null=True)
    anticipated_discharge_date = models.DateTimeField()
    discharge_note = models.TextField(blank=True, null=True)
    discharged_by = models.CharField(max_length=11, blank=True, null=True)
    discharged_by_full = models.IntegerField(blank=True, null=True)
    hospital_id = models.IntegerField(blank=True, null=True)
    bill_status = models.CharField(max_length=12)
    claimed = models.IntegerField()
    ward_id = models.IntegerField(blank=True, null=True)
    labour_enrollment_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'in_patient'


class Industry(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'industry'


class Insurance(models.Model):
    active = models.IntegerField()
    patient = models.ForeignKey('PatientDemograph', models.DO_NOTHING, unique=True)
    insurance_scheme = models.IntegerField(blank=True, null=True)
    policy_number = models.CharField(max_length=20, blank=True, null=True)
    enrollee_number = models.CharField(max_length=20, blank=True, null=True)
    coverage_type = models.CharField(max_length=25, blank=True, null=True)
    insurance_expiration = models.DateField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    dependent_id = models.IntegerField(blank=True, null=True)
    parent_enrollee_id = models.CharField(max_length=20, blank=True, null=True)
    principal_external = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insurance'


class InsuranceBillableItems(models.Model):
    item_code = models.CharField(max_length=20, blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)
    item_group_category_id = models.IntegerField(blank=True, null=True)
    hospid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'insurance_billable_items'


class InsuranceItemsCost(models.Model):
    item_code = models.CharField(max_length=20, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    followupprice = models.DecimalField(db_column='followUpPrice', max_digits=12, decimal_places=2)  # Field name made lowercase.
    theatreprice = models.DecimalField(db_column='theatrePrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    anaesthesiaprice = models.DecimalField(db_column='anaesthesiaPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    surgeonprice = models.DecimalField(db_column='surgeonPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    co_pay = models.DecimalField(max_digits=10, decimal_places=0)
    insurance_scheme_id = models.IntegerField()
    insurance_code = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=9)
    capitated = models.IntegerField()
    hospid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insurance_items_cost'
        unique_together = (('item_code', 'insurance_scheme_id'),)


class InsuranceOwners(models.Model):
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.CharField(max_length=75, blank=True, null=True)
    hospid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'insurance_owners'


class InsuranceSchemes(models.Model):
    scheme_name = models.CharField(max_length=75, blank=True, null=True)
    badge_id = models.IntegerField(blank=True, null=True)
    scheme_owner = models.ForeignKey(InsuranceOwners, models.DO_NOTHING, blank=True, null=True)
    pay_type = models.CharField(max_length=9)
    insurance_type_id = models.IntegerField(blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2)
    reg_cost_individual = models.DecimalField(max_digits=10, decimal_places=2)
    reg_cost_company = models.DecimalField(max_digits=10, decimal_places=2)
    hospid = models.IntegerField()
    receivables_account_id = models.IntegerField(blank=True, null=True)
    discount_account_id = models.IntegerField(blank=True, null=True)
    partner_id = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=75, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    logo_url = models.TextField(blank=True, null=True)
    clinical_services_rate = models.FloatField()

    class Meta:
        managed = False
        db_table = 'insurance_schemes'


class InsuranceType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'insurance_type'


class Invoice(models.Model):
    patient_id = models.IntegerField(blank=True, null=True)
    scheme_id = models.IntegerField(blank=True, null=True)
    cashier_id = models.IntegerField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'invoice'


class InvoiceLine(models.Model):
    invoice_id = models.IntegerField()
    bill_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'invoice_line'
        unique_together = (('invoice_id', 'bill_id'),)


class IpObservation(models.Model):
    in_patient_id = models.IntegerField()
    date = models.DateTimeField()
    user_id = models.IntegerField()
    note = models.TextField()

    class Meta:
        managed = False
        db_table = 'ip_observation'


class Item(models.Model):
    name = models.CharField(max_length=50)
    billing_code = models.CharField(max_length=10)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'


class ItemBatch(models.Model):
    name = models.CharField(max_length=120)
    item_id = models.IntegerField()
    quantity = models.IntegerField()
    expiration_date = models.DateField()
    service_centre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_batch'


class IvfEggCollection(models.Model):
    instance_id = models.IntegerField(blank=True, null=True)
    time_entered = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)
    collection_time = models.DateTimeField(blank=True, null=True)
    method_id = models.IntegerField(blank=True, null=True)
    done_by_id = models.IntegerField(blank=True, null=True)
    total_left = models.IntegerField(blank=True, null=True)
    total_right = models.IntegerField(blank=True, null=True)
    witness_ids = models.CharField(max_length=20, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_egg_collection'


class IvfEggCollectionFollicleData(models.Model):
    egg_collection_id = models.IntegerField()
    size_id = models.IntegerField()
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ivf_egg_collection_follicle_data'


class IvfEggCollectionMethod(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ivf_egg_collection_method'


class IvfFertilization(models.Model):
    instance_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    time_entered = models.DateTimeField()
    method_id = models.IntegerField(blank=True, null=True)
    zygote_type = models.CharField(max_length=10, blank=True, null=True)
    cell_no = models.IntegerField(blank=True, null=True)
    witness_ids = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_fertilization'
        unique_together = (('instance_id', 'method_id', 'zygote_type'),)


class IvfFollicleSize(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ivf_follicle_size'


class IvfInsemination(models.Model):
    user_id = models.IntegerField()
    time_entered = models.DateTimeField()
    instance_id = models.IntegerField(blank=True, null=True)
    method_id = models.IntegerField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    total_eggs = models.FloatField(blank=True, null=True)
    total_sperm = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    witness_ids = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_insemination'


class IvfMethods(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ivf_methods'


class IvfNote(models.Model):
    instance_id = models.IntegerField()
    note = models.TextField()
    date = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_note'


class IvfNoteTemplate(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_note_template'


class IvfPackage(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_package'


class IvfProtocol(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_protocol'


class IvfSampleSource(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ivf_sample_source'


class IvfSampleState(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ivf_sample_state'


class IvfSimulation(models.Model):
    enrolment_id = models.IntegerField(blank=True, null=True)
    record_date = models.DateTimeField(blank=True, null=True)
    recorded_by_id = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    endo = models.IntegerField(blank=True, null=True)
    e2 = models.IntegerField(blank=True, null=True)
    gnrha = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hmg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ant = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fsh = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_simulation'


class IvfSimulationData(models.Model):
    ivf_simulation_id = models.IntegerField()
    right_side = models.IntegerField()
    left_side = models.IntegerField()
    size_index_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ivf_simulation_data'


class IvfSpermAnalysis(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    time_entered = models.DateTimeField()
    instance_id = models.IntegerField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    cell_no = models.IntegerField(blank=True, null=True)
    density = models.FloatField(blank=True, null=True)
    motility = models.FloatField(blank=True, null=True)
    prog = models.CharField(max_length=50, blank=True, null=True)
    abnormal = models.FloatField(blank=True, null=True)
    mar = models.CharField(max_length=50, blank=True, null=True)
    aggl = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    witness_ids = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_sperm_analysis'


class IvfSpermCollection(models.Model):
    instance_id = models.IntegerField(blank=True, null=True)
    time_entered = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    donor_code = models.CharField(max_length=20, blank=True, null=True)
    procedure_id = models.IntegerField(blank=True, null=True)
    abstinence_days = models.IntegerField()
    collection_date = models.DateTimeField(blank=True, null=True)
    witness_ids = models.CharField(max_length=20, blank=True, null=True)
    analysis_post_report = models.TextField(blank=True, null=True)
    analysis_pre_report = models.TextField(blank=True, null=True)
    production_time = models.DateTimeField(blank=True, null=True)
    analysis_time = models.DateTimeField(blank=True, null=True)
    preparation_method = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_sperm_collection'


class IvfSpermProcedure(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ivf_sperm_procedure'


class IvfTransferType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ivf_transfer_type'


class IvfTreatment(models.Model):
    enrollment_id = models.IntegerField()
    date = models.DateTimeField(blank=True, null=True)
    day_of_cycle = models.IntegerField(blank=True, null=True)
    buserelin = models.CharField(max_length=70, blank=True, null=True)
    guserelin = models.CharField(max_length=70, blank=True, null=True)
    findings = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ivf_treatment'


class KinRelation(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'kin_relation'


class LabCombo(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'lab_combo'


class LabComboData(models.Model):
    lab_combo_id = models.IntegerField()
    lab_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lab_combo_data'


class LabNotes(models.Model):
    lab_group_id = models.CharField(max_length=11, blank=True, null=True)
    lab_note = models.TextField(blank=True, null=True)
    when = models.DateTimeField(blank=True, null=True)
    who = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_notes'


class LabRequests(models.Model):
    lab_group_id = models.CharField(max_length=50)
    patient_id = models.IntegerField(blank=True, null=True)
    requested_by = models.CharField(max_length=15, blank=True, null=True)
    request_note = models.TextField(blank=True, null=True)
    time_entered = models.DateTimeField()
    preferred_specimens = models.TextField(blank=True, null=True)
    hospid = models.IntegerField(blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)
    service_centre_id = models.IntegerField(blank=True, null=True)
    in_patient_id = models.IntegerField(blank=True, null=True)
    encounter_id = models.IntegerField(blank=True, null=True)
    urgent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_requests'


class LabResult(models.Model):
    lab_template = models.ForeignKey('LabTemplate', models.DO_NOTHING)
    patient_lab = models.ForeignKey('PatientLabs', models.DO_NOTHING)
    abnormal_lab_value = models.IntegerField()
    approved = models.IntegerField()
    approved_by = models.CharField(max_length=15, blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_result'


class LabResultData(models.Model):
    lab_result = models.ForeignKey(LabResult, models.DO_NOTHING)
    lab_template_data = models.ForeignKey('LabTemplateData', models.DO_NOTHING)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'lab_result_data'
        unique_together = (('lab_result', 'lab_template_data'),)


class LabSpecimen(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'lab_specimen'


class LabTemplate(models.Model):
    label = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'lab_template'


class LabTemplateData(models.Model):
    lab_template = models.ForeignKey(LabTemplate, models.DO_NOTHING)
    label = models.CharField(max_length=32)
    reference = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'lab_template_data'


class LabTestsGroup(models.Model):
    name = models.CharField(max_length=20)
    test_ids = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'lab_tests_group'


class LabtestsConfig(models.Model):
    billing_code = models.CharField(max_length=16)
    name = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey('LabtestsConfigCategory', models.DO_NOTHING)
    lab_template_id = models.IntegerField()
    testunit_symbol = models.CharField(db_column='testUnit_Symbol', max_length=30, blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(blank=True, null=True)
    hospid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'labtests_config'


class LabtestsConfigCategory(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'labtests_config_category'


class Lga(models.Model):
    state = models.ForeignKey('State', models.DO_NOTHING)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'lga'


class LifeStyle(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'life_style'


class LogAppointment(models.Model):
    aid = models.IntegerField()
    group_id = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    attended_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9)
    log_time = models.DateTimeField()
    editor_id = models.IntegerField()
    trig_type = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'log_appointment'


class MedicalExam(models.Model):
    name = models.CharField(max_length=50)
    billing_code = models.CharField(max_length=10)
    labs = models.CharField(max_length=500, blank=True, null=True)
    procedures = models.CharField(max_length=500, blank=True, null=True)
    imagings = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medical_exam'


class MessageDispatch(models.Model):
    pid = models.CharField(max_length=12)
    message = models.TextField()
    sms_channel_address = models.CharField(max_length=20)
    sms_delivery_status = models.IntegerField()
    email_channel_address = models.CharField(max_length=200)
    email_delivery_status = models.IntegerField()
    voice_channel_address = models.CharField(max_length=20, blank=True, null=True)
    voice_delivery_status = models.IntegerField()
    export_status = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_dispatch'


class MessageDistributionList(models.Model):
    patient_id = models.CharField(max_length=11)
    list = models.CharField(max_length=50)
    date_added = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'message_distribution_list'


class MessageQueueTemp(models.Model):
    data_id = models.IntegerField()
    date_generated = models.DateTimeField()
    source = models.CharField(max_length=20)
    message_content = models.CharField(max_length=320)
    message_status = models.IntegerField()
    patient = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'message_queue_temp'


class MessageSubscription(models.Model):
    patient = models.CharField(max_length=64)
    channel_subscribed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'message_subscription'


class MessageTemplate(models.Model):
    channel = models.ForeignKey(Channel, models.DO_NOTHING)
    template_text = models.TextField()
    text_type = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'message_template'


class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    staffid = models.CharField(db_column='staffId', max_length=11, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=6, blank=True, null=True)
    when = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class NursingService(models.Model):
    billing_code = models.CharField(unique=True, max_length=16)
    service_name = models.CharField(max_length=50, blank=True, null=True)
    hospid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nursing_service'


class NursingTemplate(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'nursing_template'


class Onlinestatus(models.Model):
    staffid = models.IntegerField(db_column='staffId', primary_key=True)  # Field name made lowercase.
    is_online = models.IntegerField()
    last_seen = models.DateTimeField(blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'onlinestatus'


class Ophthalmology(models.Model):
    billing_code = models.CharField(max_length=16)
    name = models.CharField(max_length=50, blank=True, null=True)
    category_id = models.IntegerField()
    ophthalmology_template_id = models.IntegerField(blank=True, null=True)
    unit_symbol = models.CharField(max_length=30, blank=True, null=True)
    reference = models.TextField(blank=True, null=True)
    hospid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ophthalmology'


class OphthalmologyCategory(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ophthalmology_category'


class OphthalmologyItem(models.Model):
    billing_code = models.CharField(max_length=16)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ophthalmology_item'


class OphthalmologyItemBatch(models.Model):
    name = models.CharField(max_length=120)
    item_id = models.IntegerField()
    quantity = models.IntegerField()
    service_centre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ophthalmology_item_batch'


class OphthalmologyItemsRequest(models.Model):
    patient_id = models.IntegerField(blank=True, null=True)
    requested_by = models.IntegerField(blank=True, null=True)
    received_by = models.DateTimeField(blank=True, null=True)
    delivered_by = models.DateTimeField(blank=True, null=True)
    time_entered = models.DateTimeField()
    time_received = models.DateTimeField(blank=True, null=True)
    time_delivered = models.DateTimeField(blank=True, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=9)
    service_centre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ophthalmology_items_request'


class OphthalmologyItemsRequestData(models.Model):
    request_id = models.IntegerField()
    item_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ophthalmology_items_request_data'


class OphthalmologyRequests(models.Model):
    group_code = models.CharField(max_length=7)
    patient_id = models.CharField(max_length=11, blank=True, null=True)
    requested_by = models.CharField(max_length=15, blank=True, null=True)
    time_entered = models.DateTimeField()
    preferred_specimens = models.TextField(blank=True, null=True)
    hospid = models.IntegerField(blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)
    service_centre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ophthalmology_requests'


class OphthalmologyResult(models.Model):
    ophthalmology_template_id = models.IntegerField()
    patient_ophthalmology_id = models.IntegerField()
    abnormal_ophthalmology_value = models.IntegerField()
    approved = models.IntegerField()
    approved_by = models.CharField(max_length=15, blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ophthalmology_result'


class OphthalmologyResultData(models.Model):
    ophthalmology_result_id = models.IntegerField()
    ophthalmology_template_data_id = models.IntegerField()
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ophthalmology_result_data'
        unique_together = (('ophthalmology_result_id', 'ophthalmology_template_data_id'),)


class OphthalmologySpecimen(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'ophthalmology_specimen'


class OphthalmologyTemplate(models.Model):
    label = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ophthalmology_template'


class OphthalmologyTemplateData(models.Model):
    ophthalmology_template_id = models.IntegerField()
    label = models.CharField(max_length=32)
    reference = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'ophthalmology_template_data'


class Package(models.Model):
    active = models.IntegerField()
    expiration = models.DateField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=70)
    billing_code = models.CharField(max_length=30, blank=True, null=True)
    create_date = models.DateTimeField()
    create_user_id = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'package'


class PackageCategory(models.Model):
    name = models.CharField(max_length=70)

    class Meta:
        managed = False
        db_table = 'package_category'


class PackageItem(models.Model):
    package_id = models.IntegerField()
    item_code = models.CharField(max_length=20)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'package_item'
        unique_together = (('package_id', 'item_code'),)


class PackageSubscription(models.Model):
    patient_id = models.IntegerField()
    package_id = models.IntegerField()
    date_subscribed = models.DateTimeField()
    active = models.IntegerField()
    create_user = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_subscription'


class PackageToken(models.Model):
    patient_id = models.IntegerField()
    original_quantity = models.IntegerField()
    quantity_left = models.IntegerField()
    item_code = models.CharField(max_length=12)
    date_bought = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'package_token'


class PackageTokenUsage(models.Model):
    patient_id = models.IntegerField()
    item_code = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.IntegerField()
    use_date = models.DateTimeField()
    responsible_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'package_token_usage'


class PatientAllergen(models.Model):
    active = models.IntegerField()
    patient_id = models.CharField(db_column='patient_ID', max_length=11)  # Field name made lowercase.
    allergen = models.CharField(max_length=50, blank=True, null=True)
    reaction = models.TextField()
    severity = models.CharField(max_length=11)
    noted_by = models.IntegerField()
    date_noted = models.DateTimeField()
    hospid = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    drug_super_gen_id = models.IntegerField(blank=True, null=True)
    encounter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_allergen'


class PatientAntenatal(models.Model):
    patient_id = models.CharField(max_length=15, blank=True, null=True)
    family_id = models.CharField(max_length=15, blank=True, null=True)
    family_role = models.CharField(max_length=8, blank=True, null=True)
    antenatal_status = models.CharField(max_length=10, blank=True, null=True)
    date_antenated = models.DateField(blank=True, null=True)
    date_last_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'patient_antenatal'


class PatientAntenatalItems(models.Model):
    patient_id = models.CharField(max_length=15)
    chart_item_id = models.IntegerField()
    chart_item_level = models.IntegerField()
    type = models.CharField(max_length=11)
    due_date = models.DateField()
    date_taken = models.DateField(blank=True, null=True)
    taken_by = models.CharField(max_length=15, blank=True, null=True)
    expiration_date = models.DateField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_antenatal_items'


class PatientAntenatalUsages(models.Model):
    aid = models.IntegerField()
    patient_id = models.IntegerField()
    item_id = models.IntegerField()
    item_type = models.CharField(max_length=12)
    usages = models.IntegerField()
    date_used = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'patient_antenatal_usages'


class PatientAttachment(models.Model):
    patient_id = models.IntegerField()
    category_id = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=255)
    document_url = models.CharField(max_length=255)
    date_added = models.DateTimeField()
    user_add_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'patient_attachment'


class PatientCareMember(models.Model):
    in_patient_id = models.IntegerField()
    care_member_id = models.IntegerField(blank=True, null=True)
    care_team_id = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField()
    entry_time = models.DateTimeField()
    changed_by = models.IntegerField(blank=True, null=True)
    change_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9)
    type = models.CharField(max_length=6)
    primary_care_id = models.IntegerField(blank=True, null=True)
    primary_care_type = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'patient_care_member'


class PatientDemograph(models.Model):
    patient_id = models.AutoField(db_column='patient_ID', primary_key=True)  # Field name made lowercase.
    active = models.IntegerField()
    deceased = models.IntegerField()
    legacy_patient_id = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=75, blank=True, null=True)
    login_id = models.IntegerField(blank=True, null=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    mname = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    dob_estimated = models.IntegerField()
    sex = models.CharField(max_length=6)
    email = models.CharField(max_length=128)
    address = models.CharField(max_length=70)
    nationality = models.IntegerField()
    occupation = models.TextField(blank=True, null=True)
    work_address = models.TextField(blank=True, null=True)
    industry_id = models.IntegerField(blank=True, null=True)
    religion_id = models.IntegerField(blank=True, null=True)
    lga_id = models.IntegerField()
    district_id = models.IntegerField(blank=True, null=True)
    state_id = models.IntegerField()
    state_res_id = models.IntegerField()
    lga_res_id = models.IntegerField()
    district_res_id = models.IntegerField(blank=True, null=True)
    kinsfirstname = models.CharField(db_column='KinsFirstName', max_length=20)  # Field name made lowercase.
    kinslastname = models.CharField(db_column='KinsLastName', max_length=20)  # Field name made lowercase.
    kinsphone = models.CharField(db_column='KinsPhone', max_length=20)  # Field name made lowercase.
    kinsaddress = models.CharField(db_column='KinsAddress', max_length=70)  # Field name made lowercase.
    kin_relation_id = models.IntegerField(blank=True, null=True)
    registered_by = models.CharField(db_column='registered_By', max_length=11)  # Field name made lowercase.
    phonenumber = models.CharField(max_length=17, blank=True, null=True)
    foreign_number = models.CharField(max_length=20, blank=True, null=True)
    bloodgroup = models.CharField(max_length=10, blank=True, null=True)
    bloodtype = models.CharField(max_length=10, blank=True, null=True)
    basehospital = models.CharField(max_length=70, blank=True, null=True)
    transferedto = models.CharField(max_length=70, blank=True, null=True)
    enrollment_date = models.DateTimeField()
    referral_id = models.IntegerField(blank=True, null=True)
    referral_company_id = models.IntegerField(blank=True, null=True)
    socio_economic = models.IntegerField(blank=True, null=True)
    lifestyle = models.CharField(max_length=20, blank=True, null=True)
    care_manager_id = models.IntegerField(blank=True, null=True)
    scheme_at_registration_id = models.IntegerField(blank=True, null=True)
    last_modified_by = models.IntegerField(blank=True, null=True)
    last_modified_date = models.DateTimeField(blank=True, null=True)
    cum_annual_days_on_admission = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'patient_demograph'


class PatientDentistry(models.Model):
    requestcode = models.CharField(db_column='requestCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    patient_id = models.IntegerField()
    dentistry_ids = models.CharField(max_length=200)
    request_note = models.CharField(max_length=120, blank=True, null=True)
    requested_by_id = models.IntegerField()
    request_date = models.DateTimeField()
    approved = models.IntegerField()
    approved_by_id = models.IntegerField(blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    date_last_modified = models.DateTimeField()
    status = models.IntegerField()
    cancelled = models.IntegerField()
    cancel_date = models.DateTimeField(blank=True, null=True)
    canceled_by_id = models.IntegerField(blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_dentistry'


class PatientDentistryNotes(models.Model):
    patient_dentistry_id = models.IntegerField(blank=True, null=True)
    note = models.TextField()
    note_area = models.CharField(max_length=50)
    create_uid = models.CharField(max_length=15)
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'patient_dentistry_notes'


class PatientDiagnoses(models.Model):
    patient_id = models.IntegerField(db_column='patient_ID')  # Field name made lowercase.
    date_of_entry = models.DateTimeField()
    diagnosed_by = models.IntegerField(blank=True, null=True)
    diagnosisnote = models.TextField(db_column='diagnosisNote', blank=True, null=True)  # Field name made lowercase.
    diag_type = models.CharField(db_column='diag-type', max_length=2, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    diagnosis = models.CharField(max_length=300, blank=True, null=True)
    field_status = models.CharField(db_column='_status', max_length=12, blank=True, null=True)  # Field renamed because it started with '_'.
    severity = models.CharField(max_length=9)
    active = models.IntegerField()
    hospital_diagnosed = models.CharField(max_length=50, blank=True, null=True)
    encounter_id = models.IntegerField(blank=True, null=True)
    in_patient_id = models.IntegerField(blank=True, null=True)
    body_part_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_diagnoses'


class PatientHistory(models.Model):
    assessment_id = models.IntegerField(blank=True, null=True)
    patient_id = models.IntegerField()
    history_id = models.IntegerField()
    create_uid = models.IntegerField()
    create_date = models.DateTimeField()
    instance_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_history'


class PatientHistoryData(models.Model):
    patient_history_id = models.IntegerField()
    history_template_data_id = models.IntegerField()
    value = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'patient_history_data'


class PatientInRoom(models.Model):
    roomid = models.CharField(db_column='roomID', max_length=5, blank=True, null=True)  # Field name made lowercase.
    patientid = models.CharField(db_column='patientID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    queue_for = models.CharField(max_length=6)
    time_in = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'patient_in_room'


class PatientLabs(models.Model):
    patient_id = models.IntegerField(blank=True, null=True)
    test_id = models.IntegerField(blank=True, null=True)
    lab_group_id = models.CharField(max_length=50)
    performed_by = models.CharField(max_length=11, blank=True, null=True)
    test_notes = models.TextField(blank=True, null=True)
    test_specimen_ids = models.CharField(max_length=30, blank=True, null=True)
    test_date = models.DateTimeField(blank=True, null=True)
    specimen_collected_by = models.CharField(max_length=15, blank=True, null=True)
    specimen_notes = models.CharField(max_length=50, blank=True, null=True)
    specimen_date = models.DateTimeField(blank=True, null=True)
    received = models.IntegerField()
    specimen_received_by = models.IntegerField(blank=True, null=True)
    field_status = models.CharField(db_column='_status', max_length=9)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'patient_labs'


class PatientMedicalReport(models.Model):
    requestcode = models.CharField(db_column='requestCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    patient_id = models.IntegerField()
    exam_id = models.IntegerField()
    request_note = models.CharField(max_length=120, blank=True, null=True)
    requested_by_id = models.IntegerField()
    request_date = models.DateTimeField()
    approved = models.IntegerField()
    approved_by_id = models.IntegerField(blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    date_last_modified = models.DateTimeField()
    cancelled = models.IntegerField()
    cancel_date = models.DateTimeField(blank=True, null=True)
    canceled_by_id = models.IntegerField(blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)
    labs = models.IntegerField(blank=True, null=True)
    imagings = models.CharField(max_length=100, blank=True, null=True)
    procedures = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_medical_report'


class PatientMedicalReportNote(models.Model):
    patient_medical_report_id = models.IntegerField(blank=True, null=True)
    note = models.TextField()
    create_uid = models.CharField(max_length=15)
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'patient_medical_report_note'


class PatientMedicament(models.Model):
    admission_id = models.IntegerField()
    drug_id = models.IntegerField()
    method = models.CharField(max_length=20)
    dosage = models.IntegerField()
    every = models.CharField(max_length=10)
    interval = models.IntegerField()
    time_strict = models.IntegerField()
    created_by = models.CharField(max_length=20)
    created_on = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'patient_medicament'


class PatientOphthalmology(models.Model):
    patient_id = models.CharField(max_length=15, blank=True, null=True)
    ophthalmology_id = models.IntegerField(blank=True, null=True)
    ophthalmology_group_code = models.CharField(max_length=7)
    performed_by = models.CharField(max_length=11, blank=True, null=True)
    test_notes = models.TextField(blank=True, null=True)
    ophthalmology_specimen_ids = models.CharField(max_length=30, blank=True, null=True)
    test_date = models.DateTimeField(blank=True, null=True)
    specimen_collected_by = models.CharField(max_length=15, blank=True, null=True)
    specimen_notes = models.CharField(max_length=50, blank=True, null=True)
    specimen_date = models.DateTimeField(blank=True, null=True)
    received = models.IntegerField()
    specimen_received_by = models.IntegerField(blank=True, null=True)
    field_status = models.CharField(db_column='_status', max_length=9)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'patient_ophthalmology'


class PatientPhysicalAssessments(models.Model):
    patient_id = models.CharField(max_length=15)
    heent = models.CharField(db_column='HEENT', max_length=200)  # Field name made lowercase.
    heent_note = models.CharField(db_column='HEENT_Note', max_length=70, blank=True, null=True)  # Field name made lowercase.
    heart = models.CharField(db_column='Heart', max_length=200)  # Field name made lowercase.
    heart_note = models.CharField(db_column='Heart_Note', max_length=70, blank=True, null=True)  # Field name made lowercase.
    lungs = models.CharField(db_column='Lungs', max_length=200)  # Field name made lowercase.
    lungs_note = models.CharField(db_column='Lungs_Note', max_length=70, blank=True, null=True)  # Field name made lowercase.
    abdomen = models.CharField(db_column='Abdomen', max_length=200)  # Field name made lowercase.
    abdomen_note = models.CharField(db_column='Abdomen_Note', max_length=70, blank=True, null=True)  # Field name made lowercase.
    extremites = models.CharField(db_column='Extremites', max_length=200)  # Field name made lowercase.
    extremites_note = models.CharField(db_column='Extremites_Note', max_length=70, blank=True, null=True)  # Field name made lowercase.
    skin = models.CharField(db_column='Skin', max_length=200)  # Field name made lowercase.
    skin_note = models.CharField(db_column='Skin_Note', max_length=70, blank=True, null=True)  # Field name made lowercase.
    neuro = models.CharField(db_column='Neuro', max_length=200)  # Field name made lowercase.
    neuro_note = models.CharField(db_column='Neuro_Note', max_length=70, blank=True, null=True)  # Field name made lowercase.
    assessed_by = models.CharField(max_length=15)
    entry_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'patient_physical_assessments'


class PatientPhysicalExamination(models.Model):
    patient_id = models.IntegerField()
    date = models.DateTimeField()
    physical_examination_id = models.IntegerField()
    reviewer_id = models.IntegerField()
    encounter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_physical_examination'


class PatientPreConditions(models.Model):
    patient_id = models.CharField(max_length=15)
    field_condition = models.CharField(db_column='_condition', max_length=150)  # Field renamed because it started with '_'.
    diag_date = models.DateField(blank=True, null=True)
    severity = models.IntegerField()
    therapy = models.CharField(max_length=20)
    therapy_start_date = models.DateField(blank=True, null=True)
    response = models.IntegerField()
    active = models.IntegerField()
    history = models.IntegerField()
    entered_by = models.CharField(max_length=15)
    date_entered = models.DateTimeField()
    hospid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_pre_conditions'


class PatientProcedure(models.Model):
    patient_id = models.IntegerField()
    in_patient_id = models.IntegerField(blank=True, null=True)
    procedure_id = models.IntegerField()
    request_id = models.CharField(max_length=20)
    request_date = models.DateTimeField()
    condition_ids = models.CharField(max_length=70, blank=True, null=True)
    field_status = models.CharField(db_column='_status', max_length=9)  # Field renamed because it started with '_'.
    time_start = models.DateTimeField(blank=True, null=True)
    time_stop = models.DateTimeField(blank=True, null=True)
    closing_text = models.CharField(max_length=255, blank=True, null=True)
    resource_id = models.IntegerField(blank=True, null=True)
    requested_by_id = models.IntegerField()
    theatre_id = models.IntegerField(blank=True, null=True)
    has_anesthesiologist = models.IntegerField()
    anesthesiologist_id = models.IntegerField(blank=True, null=True)
    has_surgeon = models.IntegerField()
    surgeon_id = models.IntegerField(blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)
    service_centre_id = models.IntegerField(blank=True, null=True)
    encounter_id = models.IntegerField(blank=True, null=True)
    bodypart_id = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)
    source_instance_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_procedure'


class PatientProcedureItems(models.Model):
    patient_procedure_id = models.IntegerField()
    item_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'patient_procedure_items'
        unique_together = (('patient_procedure_id', 'item_id'),)


class PatientProcedureNote(models.Model):
    patient_procedure_id = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    staff_id = models.IntegerField()
    note_time = models.DateTimeField()
    note_type = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_procedure_note'


class PatientProcedureNursingTask(models.Model):
    patient_procedure_id = models.IntegerField()
    service_id = models.IntegerField(blank=True, null=True)
    create_uid = models.IntegerField()
    date_field = models.DateTimeField(db_column='date_')  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'patient_procedure_nursing_task'


class PatientProcedureRegimen(models.Model):
    patient_procedure_id = models.IntegerField()
    drug_id = models.IntegerField()
    batch_id = models.IntegerField()
    quantity = models.IntegerField()
    request_time = models.DateTimeField()
    request_user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'patient_procedure_regimen'


class PatientProcedureReport(models.Model):
    patient_procedure_id = models.IntegerField()
    request_time = models.DateTimeField()
    report_user_id = models.IntegerField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'patient_procedure_report'


class PatientProcedureResource(models.Model):
    patient_procedure_id = models.IntegerField()
    staff_id = models.IntegerField(blank=True, null=True)
    create_uid = models.IntegerField()
    date_field = models.DateTimeField(db_column='date_')  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'patient_procedure_resource'


class PatientQueue(models.Model):
    patient_id = models.IntegerField()
    type = models.CharField(max_length=13)
    sub_type = models.CharField(max_length=50, blank=True, null=True)
    entry_time = models.DateTimeField()
    attended_time = models.DateTimeField(blank=True, null=True)
    tag_no = models.IntegerField()
    blocked_by = models.IntegerField(blank=True, null=True)
    seen_by = models.IntegerField(blank=True, null=True)
    department_id = models.IntegerField(blank=True, null=True)
    specialization_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=9, blank=True, null=True)
    cancelled_by = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    follow_up = models.IntegerField()
    encounter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_queue'


class PatientRegimens(models.Model):
    external = models.IntegerField()
    patient_id = models.IntegerField()
    when = models.DateTimeField()
    group_code = models.CharField(unique=True, max_length=20)
    requested_by = models.CharField(max_length=15, blank=True, null=True)
    service_centre_id = models.IntegerField(blank=True, null=True)
    in_patient_id = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    hospid = models.IntegerField(blank=True, null=True)
    refill_off = models.IntegerField(blank=True, null=True)
    encounter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_regimens'


class PatientRegimensData(models.Model):
    group_code = models.CharField(max_length=20)
    drug_id = models.IntegerField(blank=True, null=True)
    drug_generic_id = models.IntegerField()
    quantity = models.IntegerField(blank=True, null=True)
    dose = models.CharField(max_length=100)
    duration = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    batch_id = models.IntegerField(blank=True, null=True)
    frequency = models.CharField(max_length=20)
    refillable = models.IntegerField()
    status = models.CharField(max_length=9)
    requested_by = models.CharField(max_length=14, blank=True, null=True)
    modified_by = models.CharField(max_length=14, blank=True, null=True)
    filled_by = models.CharField(max_length=14, blank=True, null=True)
    filled_on = models.DateTimeField(blank=True, null=True)
    completed_by = models.CharField(max_length=14, blank=True, null=True)
    completed_on = models.DateTimeField(blank=True, null=True)
    cancelled_by = models.CharField(max_length=14, blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    cancel_note = models.TextField(blank=True, null=True)
    hospid = models.IntegerField(blank=True, null=True)
    bodypart_id = models.IntegerField(blank=True, null=True)
    external_source = models.IntegerField()
    refill_date = models.DateTimeField(blank=True, null=True)
    refill_number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_regimens_data'


class PatientScan(models.Model):
    requestcode = models.CharField(db_column='requestCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    patient_id = models.IntegerField()
    scan_ids = models.CharField(max_length=200)
    request_note = models.CharField(max_length=120, blank=True, null=True)
    requested_by_id = models.IntegerField()
    request_date = models.DateTimeField()
    approved = models.IntegerField()
    approved_by_id = models.IntegerField(blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    date_last_modified = models.DateTimeField()
    status = models.IntegerField()
    cancelled = models.IntegerField()
    cancel_date = models.DateTimeField(blank=True, null=True)
    canceled_by_id = models.IntegerField(blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)
    encounter_id = models.IntegerField(blank=True, null=True)
    service_centre_id = models.IntegerField(blank=True, null=True)
    captured = models.IntegerField()
    captured_date = models.DateTimeField(blank=True, null=True)
    captured_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_scan'


class PatientScanAttachment(models.Model):
    patient_scan_id = models.IntegerField()
    attachment_url = models.TextField()
    note = models.CharField(max_length=255)
    timeadded = models.DateTimeField(db_column='timeAdded')  # Field name made lowercase.
    create_uid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'patient_scan_attachment'


class PatientScanNotes(models.Model):
    patient_scan_id = models.IntegerField(blank=True, null=True)
    note = models.TextField()
    note_area = models.CharField(max_length=50)
    create_uid = models.CharField(max_length=15)
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'patient_scan_notes'


class PatientScanTypes(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'patient_scan_types'


class PatientSystemsReview(models.Model):
    patient_id = models.IntegerField()
    date = models.DateTimeField()
    systems_review_id = models.IntegerField()
    reviewer_id = models.IntegerField()
    assessment_id = models.IntegerField(blank=True, null=True)
    antenatal_instance_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=9, blank=True, null=True)
    encounter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_systems_review'


class PatientVaccine(models.Model):
    patient_id = models.CharField(max_length=15)
    vaccine_id = models.IntegerField()
    is_booster = models.IntegerField()
    vaccine_level = models.IntegerField()
    due_date = models.DateField(blank=True, null=True)
    billed = models.IntegerField()
    entry_date = models.DateField(blank=True, null=True)
    taken_by = models.CharField(max_length=15, blank=True, null=True)
    take_type = models.CharField(max_length=5)
    internal = models.IntegerField()
    route = models.CharField(max_length=2)
    site = models.CharField(max_length=50, blank=True, null=True)
    dosage = models.CharField(max_length=10, blank=True, null=True)
    real_administer_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_vaccine'


class PatientVaccineBooster(models.Model):
    patient_id = models.CharField(max_length=15)
    vaccinebooster_id = models.IntegerField()
    start_date = models.DateField(blank=True, null=True)
    next_due_date = models.DateField(blank=True, null=True)
    last_taken = models.DateField(blank=True, null=True)
    charged = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'patient_vaccine_booster'


class PatientVaccineBoosterHistory(models.Model):
    patientvaccinebooster_id = models.IntegerField()
    date_taken = models.DateField()
    taken_by = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'patient_vaccine_booster_history'


class PatientVaccineTemp(models.Model):
    patient_id = models.CharField(max_length=15)
    vaccine_id = models.IntegerField()
    vaccine_level = models.IntegerField()
    due_date = models.DateField()
    paid = models.IntegerField()
    date_taken = models.DateField(blank=True, null=True)
    taken_by = models.CharField(max_length=15, blank=True, null=True)
    expiration_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'patient_vaccine_temp'


class PatientVisitNotes(models.Model):
    patient_id = models.IntegerField(db_column='patient_ID')  # Field name made lowercase.
    date_of_entry = models.DateTimeField()
    noted_by = models.IntegerField()
    description = models.TextField()
    note_type = models.CharField(max_length=2, blank=True, null=True)
    reason = models.CharField(max_length=26)
    hospitalvisited = models.CharField(max_length=70, blank=True, null=True)
    sourceapp = models.CharField(max_length=15, blank=True, null=True)
    module = models.CharField(max_length=25)
    encounter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_visit_notes'


class PaymentMethods(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=33)
    ledger_id = models.IntegerField(blank=True, null=True)
    hospid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'payment_methods'


class PhysicalAssessmentGroups(models.Model):
    group_id = models.IntegerField(primary_key=True)
    patient_id = models.CharField(max_length=15)
    entry_date = models.DateTimeField()
    assessed_by = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'physical_assessment_groups'


class PhysicalExamination(models.Model):
    abbr = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=150)
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'physical_examination'


class PhysicalExaminationCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'physical_examination_category'


class PhysiotherapyBooking(models.Model):
    requestcode = models.CharField(db_column='requestCode', max_length=25, blank=True, null=True)  # Field name made lowercase.
    patient_id = models.IntegerField()
    booking_date = models.DateTimeField()
    specialization_id = models.IntegerField()
    count = models.IntegerField()
    booked_by = models.IntegerField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'physiotherapy_booking'


class PhysiotherapyItem(models.Model):
    billing_code = models.CharField(max_length=16)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'physiotherapy_item'


class PhysiotherapyItemBatch(models.Model):
    name = models.CharField(max_length=120)
    item_id = models.IntegerField()
    quantity = models.IntegerField()
    service_centre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'physiotherapy_item_batch'


class PhysiotherapyItemsRequest(models.Model):
    patient_id = models.IntegerField(blank=True, null=True)
    requested_by = models.IntegerField(blank=True, null=True)
    received_by = models.DateTimeField(blank=True, null=True)
    delivered_by = models.DateTimeField(blank=True, null=True)
    time_entered = models.DateTimeField()
    time_received = models.DateTimeField(blank=True, null=True)
    time_delivered = models.DateTimeField(blank=True, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=9)
    service_centre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'physiotherapy_items_request'


class PhysiotherapyItemsRequestData(models.Model):
    request_id = models.IntegerField()
    item_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'physiotherapy_items_request_data'


class PhysiotherapySession(models.Model):
    booking_id = models.IntegerField()
    session_date = models.DateTimeField()
    note = models.TextField()
    noted_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'physiotherapy_session'


class Procedure(models.Model):
    name = models.CharField(max_length=100)
    category_id = models.IntegerField()
    billing_code = models.CharField(max_length=10)
    icd_code = models.CharField(max_length=10)
    description = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'procedure'


class ProcedureActionList(models.Model):
    patient_procedure_id = models.IntegerField()
    note = models.TextField()
    time_entered = models.DateTimeField()
    entered_by = models.IntegerField()
    done = models.IntegerField()
    done_by = models.IntegerField(blank=True, null=True)
    done_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'procedure_action_list'


class ProcedureAttachment(models.Model):
    patient_procedure_id = models.IntegerField()
    time_entered = models.DateTimeField()
    entered_by = models.IntegerField()
    url = models.TextField(blank=True, null=True)
    mimetype = models.CharField(max_length=70, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'procedure_attachment'


class ProcedureCategory(models.Model):
    name = models.CharField(max_length=70)

    class Meta:
        managed = False
        db_table = 'procedure_category'


class ProcedureChecklistTemplate(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'procedure_checklist_template'


class ProcedureTemplate(models.Model):
    category_id = models.IntegerField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'procedure_template'


class ProcedureTemplateCategory(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'procedure_template_category'


class ProgressNote(models.Model):
    in_patient_id = models.IntegerField(blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    note = models.TextField()
    note_type = models.CharField(max_length=2, blank=True, null=True)
    noted_by = models.CharField(max_length=16)
    entry_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'progress_note'


class PurgedDrugs(models.Model):
    drug_id = models.BigIntegerField()
    quantity = models.BigIntegerField()
    amountlost = models.FloatField()
    purgedby = models.CharField(max_length=60)
    purge_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'purged_drugs'


class RefererTemplateCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'referer_template_category'


class Referral(models.Model):
    referral_company_id = models.IntegerField()
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    specialization_id = models.IntegerField(blank=True, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referral'


class ReferralCompany(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=75, blank=True, null=True)
    bank_name = models.CharField(max_length=15, blank=True, null=True)
    account_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referral_company'


class ReferralTemplate(models.Model):
    title = models.CharField(max_length=50)
    category_id = models.IntegerField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'referral_template'


class ReferralsQueue(models.Model):
    patient_id = models.IntegerField()
    doctor_id = models.IntegerField()
    datetime = models.DateTimeField()
    acknowledged = models.IntegerField()
    note = models.TextField()
    external = models.IntegerField()
    specialization_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referrals_queue'


class Religion(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'religion'


class Resource(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'resource'


class RevenueAccount(models.Model):
    bill_source_id = models.IntegerField()
    insurance_scheme_id = models.IntegerField()
    receivable_account_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'revenue_account'


class Room(models.Model):
    name = models.CharField(max_length=30)
    ward_id = models.IntegerField()
    type_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'room'


class RoomType(models.Model):
    billing_code = models.CharField(max_length=16)
    label = models.CharField(max_length=50, blank=True, null=True)
    hospital_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'room_type'


class RoundNotification(models.Model):
    round_id = models.IntegerField()
    round = models.IntegerField()
    note = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'round_notification'


class Scan(models.Model):
    name = models.CharField(max_length=100)
    billing_code = models.CharField(max_length=10)
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'scan'


class ScanCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'scan_category'


class ServiceCentre(models.Model):
    department_id = models.IntegerField()
    cost_centre_id = models.IntegerField()
    type = models.CharField(max_length=13)
    name = models.CharField(max_length=70)
    erp_location_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_centre'


class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    access = models.IntegerField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'


class Signature(models.Model):
    patient_id = models.IntegerField(unique=True, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'signature'


class SimulationSize(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'simulation_size'


class SocioEconomicStatus(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'socio_economic_status'


class SpecialEvent(models.Model):
    patient_id = models.IntegerField()
    note = models.CharField(max_length=200)
    noted_by = models.IntegerField()
    date = models.DateTimeField()
    dismissed = models.IntegerField(blank=True, null=True)
    alert_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'special_event'


class StaffCareTeam(models.Model):
    team_id = models.IntegerField()
    staff_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'staff_care_team'
        unique_together = (('team_id', 'staff_id'),)


class StaffDirectory(models.Model):
    staffid = models.AutoField(db_column='staffId', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING)
    department_id = models.IntegerField(blank=True, null=True)
    specialization_id = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=50)
    pswd = models.CharField(max_length=100)
    profession = models.CharField(max_length=16, blank=True, null=True)
    username = models.CharField(max_length=50)
    roles = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)
    sip_user_name = models.CharField(max_length=8, blank=True, null=True)
    sip_password = models.CharField(max_length=8, blank=True, null=True)
    sip_extension = models.CharField(max_length=8, blank=True, null=True)
    folio_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff_directory'


class StaffRoles(models.Model):
    code = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff_roles'


class StaffSpecialization(models.Model):
    billing_code = models.CharField(unique=True, max_length=16)
    staff_type = models.CharField(max_length=50, blank=True, null=True)
    hospid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'staff_specialization'


class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'state'


class StiCareEntryPoint(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'sti_care_entry_point'


class StiPriorArt(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'sti_prior_art'


class StiTestMode(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        managed = False
        db_table = 'sti_test_mode'


class SystemsReview(models.Model):
    name = models.CharField(max_length=150)
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'systems_review'


class SystemsReviewCategory(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'systems_review_category'


class Test(models.Model):
    patient_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'test'


class VaccineLevels(models.Model):
    vaccine_id = models.IntegerField()
    level = models.IntegerField()
    start_index = models.IntegerField()
    end_index = models.IntegerField()
    start_age = models.IntegerField()
    end_age = models.IntegerField()
    duration = models.IntegerField()
    start_age_scale = models.CharField(max_length=5)
    end_age_scale = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'vaccine_levels'


class Vaccines(models.Model):
    billing_code = models.CharField(max_length=15)
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    default_price = models.DecimalField(max_digits=13, decimal_places=2)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vaccines'


class VaccinesBooster(models.Model):
    vaccine_id = models.IntegerField()
    start_age = models.IntegerField()
    start_age_scale = models.CharField(max_length=5)
    interval_field = models.IntegerField(db_column='interval_')  # Field renamed because it ended with '_'.
    interval_scale = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'vaccines_booster'


class VitalSign(models.Model):
    patient_id = models.IntegerField()
    read_date = models.DateTimeField()
    value = models.CharField(max_length=16)
    in_patient_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=21)
    hospital_id = models.IntegerField()
    read_by = models.IntegerField()
    encounter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vital_sign'


class Voucher(models.Model):
    code = models.CharField(unique=True, max_length=8)
    batch_id = models.IntegerField()
    date_used = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'voucher'


class VoucherBatch(models.Model):
    quantity = models.IntegerField()
    amount = models.FloatField()
    type = models.CharField(max_length=8)
    generator_id = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    date_generated = models.DateTimeField()
    expiration_date = models.DateField()
    service_centre_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'voucher_batch'


class Ward(models.Model):
    name = models.CharField(max_length=50)
    cost_centre_id = models.IntegerField()
    block_id = models.IntegerField()
    billing_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ward'


class WardRound(models.Model):
    patient_id = models.CharField(max_length=15)
    admission_id = models.IntegerField()
    frequency = models.IntegerField()
    entry_time = models.DateTimeField()
    last_round_time = models.DateTimeField(blank=True, null=True)
    end_round_time = models.DateTimeField()
    round_count = models.IntegerField()
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ward_round'
