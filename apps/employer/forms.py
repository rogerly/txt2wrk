from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import EmployerProfile

from common.helpers import USPhoneNumberField
from registration.forms import RegistrationForm

class EmployerProfileForm(forms.ModelForm):
    
    class Meta:
        model = EmployerProfile
        exclude = ('user')
        
attrs_dict = { 'class': 'required' }

class EmployerRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        self.base_fields.keyOrder = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number']
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)

    phone_number = USPhoneNumberField(label = _("Phone Number"),
                                       widget=forms.TextInput(attrs=attrs_dict),
                                       required = True,
                                       )

    first_name = forms.CharField(label = _('First Name'), required = True)

    last_name = forms.CharField(label = _('Last Name'), required = True)

    def clean(self):
        return super(EmployerRegistrationForm, self).clean()

class EmployerLoginForm(forms.Form):

    username = forms.CharField(label=_("Username"),
                               widget=forms.TextInput(attrs=attrs_dict),
                               required=True,
                               )

    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False))
    
    user = None
    
    def clean_username(self):
        return self.cleaned_data['username']
    
    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            self.user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
            if self.user is not None:
                return self.cleaned_data
            else:
                raise forms.ValidationError(_("Your password is incorrect."))
