from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from account.models import Profile
from job.models import Criteria, Job
from datetime import date

    
class ApplicantProfile(Profile, Criteria):
    
    mobile_number = models.CharField('Mobile Phone Number', 
                                     blank=False, 
                                     max_length=20, 
                                     help_text = "We need your phone number to receive job updates",
                                    )

    confirmed_phone = models.BooleanField(default=False)

    jobs = models.ManyToManyField(Job, related_name='applicants')

    def __unicode__(self):
        return u'%s' % (self.mobile_number,)


    def get_login_destination(self):
        if self.is_complete():
            return reverse('applicant_dashboard')
        else:
            return reverse('applicant_profile')

class ApplicantJob(models.Model):
    date_submitted = models.DateField(default=date.today())
    job = models.ForeignKey(Job, related_name='applicant_job')
    applicant = models.ForeignKey(ApplicantProfile)
    