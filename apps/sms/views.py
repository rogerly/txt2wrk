from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from sms.models import SMS, RES_UNKNOWN, RES_NUMBER_CONFIRMATION, RES_UNSUBSCRIBE
from sms.models import ACK_NUMBER_CONFIRMATION, ACK_UNSUBSCRIBE, ACK_JOB_APPLY, ACK_UNKNOWN
from sms.forms import ReceiveSMSForm
from applicant.models import ApplicantProfile

sms_templates = {
                 ACK_NUMBER_CONFIRMATION: 'sms/ack/number_confirmation.html',
                 ACK_UNSUBSCRIBE: 'sms/ack/unsubscribe.html',
                 ACK_JOB_APPLY: 'sms/ack/job_apply.html',
                 ACK_UNKNOWN: 'sms/ack/unknown.html',
                 }

@csrf_exempt
def receive_sms(request, template=None, form_class=ReceiveSMSForm):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET
    form = form_class(fields)
    if form.is_valid():
        profile = None
        try:
            profile = ApplicantProfile.objects.get(mobile_number=form.cleaned_data['From'])
            
        except ApplicantProfile.DoesNotExist:
            pass

        message = form.cleaned_data['Body']

        response, message_type = SMS.get_message_type(message, profile)
        sms = SMS(applicant=profile, 
                  sent_by_us=False,
                  message=form.cleaned_data['Body'],
                  sms_sid=form.cleaned_data['SmsSid'],
                  phone_number=form.cleaned_data['From'],
                  message_type=message_type)

        sms.save()

        if profile is not None:
            if message_type == RES_NUMBER_CONFIRMATION:
                profile.confirmed_phone = True
                profile.save()
            
            if message_type == RES_UNSUBSCRIBE:
                profile.confirmed_phone = False
                profile.save()

    return render_to_response(sms_templates[message_type+1],
                              {
                               'response': response,
                               },
                              context_instance=RequestContext(request))
    