from django import forms
from common.helpers import USPhoneNumberField

from applicant.models import ApplicantProfile
from models import Call

class ReceiveCallForm(forms.Form):
    
    From = USPhoneNumberField(required=True)
    CallSid = forms.CharField(required=True)

class HandleFragmentForm(forms.Form):
    
    CallSid = forms.CharField(required=True)
    Digits = forms.CharField(required=False)
    
    def clean(self):
        
        self.call = Call.objects.get(call_sid=self.cleaned_data['CallSid'])
        
        return super(HandleFragmentForm, self).clean()