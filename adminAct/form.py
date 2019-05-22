
from django import forms
from .models import UserAgreement


class UserAgreementForm(forms.ModelForm):

    class Meta:
        model = UserAgreement
        fields = ['notes', 'active']
        widgets = {
            'notes': forms.Textarea()
        }
