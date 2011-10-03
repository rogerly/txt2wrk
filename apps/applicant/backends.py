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


from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.models import RegistrationProfile

from applicant.forms import ApplicantRegistrationForm, DemoApplicantRegistrationForm
from applicant.models import ApplicantProfile

from job.models import Workday, Industry

from sms.models import SMS, REQ_NUMBER_CONFIRMATION

class ApplicantBackend(object):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. SMS is sent to user with verfication information.

    3. User responds to verfication, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.RegistrationProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.
    
    """
    def register(self, request, **kwargs):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        username, email, password, phone = kwargs['username'], kwargs['email'], kwargs['password1'], kwargs['mobile_number']
        first_name, last_name = kwargs['first_name'], kwargs['last_name']
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        profile, created = ApplicantProfile.objects.get_or_create(user=new_user)
        profile.mobile_number = phone

        profile.save()

        auth_user = authenticate(username=phone, password=password)
        login(request, auth_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=auth_user,
                                     request=request)

        # Send a confirmation text to the applicant's phone
        # so we can confirm that it is a real phone number
        # TODO: Move this to somewhere else so it can be
        # triggered by the user_registered signal above
        # (Otherwise, we block until the SMS request is 
        # send to Twilio.)
        sms = SMS.send(applicant=profile, 
                       phone_number=profile.mobile_number,
                       message='Welcome to txt2wrk! To verify your phone number, reply with "OK". If you did not sign up with txt2wrk, reply with "STOP" to be removed from our system.',
                       message_type=REQ_NUMBER_CONFIRMATION)

        return auth_user

    def activate(self, request, activation_key):
        raise NotImplementedError

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.
        
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_form_class(self, request):
        """
        Return the default form class used for user registration.
        
        """
        return ApplicantRegistrationForm

    def post_registration_redirect(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        
        """
        return ('applicant_profile', (), {})

    def post_activation_redirect(self, request, user):
        raise NotImplementedError

class DemoApplicantBackend(object):
    def register(self, request, **kwargs):
        username, password, phone = kwargs['username'], kwargs['password1'], kwargs['mobile_number']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = RegistrationProfile.objects.create_inactive_user(username=username,
                                                                    email='',
                                                                    password=password,
                                                                    site=site,
                                                                    send_email=False)

        profile, created = ApplicantProfile.objects.get_or_create(user=new_user)
        profile.mobile_number = phone
        profile.save()

        self.setup_default_data(new_user, profile)

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)

        # Send a confirmation text to the applicant's phone
        # so we can confirm that it is a real phone number
        # TODO: Move this to somewhere else so it can be
        # triggered by the user_registered signal above
        # (Otherwise, we block until the SMS request is
        # send to Twilio.)
        sms = SMS.send(applicant=profile,
                       phone_number=profile.mobile_number,
                       message='Welcome to txt2wrk! To verify your phone number, reply with "OK". If you did not sign up with txt2wrk, reply with "STOP" to be removed from our system.',
                       message_type=REQ_NUMBER_CONFIRMATION)

        return new_user

    def activate(self, request, activation_key):
        activated = RegistrationProfile.objects.activate_user(activation_key)

        if activated:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated,
                                        request=request)

        return activated

    def registration_allowed(self, request):
        return getattr(settings, 'DEMO_ENABLED', False)

    def get_form_class(self, request):
        return DemoApplicantRegistrationForm

    def post_registration_redirect(self, request, user):
        profile = ApplicantProfile.objects.get(user=user)
        return ('verify_phone', (profile.mobile_number,), {})

    def post_activation_redirect(self, request, user):
        return ('applicant_profile', (), {})

    def setup_default_data(self, user, profile):

        user.first_name = 'Dwight'
        user.last_name = 'Schrute'
        user.save()

        profile.address1 = '2865 Sand Hill Road'
        profile.address2 = 'Suite 101'

        profile.city = 'Menlo Park'
        profile.zip_code = '94025'

        profile.distance = 100
        profile.education = 4
        profile.employment_type = 1
        profile.overtime = True

        days = Workday.objects.all().exclude(name='Saturday').exclude(name='Sunday')
        profile.workday = days

        industry = Industry.objects.all().order_by('?')[0:5]
        profile.industry = industry

        profile.save()