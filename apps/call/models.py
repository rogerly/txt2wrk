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

class CallFragment(models.Model):
    call = models.ForeignKey(Call,
                             null=True,
                             related_name='fragments',
                             verbose_name='Fragments',
                             help_text='Call fragment')
    
    
    