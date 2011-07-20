from django.conf import settings

from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
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
                html_body = render_to_string('employer/email/notification_body.html', ctxt)
                subject = render_to_string('employer/email/notification_subject.txt', ctxt)

                email = EmailMultiAlternatives(subject, body, 'txt2wrk Notifications <%s>' % (settings.EMAIL_HOST_USER,), [job.employer.user.email])
                email.attach_alternative(html_body, 'text/html')
                email.send()
            except:
                pass
