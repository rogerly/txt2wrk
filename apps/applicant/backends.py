from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.models import RegistrationProfile

from applicant.forms import ApplicantRegistrationForm
from applicant.models import ApplicantProfile

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

        auth_user = authenticate(username=username, password=password)
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
        return ('applicant_profile_setup', (), {})

    def post_activation_redirect(self, request, user):
        raise NotImplementedError
