import random

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from sms.models import SMS, RES_UNKNOWN, RES_NUMBER_CONFIRMATION, RES_UNSUBSCRIBE
from sms.models import ACK_NUMBER_CONFIRMATION, ACK_UNSUBSCRIBE, ACK_JOB_APPLY, ACK_UNKNOWN
from sms.forms import ReceiveSMSForm
from applicant.models import ApplicantProfile, ApplicantJob
from job.models import Job

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

    demo = False
    if 'demo' in fields:
        demo = True
    form = form_class(fields)
    context = {}
    if form.is_valid():
        profile = None
        try:
            profile = ApplicantProfile.objects.get(mobile_number=form.cleaned_data['From'], demo=demo)
            
        except ApplicantProfile.DoesNotExist:
            pass

        message = form.cleaned_data['Body']

        response, message_type = SMS.get_message_type(message, profile)
        context['response'] = response

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

        additional_context, template = handle_ack(response, message_type, profile)
        context.update(additional_context)
        
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

# Handle the specific acknowledgments to responses sent via text
# by applicants
def handle_ack(response, message_type, profile):
    # Acks are one value higher than the response
    additional_context = sms_ack_functions[message_type+1](response, profile)
    return additional_context, sms_templates[message_type+1]

# Send acknowledgment about phone number confirmation
def do_number_confirm(response, profile):
    pin = None
    if profile is not None:
        profile.confirmed_phone = True
        profile.save()
        if profile.demo:
            user = profile.user
            pin = '%d' % (random.randint(0, 8999) + 1000)
            user.set_password(pin)
            user.is_active = True
            user.save()
    return { 'pin': pin }

# Send acknowledgment about unsubscribe
def do_unsubscribe(response, profile):
    if profile is not None:
        profile.confirmed_phone = False
        profile.save()

    return {}

# Send acknowledgment about job application being sent
def do_job_apply(response, profile):
    try:
        job = Job.objects.get(job_code=response)
        applications = ApplicantJob.objects.filter(job=job, applicant=profile)
        if applications.count() == 0:
            application = ApplicantJob(job=job, applicant=profile)
            application.save()
    except Job.DoesNotExist:
        job = None

    return { 'job': job }

# Send acknowledgment about unknown message coming through
def do_unknown(response, profile):
    return {}

sms_ack_functions = {
                     ACK_NUMBER_CONFIRMATION: do_number_confirm,
                     ACK_UNSUBSCRIBE: do_unsubscribe,
                     ACK_JOB_APPLY: do_job_apply,
                     ACK_UNKNOWN: do_unknown,
                     }


