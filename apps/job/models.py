"""
                   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions.

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.
"""


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

    job = models.OneToOneField(Job, null=False, related_name='location')

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