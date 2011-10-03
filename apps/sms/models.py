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


import twilio
import re

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save 
from django.dispatch import receiver
from xml.dom import minidom

from applicant.models import ApplicantProfile
from job_recommendation.models import JobRecommendation

job_posting_id_re = re.compile(r'^[^0-9]*(\d{5})[^0-9]*$')
unsubscribe_re = re.compile(r'[Uu][Nn][Ss][Uu][Bb][Ss][Cc][Rr][Ii][Bb][Ee]')
stop_re = re.compile(r'[Ss][Tt][Oo][Pp]')

REQ_NUMBER_CONFIRMATION=0
RES_NUMBER_CONFIRMATION=1
ACK_NUMBER_CONFIRMATION=2

RES_UNSUBSCRIBE=11
ACK_UNSUBSCRIBE=12

REQ_JOB_APPLY=20
RES_JOB_APPLY=21
ACK_JOB_APPLY=22

RES_UNKNOWN=101
ACK_UNKNOWN=102

MESSAGE_TYPE_TEXT = {
                     REQ_NUMBER_CONFIRMATION: 'Request phone confirmation',
                     RES_NUMBER_CONFIRMATION: 'Applicant confirmed phone number',
                     ACK_NUMBER_CONFIRMATION: 'Acknowledgment of number confirmation',
                     RES_UNSUBSCRIBE: 'Request to stop receiving texts',
                     ACK_UNSUBSCRIBE: 'Acknowledgment of unsubscribe',
                     REQ_JOB_APPLY: 'Sent job posting to applicant',
                     RES_JOB_APPLY: 'Applicant applied to job posting',
                     ACK_JOB_APPLY: 'Acknowledgment of job application',
                     RES_UNKNOWN: 'Unknown message',
                     ACK_UNKNOWN: 'Acknowledgment of unknown message',
                     }

