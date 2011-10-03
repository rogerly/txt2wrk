import random
import threading

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.models import RegistrationProfile

from applicant.models import ApplicantProfile, ApplicantJob

from employer.forms import EmployerRegistrationForm
from employer.models import EmployerProfile

from job.models import Job, JobLocation
from job_recommendation.models import JobRecommendation

class EmployerBackend(object):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, account is created.

    * No verification required.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

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
        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        phone_number = ''
        if 'phone_number' in kwargs:
            phone_number = kwargs['phone_number']

        new_user = User.objects.create_user(username, email, password)
        new_user.save()
        profile, created = EmployerProfile.objects.get_or_create(user=new_user)

        profile.phone_number = phone_number

        profile.save()

        self.setup_default_data(new_user, profile)

        auth_user = authenticate(username=username, password=password)
        login(request, auth_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=auth_user,
                                     request=request)

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
        return EmployerRegistrationForm

    def post_registration_redirect(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        
        """
        return ('employer_profile_setup', (), {})

    def post_activation_redirect(self, request, user):
        raise NotImplementedError

    def setup_default_data(self, user, profile):

        if not getattr(settings, 'DEMO_ENABLED', False):
            return

        try:
            profile_to_copy = EmployerProfile.objects.get(pk=11)

            user.first_name = profile_to_copy.user.first_name
            user.last_name = profile_to_copy.user.last_name
            user.save()

            profile.business_name = profile_to_copy.business_name
            profile.business_address1 = profile_to_copy.business_address1
            profile.business_address2 = profile_to_copy.business_address2
            profile.city = profile_to_copy.city
            profile.zip_code = profile_to_copy.zip_code
            profile.business_phone_number = profile_to_copy.business_phone_number
            profile.business_website_url = profile_to_copy.business_website_url
            profile.business_description = profile_to_copy.business_description

            profile.save()

            profiles = ApplicantProfile.objects.all().filter(id__gte=20).exclude(id__gte=25)

            JobRecommendationThread(profile, profiles, profile_to_copy.jobs.all()).start()
        except EmployerProfile.DoesNotExist:
            return

class JobRecommendationThread(threading.Thread):
    def __init__(self, profile, profiles, jobs):
        self.profile = profile
        self.profiles = profiles
        self.jobs = jobs

        threading.Thread.__init__(self)

    def run(self):
        counter = 0
        for job in self.jobs:
            print job
            new_job = Job(title=job.title,
                description=job.description,
                employer=self.profile,
                availability=job.availability,
                experience=job.experience,
                education=job.education,
                employment_type=job.employment_type,
                overtime=job.overtime,
                latitude=job.latitude,
                longitude=job.longitude)
            new_job.save()
            new_job.workday=job.workday.all()
            new_job.industry=job.industry.all()
            new_job.save()

            new_location = JobLocation(business_name=job.location.business_name,
                                       business_address1=job.location.business_address1,
                                       business_address2=job.location.business_address2,
                                       city=job.location.city,
                                       zip_code=job.location.zip_code,
                                       latitude=job.location.latitude,
                                       longitude=job.location.longitude,
                                       job=new_job)
            new_location.save()

            for existing_profile in self.profiles:
                rec = JobRecommendation(job=new_job, applicant=existing_profile, state=(JobRecommendation.NEW_REC_SENT if counter > 2 else JobRecommendation.APPLIED_REC))
                rec.save()

                if counter <= 2:
                    application = ApplicantJob(job=new_job, applicant=existing_profile)
                    application.save()

                if existing_profile.id == 24 and job.id == 12:
                    application = ApplicantJob(job=new_job, applicant=existing_profile)
                    application.save()

                counter = counter + 1

            counter = 0
