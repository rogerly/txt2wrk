from random import random

from django.db import models

from job import signals

class BaseModel(models.Model):
    name = models.CharField(max_length = 50)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.name

class Availability(BaseModel):
    pass

class Workday(BaseModel):
    pass

class Location(BaseModel):
    pass

class Education(BaseModel):
    pass

class Experience(BaseModel):
    pass

class Industry(BaseModel):
    pass

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
    availability = models.ForeignKey(Availability, null=False, default=1)
    workday = models.ManyToManyField(Workday)
    location = models.ForeignKey(Location, null=False, default=1)
    education = models.ForeignKey(Education, null=False, default=1)
    experience = models.ForeignKey(Experience, null=False, default=1)
    industry = models.ManyToManyField(Industry)
    
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

    