class SMS(models.Model):
    # The applicant associated with this SMS
    # It is possible that this isn't tied
    # to an applicant, since pretty much
    # anyone could text us.  We'll still track
    # these "errant" SMS messages, just in case
    applicant = models.ForeignKey(ApplicantProfile,
                                  null=True,
                                  related_name='sms_messages',
                                  verbose_name='SMS Messages',
                                  help_text='SMS Messages sent/received')

    # Date/time the message was processed
    action_date = models.DateTimeField(auto_now_add=True)
    
    # Whether this was sent from us.  
    # True means sent from Txt2Wrk to user
    # False means sent from user to Txt2Wrk
    sent_by_us = models.BooleanField('SMS Sent from system', default=True)

    # The body of the SMS text
    message = models.CharField('Message body',
                               max_length=160,
                               blank=True,
                               help_text='This is the body of the message')

    # A Twilio ID that references this SMS message
    # We can use this information to look up the 
    # message on Twilio's side via the API
    sms_sid = models.CharField('Twilio SMS ID',
                               max_length=34,
                               blank=True,
                               help_text='This is an ID that can be used to look up SMS on Twilio\'s side')
    
    # Keep track of the phone number that sent/received
    # this message.  Over time, if a user changes their
    # phone number, it could be useful to know that
    # this was sent from an older number, etc.
    phone_number = models.CharField('Remote phone number',
                                    max_length=20,
                                    blank=False,
                                    help_text='This is the phone number of the applicant message was sent to/received from')
    
    message_type = models.IntegerField('Message type',
                                       default = ACK_UNKNOWN,
                                       choices = (
                                                  (REQ_NUMBER_CONFIRMATION, MESSAGE_TYPE_TEXT[REQ_NUMBER_CONFIRMATION]),
                                                  (RES_NUMBER_CONFIRMATION, MESSAGE_TYPE_TEXT[RES_NUMBER_CONFIRMATION]),
                                                  (ACK_NUMBER_CONFIRMATION, MESSAGE_TYPE_TEXT[ACK_NUMBER_CONFIRMATION]),
                                                  (RES_UNSUBSCRIBE, MESSAGE_TYPE_TEXT[RES_UNSUBSCRIBE]),
                                                  (ACK_UNSUBSCRIBE, MESSAGE_TYPE_TEXT[ACK_UNSUBSCRIBE]),
                                                  (REQ_JOB_APPLY, MESSAGE_TYPE_TEXT[REQ_JOB_APPLY]),
                                                  (RES_JOB_APPLY, MESSAGE_TYPE_TEXT[RES_JOB_APPLY]),
                                                  (ACK_JOB_APPLY, MESSAGE_TYPE_TEXT[ACK_JOB_APPLY]),
                                                  (RES_UNKNOWN, MESSAGE_TYPE_TEXT[RES_UNKNOWN]),
                                                  (ACK_UNKNOWN, MESSAGE_TYPE_TEXT[ACK_UNKNOWN]),
                                                  )
                                       )
    
    def __unicode__(self):
        return u'%s - %s' % (self.phone_number, MESSAGE_TYPE_TEXT[self.message_type],)

    @staticmethod
    @receiver(pre_save, sender=JobRecommendation)
    def send_new_recommendation(sender, **kwargs):
        recommendation = kwargs['instance']
        if recommendation is not None and recommendation.state == JobRecommendation.NEW_REC_NOT_SENT:
            applicant = recommendation.applicant
            if applicant.confirmed_phone:
                job = recommendation.job
                message = u'New job! %s at %s. CALL %s to hear full description or TEXT BACK %s to submit application.' % (job.title,job.location.business_name,settings.CALLER_ID,job.job_code,)
                SMS.send(applicant=applicant,
                         phone_number=applicant.mobile_number,
                         message=message,
                         message_type=REQ_JOB_APPLY)
                recommendation.state = JobRecommendation.NEW_REC_SENT
                recommendation.save()

    # Method used to send an SMS.  Creates a new instance of the
    # SMS model and saves it after a successful send.
    @staticmethod
    def send(applicant, phone_number, message, message_type):

        if not applicant.confirmed_phone and message_type != REQ_NUMBER_CONFIRMATION:
            return None

        sms = SMS(applicant=applicant,
                  message=message,
                  sent_by_us=True,
                  phone_number=phone_number,
                  message_type=message_type)
        
        # Account object to send messages to Twilio
        account = twilio.Account(settings.ACCOUNT_SID, settings.ACCOUNT_TOKEN)
        
        # Data for the message
        sms_msg = {
                   'From': settings.CALLER_ID,
                   'To': phone_number,
                   'Body': message,
                   }
        
        try:
            # Send request to send SMS to Twilio
            response = account.request('/%s/Accounts/%s/SMS/Messages' % (settings.API_VERSION, settings.ACCOUNT_SID),
                                       'POST', sms_msg)
            
            # Parse the TwiML response (XML-based)
            dom = minidom.parseString(response)
            
            # There is only one <Sid> object, but
            # getElementsByTagName returns a list
            sms_sids = dom.getElementsByTagName('Sid')

            # Bad state, could probably log this
            if not sms_sids:
                return False
            
            # This will walk through "all" <Sid>
            # elements, but in reality there is only one
            for sms_sid in sms_sids:
                # Save the sms_sid for this SMS message
                sms.sms_sid = sms_sid.firstChild.data

        except Exception, e:
            return None

        sms.save()
        return sms
    
    @staticmethod
    def get_message_type(message, applicant):
        
        # If we find a job posting ID (exactly 8 consecutive
        # digits.  Any random stuff before/after is fine
        # but we should now allow more or fewer numbers
        match_job = job_posting_id_re.search(message)
        if match_job is not None:
            return u'%s' % (match_job.group(1)), RES_JOB_APPLY
        
        # Search for the string "unsubscribe".  Can
        # be in any case.  
        # TODO: Is the regex better or worse than a 
        # non-case-sensitive string comparison?
        match_unsub = unsubscribe_re.search(message)
        if match_unsub is not None:
            return 'unsubscribe', RES_UNSUBSCRIBE

        match_stop = stop_re.search(message)
        if match_stop is not None:
            return 'unsubscribe', RES_UNSUBSCRIBE

        # If the applicant hasn't confirmed their number
        # yet, assume this is the confirmation
        if applicant is not None and not applicant.confirmed_phone:
            return 'confirmed', RES_NUMBER_CONFIRMATION

        # We have no idea what this message is about
        return 'unknown', RES_UNKNOWN
    