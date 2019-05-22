from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken import views
from django.conf import settings
from django.views.static import serve


from  .views import *


urlpatterns = [
    url(r'^profiles/(?P<path>.*)$', serve, {'document_root': settings.PROFILE_PHOTOS_DIR} ),
    url(r'^create/user/$', create_patient_user),
    url(r'^patient/$', get_patient_profile), # done
    url(r'^doctors/$', get_doctors), # return all staffs that are doctors by profession
    url(r'^doctor/info/(?P<pk>[0-9]+)$', get_a_doctor),
    url(r'^specialization/$', staff_specialization), # return specializations
    url(r'^doctors/specialization/(?P<pk>[0-9]+)$', get_drs_on_specialization),
    url(r'^messaging/inbox/$', get_inbox_messages), # done
    url(r'^search/message/by/dates/$', get_inbox_messages_by_dates), # done
    url(r'^delete/inbox/item/$', delete_inbox_message),
    url(r'^mark/message/as/read/$', mark_as_read_message), # done
    url(r'^medicplus/incoming/message/$', save_message_from_medicplus), #pending
    url(r'^sent/message/from/patient/$', message_from_patient), # done
    url(r'^login/patient/$', userLogin), # done
    url(r'^logout/patient/$', sign_out), # done
    url(r'^unread/message/count/$', get_number_unread_messages), # done
    url(r'^patient/documents/$', get_patient_documents), # done
    url(r'^download/document/$', download_attachment),
    url(r'^search/documents/by/dates/$', get_doc_by_dates),
    url(r'^patient/bills/$', get_patient_bills), # done
    url(r'^bill/search/date/range/', get_patient_bills_date_range),
    url(r'^insured/bill/search/date/range/', get_patient_insured_bill_date_range),
    url(r'^outstanding/balance', get_patient_outstanding_balance), #done
    url(r'^patient/insured/bills/$', get_patient_insurance_bills), # done
    url(r'^outstanding/insured/bill', get_insurance_outstanding_balance), #done
    url(r'^patient/appointments/$', get_patient_appointment), # half done
    url(r'^search/patient/appointment/by/dates/$', get_patient_appointment_by_dates), # half done
    url(r'^patient/active/medication/$', get_patient_active_medications), # done
    url(r'^search/medication/by/dates/$', get_active_medications_by_dates), # done
    url(r'^patient/refillable/active/medication/$', get_refillables),
    url(r'^patient/medic/details/$', get_medic_details),
    url(r'^patient/allergen/$', get_patient_allergies), # done
    url(r'^search/allergen/by/dates/$', get_patient_allergies_by_dates), # done
    url(r'^update/patient/allergen/$', update_allergy_by_patient),
    url(r'^patient/allergen/count/$', get_allergen_count), # done
    url(r'^patient/open/medication/count/$', get_open_medication_count),
    url(r'^patient/labs/$', get_patient_labs),
    url(r'^search/patient/lab/by/date/$', get_patient_labs_by_range),
    url(r'^patient/lab/result/$', get_patient_lab_result),


]