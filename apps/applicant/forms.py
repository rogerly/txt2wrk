from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.forms import USZipCodeField

from job import models
from models import ApplicantProfile
from job.models import Industry, Workday

from common.helpers import createUniqueDjangoUsername, USPhoneNumberField, PhonePINField, CheckboxSelectMultipleDiv
from registration.forms import RegistrationForm
from django.forms.widgets import FileInput
import os
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import escape

attrs_dict = { 'class': 'required' }

class ExtensionFileField(forms.FileField):
    valid_extensions = ('.doc', '.pdf')

    def clean(self, *args, **kwargs):
        data = super(ExtensionFileField, self).clean(*args, **kwargs)
        try:
            name = data.name
            ext = os.path.splitext(name)[1]
            if ext not in self.valid_extensions:
                raise forms.ValidationError("Resume must be a pdf or a Microsoft word document")
        except:
            pass
        return data

class FileUploader(FileInput):
    input_type = 'file'
    needs_multipart_form = True

    def render(self, name, value, attrs=None):
        substitutions = dict()
        substitutions['input'] = super(FileUploader, self).render(name, value, attrs=attrs) 
        template = '%(input)s'
        
        if value and hasattr(value, "url"):
            template = "<div class='file'> %(anchor)s </div> <div class='fileinput'> %(input)s </div>" 
            filename = self.get_filename(force_unicode(value))
            substitutions['anchor'] = (u'<a href="%s">%s</a>' % (escape(value.url), filename))
        return mark_safe(template % substitutions)

    def get_filename(self, path):
        return os.path.split(path)[1]


class ApplicantProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.first_time_setup = kwargs.pop('first_time_setup')
        self.user = kwargs.pop('user')
        super(ApplicantProfileForm, self).__init__(*args, **kwargs)
        self.fields['employment_type'].label = 'Employment Preference'
        self.fields['overtime'].label = 'Can Work Overtime?'

        if self.first_time_setup:
            # Hide the phone number field if this is a first time
            # profile setup
            self.fields['mobile_number'].widget = forms.HiddenInput()
            self.fields['mobile_number'].required = False
            self.fields['first_name'].required = False
            self.fields['last_name'].required = False
        else:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

        self.fields['user'].widget = forms.HiddenInput()

    mobile_number = USPhoneNumberField(label = _("Phone Number"),
                                       widget=forms.TextInput(attrs=attrs_dict),
                                       required = True,
                                       )

    workday = forms.ModelMultipleChoiceField(
                    widget = CheckboxSelectMultipleDiv,
                    label = 'Days available to work',
                    queryset = Workday.objects.all()
    )
    
    industry = forms.ModelMultipleChoiceField(
                    widget = CheckboxSelectMultipleDiv,
                    label = 'Please select areas with the most experience',
                    queryset = Industry.objects.all().order_by('name')
    )
    
    resume = ExtensionFileField(label='Upload a New Resume', widget=FileUploader, required=False)
    zip_code = USZipCodeField(label = 'Zip Code')

    first_name = forms.CharField(label = _('First Name'), required = True)

    last_name = forms.CharField(label = _('Last Name'), required = True)

    password1 = PhonePINField(widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                              label = _('PIN (4 numbers)'), required=False)

    password2 = PhonePINField(widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                              label = _('Confirm PIN'), required=False)

    email = forms.CharField(label = _('Email'), required = False)

    class Meta:
        model = ApplicantProfile
        exclude = ('confirmed_phone', 'jobs', 'latitude', 'longitude', 'availability')
        
    def clean_mobile_number(self):
        if 'mobile_number' in self.cleaned_data:
            try:
                current_profile = ApplicantProfile.objects.get(user=self.user)
                if current_profile.mobile_number != self.cleaned_data['mobile_number']:
                    profile = ApplicantProfile.objects.get(mobile_number=self.cleaned_data['mobile_number'])
                    raise forms.ValidationError(_('This phone number already exists.'))
            except ApplicantProfile.DoesNotExist:
                pass

        return self.cleaned_data['mobile_number']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

class MobileNotificationForm(forms.Form):
    
    NOTIFICATION_CHOICES = (("1","Just call me"), 
                            ("2","Call me first, text if I do not pick up"), 
                            ("3", "Turn off notifications"))
    
    notification = forms.ChoiceField(
                    widget = forms.RadioSelect,
                    label = "Notifications",
                    choices = NOTIFICATION_CHOICES
    )

class ApplicantRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        # We dont let user enter username...we create unique guid for it
        self.base_fields['username'].widget = forms.HiddenInput()
        self.base_fields['email'].required = False
        
        try:
            self.base_fields['username'].initial = kwargs.pop('username')
        except:
            self.base_fields['username'].initial = createUniqueDjangoUsername()
            
        self.base_fields.keyOrder = ['username', 'mobile_number', 'password1', 'password2', 'first_name', 'last_name', 'email']
        super(ApplicantRegistrationForm, self).__init__(*args, **kwargs)

    mobile_number = USPhoneNumberField(label = _("Phone Number"),
                                       widget=forms.TextInput(attrs=attrs_dict),
                                       required = True,
                                       )

    first_name = forms.CharField(label = _('First Name'), required = True)

    last_name = forms.CharField(label = _('Last Name'), required = True)
    
    password1 = PhonePINField(widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                              label = _('PIN (4 numbers)'))

    password2 = PhonePINField(widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                              label = _('Confirm PIN'))

    def clean_mobile_number(self):
        if 'mobile_number' in self.cleaned_data:
            try:
                profile = ApplicantProfile.objects.get(mobile_number=self.cleaned_data['mobile_number'])
                raise forms.ValidationError(_('This phone number already exists.'))
            except ApplicantProfile.DoesNotExist:
                pass
        
        return self.cleaned_data['mobile_number']

    def clean(self):
        return super(ApplicantRegistrationForm, self).clean()

class ApplicantLoginForm(forms.Form):

    username = USPhoneNumberField(label=_("Mobile Phone Number"),
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
