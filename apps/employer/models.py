from django.conf import settings

from smtplib import SMTP

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from account.models import Profile
from applicant.signals import job_applied

class EmployerProfile(Profile):
    phone_number = models.CharField('Phone Number',
                                    blank=False,
                                    max_length=20
                                    )
    
    business_name = models.CharField('Business Name',
                                     blank=True,
                                     max_length=100,
                                     )
    
    business_address1 = models.CharField('Business Address 1',
                                         blank=True,
                                         max_length=100,
                                         )
    
    business_address2 = models.CharField('Business Address 2',
                                         blank=True,
                                         max_length=100,
                                         )
    
    city = models.CharField('City',
                            blank=True,
                            max_length=32,
                            )
    
    zip_code = models.CharField('Zip Code',
                                blank=True,
                                max_length=10,
                                )
    
    business_phone_number = models.CharField('Business Phone',
                                             blank=True,
                                             max_length=20,
                                             )
    
    business_website_url = models.CharField('Business URL',
                                            blank=True,
                                            max_length=100,
                                            )
    
    business_description = models.TextField('Business Description',
                                            blank=True,
                                            )
    
    def __unicode__(self):
        return u'%s' % (self.business_name,)

    def is_valid(self):
        return self.business_name

    def get_login_destination(self):
        if self.is_valid():
            return reverse('employer_dashboard')
        else:
            return reverse('employer_profile')

    # Contact employer upon job application
    # Once applied, email should get sent to employer notifying them
    # of a new job application
    @staticmethod
    @receiver(job_applied)
    def send_email_notification(sender, **kwargs):
        applicant = kwargs['applicant']
        job = kwargs['job']
        if applicant is not None and job is not None:
            try:
                employer = job.employer
                ctxt = {}
                ctxt['settings'] = settings
                ctxt['job'] = job
                ctxt['applicant'] = applicant
                body = render_to_string('employer/email/notification_body.txt', ctxt)

                return

                m = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                m.ehlo()
                if settings.EMAIL_USE_TLS:
                    m.starttls()
                    m.ehlo()
                m.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                m.sendmail(settings.EMAIL_HOST_USER,
                           [employer.user.email],
                           body)
                m.close()
            except:
                pass
