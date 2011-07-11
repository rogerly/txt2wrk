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

    EMPLOYMENT_TYPE_CHOICES = ((1, 'Full-time'),
                               (2, 'Part-time'),
                               (3, 'Temporary'))
    
    availability = models.IntegerField(null=True, choices=AVAILABILITY_CHOICES, default=1)
    workday = models.ManyToManyField(Workday)
    experience = models.IntegerField(null=True, choices=EXPERIENCE_CHOICES, default=1)
    education = models.IntegerField(null=True, choices=EDUCATION_CHOICES, default=1)
    employment_type = models.IntegerField(null=True, choices=EMPLOYMENT_TYPE_CHOICES, default=1)
    overtime = models.BooleanField(null=False, choices=((True, 'Yes'),(False, 'No')), default=True)
    industry = models.ManyToManyField(Industry)
    latitude = models.CharField(null=True, max_length=15)
    longitude = models.CharField(null=True, max_length=15)

    def is_complete(self):
        return self.availability or self.education or self.experience 
    
    class Meta:
        abstract = True

class Job(Criteria):

    title = models.CharField('Job Title',
                             max_length=80,
                             blank=False,
                             help_text='This is the title of the job.')

    description = models.TextField('Job Description',
                                   blank=True,
                                   help_text='This is the description of the job.')
    
    job_code = models.CharField('Job Code',
                                max_length=8,
                                blank=True,
                                db_index=True,
                                help_text='This is the job code that the applicant will use.')
    
    date_created = models.DateField(blank=False, default=date.today)
    
    employer = models.ForeignKey(EmployerProfile, null=False, related_name='jobs')

    JOB_OPEN = 1
    JOB_FILLED = 2
    JOB_CLOSED = 3

    JOB_STATE_CHOICES = ((JOB_OPEN, 'Job Open'),
                         (JOB_FILLED, 'Job Position Filled'),
                         (JOB_CLOSED, 'Job Position Closed'))

    state = models.IntegerField(null=False, default=JOB_OPEN, choices=JOB_STATE_CHOICES)

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

class JobLocation(models.Model):

    business_name = models.CharField('Business Name',
                                     blank=False,
                                     max_length=100,
                                     )

    business_address1 = models.CharField('Business Address 1',
                                         blank=False,
                                         max_length=100,
                                         )

    business_address2 = models.CharField('Business Address 2',
                                         blank=True,
                                         max_length=100,
                                         )

    city = models.CharField('City',
                            blank=False,
                            max_length=32,
                            )

    zip_code = models.CharField('Zip Code',
                                blank=False,
                                max_length=10,
                                )

    latitude = models.CharField(null=True, blank=True, max_length=15)
    longitude = models.CharField(null=True, blank=True, max_length=15)

    job = models.ForeignKey(Job, null=False, related_name='location')

    def __unicode__(self):
        return u'%s - %s, %s' % (self.business_name, self.business_address1, self.city)

