from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from account.models import Profile
from job.models import Availability, Workday, Location, Education, Experience, Industry

class ApplicantProfile(Profile):
    mobile_number = models.CharField('Mobile Phone Number', 
                                     blank=False, 
                                     max_length=20, 
                                     help_text = "We need your phone number to receive job updates",
                                    )

    confirmed_phone = models.BooleanField(default=False)

    availability = models.ForeignKey(Availability, null=False, default=1)
    workday = models.ManyToManyField(Workday)
    location = models.ForeignKey(Location, null=False, default=1)
    education = models.ForeignKey(Education, null=False, default=1)
    experience = models.ForeignKey(Experience, null=False, default=1)
    industry = models.ManyToManyField(Industry)
    
    def __unicode__(self):
        return u'%s' % (self.mobile_number,)
