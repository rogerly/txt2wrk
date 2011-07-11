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

class ApplicantProfileForm(forms.ModelForm):
    
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

    zip_code = USZipCodeField(label = 'Zip Code')

    class Meta:
        model = ApplicantProfile
        exclude = ('user', 'mobile_number', 'confirmed_phone', 'jobs', 'latitude', 'longitude', 'availability')
        
class MobileNotificationForm(forms.Form):
    
    NOTIFICATION_CHOICES = (("1","Just call me"), 
                            ("2","Call me first, text if I do not pick up"), 
                            ("3", "Turn off notifications"))
    
    notification = forms.ChoiceField(
                    widget = forms.RadioSelect,
                    label = "Notifications",
                    choices = NOTIFICATION_CHOICES
    )

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
