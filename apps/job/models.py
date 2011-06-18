from random import random

from django.conf import settings
from django.db import models

class Job(models.Model):

    title = models.CharField('Job Title',
                             max_length=80,
                             blank=False,
                             help_text='This is the title of the job.')

    description = models.CharField('Job Description',
                                   max_length=255,
                                   blank=True,
                                   help_text='This is the description of the job.')
    
    job_code = models.CharField('Job Code',
                                max_length=8,
                                blank=True,
                                db_index=True,
                                help_text='This is the job code that the applicant will use.')
    
    # Auto-create a job code if there isn't one set
    def save(self):
        if self.job_code is None or self.job_code == '':
            # This assures a valid eight digit code.  
            # Min: 10000000, Max: 99999999
            self.job_code = str(int(random() * 89999999) + 10000000)
    
        super(Job, self).save()

    