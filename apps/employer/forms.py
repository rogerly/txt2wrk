from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from models import EmployerProfile

from common.helpers import USPhoneNumberField, createUniqueDjangoUsername
from registration.forms import RegistrationForm

attrs_dict = { 'class': 'required' }

class EmployerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EmployerProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].initial = self.user.email
        profile = EmployerProfile.objects.get(user=self.user)
        self.fields['user'].widget = forms.HiddenInput()

        # Fields aren't required in the database, but we require them
        # when submitting the profile form
        self.fields['phone_number'].required=False
        self.fields['phone_number'].widget=forms.HiddenInput()
        self.fields['business_name'].required=True
        self.fields['business_address1'].required=True
        self.fields['city'].required=True
        self.fields['zip_code'].required=True
        self.fields['business_description'].required=True
        self.fields['business_phone_number'].required=False
        self.fields['business_website_url'].required=False

    business_phone_number = USPhoneNumberField(label = _('Business Phone'),
                                                widget=forms.TextInput(attrs=attrs_dict),
                                                required = False)
    
    password1 = forms.CharField(label=_("Password"),
                                widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                required=False)

    password2 = forms.CharField(widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label = _('Confirm Password'),
                                required=False)

    email = forms.CharField(label = _('Email Address'), required = False)

    edit_account_details = forms.CharField(widget = forms.HiddenInput(),
                                           label = '',
                                           required = False)

    class Meta:
        model = EmployerProfile

    def clean_email(self):
        if 'email' in self.cleaned_data:
            if self.cleaned_data['email'] != self.user.email:
                try:
                    existing_profile = EmployerProfile.objects.all().exclude(user=self.user).get(user__email__iexact=self.cleaned_data['email'])
                    raise forms.ValidationError(_("A user with that email already exists."))
                except EmployerProfile.DoesNotExist:
                    pass
        return self.cleaned_data['email']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

class EmployerRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['username'].widget = forms.HiddenInput()
        self.base_fields.keyOrder = ['username', 'password1', 'password2', 'email']

        try:
            self.base_fields['username'].initial = kwargs.pop('username')
        except:
            self.base_fields['username'].initial = createUniqueDjangoUsername()

        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        if 'email' in self.cleaned_data:
            try:
                profile = EmployerProfile.objects.get(user__email__iexact=self.cleaned_data['email'])
                raise forms.ValidationError(_('A user with that email already exists.'))
            except EmployerProfile.DoesNotExist:
                pass

        return self.cleaned_data['email']


    def clean(self):
        return super(EmployerRegistrationForm, self).clean()

class EmployerLoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
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
            self.user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
            if self.user is not None:
                return self.cleaned_data
            else:
                raise forms.ValidationError(_("Your password is incorrect."))
