from django import forms
from common.helpers import USPhoneNumberField

class ReceiveSMSForm(forms.Form):
    
    From = USPhoneNumberField(required=True)
    Body = forms.CharField(required=True)
    SmsSid = forms.CharField(required=True)
    

