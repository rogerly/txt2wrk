from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

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
    
    def __unicode__(self):
        return u'%s' % (self.mobile_number,)

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    account, created = ApplicantProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
