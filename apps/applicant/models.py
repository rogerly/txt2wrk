import urllib
try:
    import json as simplejson
except ImportError:
    import simplejson

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

    def __init__(self, *args, **kwargs):
        super(ApplicantProfile, self).__init__(*args, **kwargs)
        self.zip_code_old = self.zip_code

    mobile_number = models.CharField('Mobile Phone Number', 
                                     blank=False, 
                                     max_length=20, 
                                     help_text = "We need your phone number to receive job updates",
                                    )

    confirmed_phone = models.BooleanField(default=False)
    resume = models.FileField(upload_to='resumes', null=True)
    zip_code = models.CharField('Zip Code', null=True, blank=False, max_length=10)

    DISTANCE_OPTIONS = ((5, 'Less than 5 miles'),
                        (10, 'Less than 10 miles'),
                        (15, 'Less than 15 miles'),
                        (20, 'Less than 20 miles'),
                        (30, 'Less than 30 miles'),
                        (100, 'Less than 100 miles'))

    distance = models.IntegerField('Distance Willing to Travel for Work',
                                   choices=DISTANCE_OPTIONS,
                                   default=5)

    def __unicode__(self):
        return u'%s' % (self.mobile_number,)
    
    def save(self, *args, **kwargs):
        try:
            profile = ApplicantProfile.objects.get(id=self.id)
            if profile.resume and  profile.resume != self.resume:
                profile.resume.delete(save=False)
        except ApplicantProfile.DoesNotExist:
            pass

        if self.zip_code != self.zip_code_old:
            try:
                request = "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % (self.zip_code,)
                result = simplejson.load(urllib.urlopen(request))

                if result['status'] == 'OK':
                    self.latitude = result['results'][0]['geometry']['location']['lat']
                    self.longitude = result['results'][0]['geometry']['location']['lng']
            except:
                pass

        super(ApplicantProfile, self).save(*args, **kwargs)


    def get_login_destination(self):
        if self.is_complete():
            return reverse('applicant_dashboard')
        else:
            return reverse('applicant_profile')

    def distance_display(self):
        for distance_option in self.DISTANCE_OPTIONS:
            if distance_option[0] == self.distance:
                return distance_option[1]

        return ''

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
