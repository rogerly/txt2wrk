import twilio
import re

from django.conf import settings
from django.db import models
from xml.dom import minidom

from applicant.models import ApplicantProfile
from job_recommendation.models import JobRecommendation

job_posting_id_re = re.compile(r'^[^0-9]*(\d{8})[^0-9]*$')

INBOUND_CHECK_JOBS=1
OUTBOUND_NOTIFY_JOBS=2
INBOUND_UNKNOWN=101
OUTBOUND_UNKNOWN=102

CALL_TYPE_TEXT = {
                  INBOUND_CHECK_JOBS: 'Inbound call to check job listings',
                  OUTBOUND_NOTIFY_JOBS: 'Outbound call to notify applicant of new postings',
                  INBOUND_UNKNOWN: 'Unknown inbound call',
                  OUTBOUND_UNKNOWN: 'Unknown outbound call [should never happen]',
                  }

class Call(models.Model):
    
    applicant = models.ForeignKey(ApplicantProfile,
                                  null=True,
                                  related_name='calls',
                                  verbose_name='Calls',
                                  help_text='Calls sent/received')
    
    start_time = models.DateTimeField(auto_now_add=True)
    
    outbound = models.BooleanField('Call sent from system', default=True)
    
    call_sid = models.CharField('Twilio Call ID',
                                max_length=64,
                                blank=True,
                                help_text='This is an ID that can be used to look up a Call on Twilio')
    
    phone_number = models.CharField('Remote phone number',
                                    max_length=20,
                                    blank=False,
                                    help_text='This is the phone number of the applicant\'s phone')
    
    call_type = models.IntegerField('Call type',
                                    default = INBOUND_UNKNOWN,
                                    choices = (
                                               (INBOUND_CHECK_JOBS, CALL_TYPE_TEXT[INBOUND_CHECK_JOBS]),
                                               (OUTBOUND_NOTIFY_JOBS, CALL_TYPE_TEXT[OUTBOUND_NOTIFY_JOBS]),
                                               (INBOUND_UNKNOWN, CALL_TYPE_TEXT[INBOUND_UNKNOWN]),
                                               (OUTBOUND_UNKNOWN, CALL_TYPE_TEXT[OUTBOUND_UNKNOWN]),
                                               )
                                    )
    
    def __unicode__(self):
        return u'%s - %s' % (self.phone_number, CALL_TYPE_TEXT[self.call_type],)

OUTBOUND_WELCOME_KNOWN_USER=1
OUTBOUND_WELCOME_UNKNOWN_USER=2

INBOUND_WRONG_USER=11
OUTBOUND_ENTER_PHONE_NUMBER=12
INBOUND_ENTER_PHONE_NUMBER=13
OUTBOUND_WRONG_PHONE_NUMBER=14

OUTBOUND_ENTER_PASSWORD=21
INBOUND_ENTER_PASSWORD=22
OUTBOUND_WRONG_PASSWORD=23

INBOUND_UNKNOWN_FRAGMENT=1001
OUTBOUND_UNKNOWN_FRAGMENT=1002

FRAGMENT_TYPE_TEXT = {
                      OUTBOUND_WELCOME_KNOWN_USER: 'Welcome message to recognized caller',
                      OUTBOUND_WELCOME_UNKNOWN_USER: 'Welcome message to unrecognized caller',
                      INBOUND_WRONG_USER: 'Caller trying to change to different applicant',
                      OUTBOUND_ENTER_PHONE_NUMBER: 'Ask for phone number of applicant',
                      INBOUND_ENTER_PHONE_NUMBER: 'Caller sending phone number for applicant',
                      OUTBOUND_WRONG_PHONE_NUMBER: 'Notify caller of invalid/unknown phone number',
                      OUTBOUND_ENTER_PASSWORD: 'Ask for password',
                      INBOUND_ENTER_PASSWORD: 'Caller sending password',
                      OUTBOUND_WRONG_PASSWORD: 'Notify caller of invalid password',
                      INBOUND_UNKNOWN_FRAGMENT: 'Unknown inbound message',
                      OUTBOUND_UNKNOWN_FRAGMENT: 'Unknown outbound message',
                      }

class CallFragment(models.Model):
    call = models.ForeignKey(Call,
                             null=True,
                             related_name='fragments',
                             verbose_name='Fragments',
                             help_text='Call fragment')
    
    outbound = models.BooleanField('Fragment sent from system', default=True)
    
    fragment_type = models.IntegerField('Fragment type',
                                        default = INBOUND_UNKNOWN_FRAGMENT,
                                        choices = (
                                                   (OUTBOUND_WELCOME_KNOWN_USER, FRAGMENT_TYPE_TEXT[OUTBOUND_WELCOME_KNOWN_USER]),
                                                   (OUTBOUND_WELCOME_UNKNOWN_USER, FRAGMENT_TYPE_TEXT[OUTBOUND_WELCOME_UNKNOWN_USER]),
                                                   (INBOUND_WRONG_USER, FRAGMENT_TYPE_TEXT[INBOUND_WRONG_USER]),
                                                   (OUTBOUND_ENTER_PHONE_NUMBER, FRAGMENT_TYPE_TEXT[OUTBOUND_ENTER_PHONE_NUMBER]),
                                                   (INBOUND_ENTER_PHONE_NUMBER, FRAGMENT_TYPE_TEXT[INBOUND_ENTER_PHONE_NUMBER]),
                                                   (OUTBOUND_WRONG_PHONE_NUMBER, FRAGMENT_TYPE_TEXT[OUTBOUND_WRONG_PHONE_NUMBER]),
                                                   (OUTBOUND_ENTER_PASSWORD, FRAGMENT_TYPE_TEXT[OUTBOUND_ENTER_PASSWORD]),
                                                   (INBOUND_ENTER_PASSWORD, FRAGMENT_TYPE_TEXT[INBOUND_ENTER_PASSWORD]),
                                                   (OUTBOUND_WRONG_PASSWORD, FRAGMENT_TYPE_TEXT[OUTBOUND_WRONG_PASSWORD]),
                                                   (INBOUND_UNKNOWN_FRAGMENT, FRAGMENT_TYPE_TEXT[INBOUND_UNKNOWN_FRAGMENT]),
                                                   (OUTBOUND_UNKNOWN_FRAGMENT, FRAGMENT_TYPE_TEXT[OUTBOUND_UNKNOWN_FRAGMENT]),
                                                   )
                                        )
