import settings
import twilio

from django.db import models
from xml.dom import minidom

from applicant.models import ApplicantProfile


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
    
    # Method used to send an SMS.  Assumes a valid instance
    # of this model with the applicant, message and phone_number
    # set.  
    # TODO: Could make this a static method that takes in those
    # parameters. Should revisit 
    def send(self):
        
        # This is sent by us
        self.sent_by_us = True

        # Account object to send messages to Twilio
        account = twilio.Account(settings.ACCOUNT_SID, settings.ACCOUNT_TOKEN)
        
        # Data for the message
        sms_msg = {
                   'From': settings.CALLER_ID,
                   'To': self.phone_number,
                   'Body': self.message,
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
                self.sms_sid = sms_sid.firstChild.data

        except Exception, e:
            print e
            return False
            
        return True
    
    