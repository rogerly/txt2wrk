import urllib
try:
    import json as simplejson
except ImportError:
    import simplejson

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
    
    AVAILABILITY_CHOICES = ((None, "Please select one"),
                            (1, "Immediately"), 
                            (2, "Within a month"))
    
    EDUCATION_CHOICES = ((None, "Please select one"),
                        (1, "High school diploma"),
                            (2, 'GED'),
                            (3, "Associates Degree"),
                            (4, "Bachelor's Degree"))
    
    EXPERIENCE_CHOICES = ((None, "Please select one"),
                          (1, "0-1 years"), 
                            (2, "1-4 years"), 
                            (3, "4-10 years"))

    EMPLOYMENT_TYPE_CHOICES = ((None, "Please select one"),
                               (1, 'Full-time'),
                               (2, 'Part-time'),
                               (3, 'Temporary'))
    
    availability = models.IntegerField(null=True, choices=AVAILABILITY_CHOICES, default=None)
    workday = models.ManyToManyField(Workday)
    experience = models.IntegerField(null=True, choices=EXPERIENCE_CHOICES, default=None)
    education = models.IntegerField(null=True, choices=EDUCATION_CHOICES, default=None)
    employment_type = models.IntegerField(null=True, choices=EMPLOYMENT_TYPE_CHOICES, default=None)
    overtime = models.BooleanField(null=False, choices=((True, 'Yes'),(False, 'No')), default=True)
    industry = models.ManyToManyField(Industry)
    latitude = models.CharField(null=True, max_length=15)
    longitude = models.CharField(null=True, max_length=15)

    def is_complete(self):
        return self.availability or self.education or self.experience 

    def get_overtime_display(self):
        if self.overtime:
            return 'Yes'
        else:
            return 'No'

    def get_workday_display(self):
        val = ''
        for i, day in enumerate(self.workday.all().order_by('id')):
            val += day.name
            if i != self.workday.count()-1:
                val += ', '

        if val.startswith('Monday, Tuesday, Wednesday, Thursday, Friday'):
            if val.find('Saturday') != -1:
                if val.find('Sunday') != -1:
                    val = 'Everyday'
                else:
                    val = 'Weekdays and Saturday'
            else:
                if val.find('Sunday') != -1:
                    val = 'Weekdays and Sunday'
                else:
                    val = 'Weekdays'
        elif val.startswith('Saturday') and val.find('Sunday') != -1:
            val = 'Weekends'

        return val

    class Meta:
        abstract = True

class Job(Criteria):

    title = models.CharField('Job Title',
                             max_length=80,
                             blank=False,
                             help_text='This is the title of the job.')

    description = models.TextField('Job Description',
                                   blank=False,
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
            # This assures a valid five digit code.
            # Min: 10000, Max: 99999
            self.job_code = str(int(random() * 89999) + 10000)
            new_job = True
    
        super(Job, self).save()

        if new_job:
            signals.job_created.send(sender=self.__class__,
                                     job=self)

    def __unicode__(self):
        return u'%s' % (self.title,)

class JobLocation(models.Model):

    def __init__(self, *args, **kwargs):
        super(JobLocation, self).__init__(*args, **kwargs)
        self.business_address1_old = self.business_address1
        self.business_address2_old = self.business_address2
        self.city_old = self.city
        self.zip_code_old = self.zip_code

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

    def save(self):
        if self.business_address1 != self.business_address1_old or self.business_address2 != self.business_address2_old or self.city != self.city_old or self.zip_code != self.zip_code_old:

            try:
                location = '%s %s %s %s' % (self.business_address1, self.business_address2, self.city, self.zip_code)
                location = urllib.quote_plus(location)
                request = "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % (location,)
                result = simplejson.load(urllib.urlopen(request))

                if result['status'] == 'OK':
                    self.latitude = result['results'][0]['geometry']['location']['lat']
                    self.longitude = result['results'][0]['geometry']['location']['lng']
            except:
                pass

        super(JobLocation, self).save()