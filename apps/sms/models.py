import twilio
import re

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save 
from django.dispatch import receiver
from xml.dom import minidom

from applicant.models import ApplicantProfile
from job_recommendation.models import JobRecommendation

job_posting_id_re = re.compile(r'^[^0-9]*(\d{8})[^0-9]*$')
unsubscribe_re = re.compile(r'[Uu][Nn][Ss][Uu][Bb][Ss][Cc][Rr][Ii][Bb][Ee]')

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
        if recommendation is not None and recommendation.state == JobRecommendation.NEW_REC:
            applicant = recommendation.applicant
            job = recommendation.job
            message = u'New job posted! %s. CALL 5103943562 to hear full description or TEXT BACK with %s to send your resume and apply.' % (job.title, job.job_code,)
            SMS.send(applicant=applicant,
                     phone_number=applicant.mobile_number,
                     message=message,
                     message_type=REQ_JOB_APPLY)

    # Method used to send an SMS.  Creates a new instance of the
    # SMS model and saves it after a successful send.
    @staticmethod
    def send(applicant, phone_number, message, message_type):
        
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
            print e
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

        # If the applicant hasn't confirmed their number
        # yet, assume this is the confirmation
        if applicant is not None and not applicant.confirmed_phone:
            return 'confirmed', RES_NUMBER_CONFIRMATION

        # We have no idea what this message is about
        return 'unknown', RES_UNKNOWN
    