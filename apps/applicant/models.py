from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from job.models import Availability, Workday, Location, Education, Experience, Industry

class ApplicantProfile(models.Model):
    mobile_number = models.CharField('Mobile Phone Number', 
                                     blank=False, 
                                     max_length=20, 
                                     help_text = "We need your phone number to receive job updates",
                                    )

    confirmed_phone = models.BooleanField(default=False)

    user = models.OneToOneField(User,
                                related_name="applicant_profile"
                                )
    
    availability = models.ForeignKey(Availability, null=False, default=1)
    workday = models.ManyToManyField(Workday)
    location = models.ForeignKey(Location, null=False, default=1)
    education = models.ForeignKey(Education, null=False, default=1)
    experience = models.ForeignKey(Experience, null=False, default=1)
    industry = models.ManyToManyField(Industry)
    
    def __unicode__(self):
        return u'%s' % (self.mobile_number,)

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    account, created = ApplicantProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
