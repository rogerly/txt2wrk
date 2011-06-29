from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from account.models import Profile

class Employer(Profile):
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
    
    business_phone_number = models.CharField('Business Phone Number',
                                             blank=True,
                                             max_length=20,
                                             )
    
    business_website_url = models.CharField('Business Website URL',
                                            blank=True,
                                            max_length=100,
                                            )
    
    business_description = models.TextField('Business Description',
                                            blank=True,
                                            )
    
    def __unicode__(self):
        return u'%s' % (self.business_name,)

    def get_login_destination(self):
        return reverse('employer_profile')