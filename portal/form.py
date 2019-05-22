
from django import forms

from mobiles.models import FakePatient, FakeContact


class FakePatientForm(forms.ModelForm):
    class Meta:
        model = FakePatient
        exclude = ['district']
        widgets = {
            'address': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'next_kin_address': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'work_address': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'res_address': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
        }


class FakeContactForm(forms.ModelForm):
    class Meta:
        model = FakeContact
        exclude = ['fake_patient']



class CaptchaForm(forms.ModelForm):
    pass