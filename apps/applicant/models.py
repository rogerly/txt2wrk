from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from account.models import Profile
from job.models import Criteria, Job
from datetime import date
from signals import job_applied
    
class ApplicantProfile(Profile, Criteria):
    
    mobile_number = models.CharField('Mobile Phone Number', 
                                     blank=False, 
                                     max_length=20, 
                                     help_text = "We need your phone number to receive job updates",
                                    )

    confirmed_phone = models.BooleanField(default=False)

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

    APPLICATION_APPLIED = 1
    APPLICATION_REMOVED = 2

    APPLICATION_STATE_CHOICES = ((APPLICATION_APPLIED, 'Applied'),
                                 (APPLICATION_REMOVED, 'Removed application'))

    state = models.IntegerField(null=False, default=APPLICATION_APPLIED, choices=APPLICATION_STATE_CHOICES)

    # Send save signal to handle anything needs to happen when an application
    # is submitted    
    def save(self):
        super(ApplicantJob, self).save()
        if self.state == ApplicantJob.APPLICATION_APPLIED:
            job_applied.send(sender=self.__class__,
                             job=self.job, applicant=self.applicant)
