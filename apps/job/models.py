from random import random
from datetime import date
from django.db import models

from job import signals
from employer.models import EmployerProfile

class BaseModel(models.Model):
    name = models.CharField(max_length = 50)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.name


class Workday(BaseModel):
    pass

class Industry(BaseModel):
    pass


class Criteria(models.Model):
    
    AVAILABILITY_CHOICES = ((1, "Immediately"), 
                            (2, "Within a month"))
    
    EDUCATION_CHOICES = ((1, "High school diploma"), 
                            (2, "Associates Degree"), 
                            (3, "Bachelor's Degree"))
    
    EXPERIENCE_CHOICES = ((1, "0-1 years"), 
                            (2, "1-4 years"), 
                            (3, "4-10 years"))

    
    availability = models.IntegerField(null=False, choices=AVAILABILITY_CHOICES)
    workday = models.ManyToManyField(Workday)
    experience = models.IntegerField(null=False, choices=EXPERIENCE_CHOICES)
    education = models.IntegerField(null=False, choices=EDUCATION_CHOICES)
    industry = models.ManyToManyField(Industry)
    latitude = models.CharField(null=True, max_length=5)
    longitude = models.CharField(null=True, max_length=5)

    def is_complete(self):
        return self.availability or self.education or self.experience 
    
    class Meta:
        abstract = True


class Job(Criteria):

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
    
    date_created = models.DateField(blank=False, default=date.today)
    
    employer = models.ForeignKey(EmployerProfile, null=False, related_name='jobs')
    
    
    # Auto-create a job code if there isn't one set
    def save(self, *args, **kwargs):
        new_job = False
        if self.job_code is None or self.job_code == '':
            # This assures a valid eight digit code.  
            # Min: 10000000, Max: 99999999
            self.job_code = str(int(random() * 89999999) + 10000000)
            new_job = True
    
        super(Job, self).save()

        if new_job:
            signals.job_created.send(sender=self.__class__,
                                     job=self)

    def __unicode__(self):
        return u'%s' % (self.title,)


    