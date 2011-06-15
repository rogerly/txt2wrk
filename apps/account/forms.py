import pdb

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.forms import USPhoneNumberField

from common.helpers import createUniqueDjangoUsername

from registration.forms import RegistrationForm

attrs_dict = { 'class': 'required' }

class ApplicantRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        # We dont let user enter username...we create unique guid for it
        self.base_fields['username'].widget = forms.HiddenInput()
        self.base_fields['email'].required = False
        
        try:
            self.base_fields['username'].initial = kwargs.pop('username')
        except:
            self.base_fields['username'].initial = createUniqueDjangoUsername()
#        self.base_fields['username'].initial = createUniqueDjangoUsername()
        super(ApplicantRegistrationForm, self).__init__(*args, **kwargs)
        # We dont let user enter username...we create unique guid for it
#        try:
#            print kwargs
#            self.base_fields['username'].initial = kwargs.pop('username')
#        except:
#        self.base_fields['username'].initial = createUniqueDjangoUsername()

#        super(ApplicantRegistrationForm, self).__init__()
        
#    username = forms.CharField(widget=forms.HiddenInput())

#    email = forms.EmailField(max_length=75,
#                             label=_("Email address"),
#                             required = False,
#                             )

    mobile_number = USPhoneNumberField(label = _("Mobile Phone Number"),
                                       widget=forms.TextInput(attrs=attrs_dict),
                                       required = True,
                                       )

    def clean(self):
        return super(ApplicantRegistrationForm, self).clean()
