from django import forms
from common.helpers import USPhoneNumberField

from applicant.models import ApplicantProfile

class ReceiveCallForm(forms.Form):
    
    From = USPhoneNumberField(required=True)
    CallSid = forms.CharField(required=True)
