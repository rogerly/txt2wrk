from django import forms
from django.contrib.auth import authenticate
from common.helpers import USPhoneNumberField
from django.utils.translation import ugettext_lazy as _

from applicant.models import ApplicantProfile
from models import Call

class ReceiveCallForm(forms.Form):
    
    From = USPhoneNumberField(required=True)
    CallSid = forms.CharField(required=True)

class HandleFragmentForm(forms.Form):
    
    CallSid = forms.CharField(required=True)
    Digits = forms.CharField(required=False)
    
class VerifyPasswordForm(forms.Form):
    
    CallSid = forms.CharField(required=True)
    Digits = forms.CharField(required=True)
    
    def clean(self):
        if 'Digits' in self.cleaned_data:
            call = Call.objects.get(call_sid=self.cleaned_data['CallSid'])
            profile = call.applicant
            user = authenticate(username=profile.mobile_number, password=self.cleaned_data['Digits'])
            if user is None:
                raise forms.ValidationError(_('Bad password.'))
        
        return super(VerifyPasswordForm, self).clean()