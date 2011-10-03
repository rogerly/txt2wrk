"""
                   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions.

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.
"""


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
        self.user = kwargs.pop('user')
        super(ApplicantProfileForm, self).__init__(*args, **kwargs)
        self.fields['employment_type'].label = 'Employment Preference'
        self.fields['overtime'].label = 'Can Work Overtime?'
        self.fields['name'].initial = '%s %s' % (self.user.first_name, self.user.last_name,)
        self.fields['email'].initial = self.user.email
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['experience'].required = False
        self.fields['distance'].required = False
        self.fields['distance'].widget = forms.HiddenInput()
        try:
            profile = ApplicantProfile.objects.get(user=self.user)
            self.fields['mobile_number'].initial = profile.mobile_number
        except ApplicantProfile.DoesNotExist:
            pass

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

    name = forms.CharField(label = _('Name'), required = True)

    password1 = PhonePINField(widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                              label = _('PIN (4 numbers)'), required=False)

    password2 = PhonePINField(widget = forms.PasswordInput(attrs=attrs_dict, render_value=False),
                              label = _('Confirm PIN'), required=False)

    email = forms.CharField(label = _('Email'), required = False)

    edit_account_details = forms.CharField(widget = forms.HiddenInput(),
                                           label = '',
                                           required = False)

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

class DemoApplicantRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(DemoApplicantRegistrationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    first_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    last_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    password1 = forms.CharField(widget=forms.HiddenInput(), required=False)
    password2 = forms.CharField(widget=forms.HiddenInput(), required=False)
    email = forms.CharField(widget=forms.HiddenInput(), required=False)

    mobile_number = USPhoneNumberField(label = _("Phone Number"),
                                       widget=forms.TextInput(attrs=attrs_dict),
                                       required = True,
                                       )

    def clean_mobile_number(self):
        if 'mobile_number' in self.cleaned_data:
            try:
                profile = ApplicantProfile.objects.get(mobile_number=self.cleaned_data['mobile_number'])
                raise forms.ValidationError(_('This phone number already exists.'))
            except ApplicantProfile.DoesNotExist:
                pass

        return self.cleaned_data['mobile_number']

    def clean(self):
        self.cleaned_data['username'] = createUniqueDjangoUsername()
        return super(DemoApplicantRegistrationForm, self).clean()

class ApplicantLoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if 'verify_phone' in kwargs:
            if kwargs.pop('verify_phone'):
                self.base_fields['username'].widget = forms.HiddenInput()
        super(ApplicantLoginForm, self).__init__(*args, **kwargs)

    username = USPhoneNumberField(label=_("Mobile Phone Number"),
                                  widget=forms.TextInput(attrs=attrs_dict),
                                  required=True,
                                  )

    password = forms.CharField(label=_("PIN"), widget=forms.PasswordInput(render_value=False), max_length=4)
    
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
