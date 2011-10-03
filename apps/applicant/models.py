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

import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from account.models import Profile
from job.models import Criteria, Job
from signals import job_applied
    
class ApplicantProfile(Profile, Criteria):

    def __init__(self, *args, **kwargs):
        super(ApplicantProfile, self).__init__(*args, **kwargs)
        self.zip_code_old = self.zip_code

    mobile_number = models.CharField('Mobile Phone Number', 
                                     blank=False, 
                                     max_length=20, 
                                     help_text = "We need your phone number to receive job updates",
                                    )

    confirmed_phone = models.BooleanField(default=False)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    address1 = models.CharField('Address', null=True, max_length=100)
    address2 = models.CharField('Address2', null=True, max_length=100, blank=True)
    city = models.CharField('City', null=True, max_length=32)
    zip_code = models.CharField('Zip Code', null=True, blank=False, max_length=10)

    DISTANCE_OPTIONS = ((5, 'Less than 5 miles'),
                        (10, 'Less than 10 miles'),
                        (15, 'Less than 15 miles'),
                        (20, 'Less than 20 miles'),
                        (30, 'Less than 30 miles'),
                        (100, 'Less than 100 miles'))

    distance = models.IntegerField('Distance Willing to Travel for Work',
                                   choices=DISTANCE_OPTIONS,
                                   default=5)

    def __unicode__(self):
        return u'%s' % (self.mobile_number,)
    
    def save(self, *args, **kwargs):
        try:
            profile = ApplicantProfile.objects.get(id=self.id)
            if profile.resume and  profile.resume != self.resume:
                profile.resume.delete(save=False)
        except ApplicantProfile.DoesNotExist:
            pass

        if self.zip_code != self.zip_code_old:
            try:
                request = "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % (self.zip_code,)
                result = simplejson.load(urllib.urlopen(request))

                if result['status'] == 'OK':
                    self.latitude = result['results'][0]['geometry']['location']['lat']
                    self.longitude = result['results'][0]['geometry']['location']['lng']
            except:
                pass

        super(ApplicantProfile, self).save(*args, **kwargs)


    def get_login_destination(self):
        if self.is_complete():
            return reverse('applicant_dashboard')
        else:
            return reverse('applicant_profile')

    def distance_display(self):
        for distance_option in self.DISTANCE_OPTIONS:
            if distance_option[0] == self.distance:
                return distance_option[1]

        return ''

class ApplicantJob(models.Model):
    date_submitted = models.DateTimeField(default=datetime.datetime.now())
    job = models.ForeignKey(Job, related_name='applicant_job')
    applicant = models.ForeignKey(ApplicantProfile)

    APPLICATION_APPLIED = 1
    APPLICATION_REMOVED = 2

    APPLICATION_STATE_CHOICES = ((APPLICATION_APPLIED, 'Applied'),
                                 (APPLICATION_REMOVED, 'Removed application'))

    state = models.IntegerField(null=False, default=APPLICATION_APPLIED, choices=APPLICATION_STATE_CHOICES)

    send_email = models.BooleanField(default=True)

    # Send save signal to handle anything needs to happen when an application
    # is submitted    
    def save(self):
        super(ApplicantJob, self).save()
        if self.state == ApplicantJob.APPLICATION_APPLIED and self.send_email:
            job_applied.send(sender=self.__class__,
                             job=self.job, applicant=self.applicant)
