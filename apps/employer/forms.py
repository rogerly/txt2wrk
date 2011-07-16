from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import EmployerProfile

from common.helpers import USPhoneNumberField
from registration.forms import RegistrationForm

attrs_dict = { 'class': 'required' }

class EmployerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.first_time_setup = kwargs.pop('first_time_setup')
        self.user = kwargs.pop('user')
        super(EmployerProfileForm, self).__init__(*args, **kwargs)

        if self.first_time_setup:
            # Hide the phone number field if this is a first time
            # profile setup
            self.fields['phone_number'].widget = forms.HiddenInput()
            self.fields['phone_number'].required = False
            self.fields['first_name'].required = False
            self.fields['last_name'].required = False
            self.fields['username'].required = False
        else:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            profile = EmployerProfile.objects.get(user=self.user)
            if profile.demo:
                self.fields['username'].initial = self.user.username[:-5]
            else:
                self.fields['username'].initial = self.user.username

        self.fields['user'].widget = forms.HiddenInput()

        # Fields aren't required in the database, but we require them
        # when submitting the profile form
        self.fields['business_name'].required=True
        self.fields['business_address1'].required=True
        self.fields['city'].required=True
        self.fields['zip_code'].required=True
        self.fields['business_description'].required=True
        self.fields['business_phone_number'].required=True
        self.fields['business_website_url'].required=True

    business_phone_number = USPhoneNumberField(label = _('Business Phone'),
                                                widget=forms.TextInput(attrs=attrs_dict),
                                                required = True)
    
    phone_number = USPhoneNumberField(label = _("Phone Number"),
                                       widget=forms.TextInput(attrs=attrs_dict),
                                       required = True,
                                       )

    username = forms.CharField(label=_("Username"),
                               widget=forms.TextInput(attrs=attrs_dict),
                               required=True,
                               )

    first_name = forms.CharField(label = _('First Name'), required = True)

    last_name = forms.CharField(label = _('Last Name'), required = True)

    password1 = forms.CharField(label=_("Password"),
                                widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                required=False)

    password2 = forms.CharField(widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label = _('Confirm Password'),
                                required=False)

    email = forms.CharField(label = _('Email Address'), required = False)

    class Meta:
        model = EmployerProfile
        exclude = ('demo',)

    def clean_username(self):
        try:
            if 'username' in self.cleaned_data:
                profile = EmployerProfile.objects.get(user=self.user)
                if '%s%s' % (self.cleaned_data['username'], '_demo' if profile.demo else '') != self.user.username:
                    user = User.objects.get(username__iexact='%s%s' % (self.cleaned_data['username'], '_demo' if profile.demo else ''))
                    raise forms.ValidationError(_("A user with that username already exists."))
        except User.DoesNotExist:
            pass

        return self.cleaned_data['username']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

class EmployerRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        self.demo = kwargs.pop('demo')
        self.base_fields.keyOrder = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number']
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)

    phone_number = USPhoneNumberField(label = _("Phone Number"),
                                       widget=forms.TextInput(attrs=attrs_dict),
                                       required = True,
                                       )

    first_name = forms.CharField(label = _('First Name'), required = True)

    last_name = forms.CharField(label = _('Last Name'), required = True)

    def clean_username(self):
        try:
            if 'username' in self.cleaned_data:
                user = User.objects.get(username__iexact='%s%s' % (self.cleaned_data['username'], '_demo' if self.demo else '',))
                raise forms.ValidationError(_("A user with that username already exists."))
        except User.DoesNotExist:
            pass

        return self.cleaned_data['username']

    def clean(self):
        return super(EmployerRegistrationForm, self).clean()

class EmployerLoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.demo = kwargs.pop('demo')
        super(EmployerLoginForm, self).__init__(*args, **kwargs)

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
            self.user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'], demo=self.demo)
            if self.user is not None:
                return self.cleaned_data
            else:
                raise forms.ValidationError(_("Your password is incorrect."))
