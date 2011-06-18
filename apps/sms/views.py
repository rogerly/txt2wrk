from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from sms.models import SMS
from sms.forms import ReceiveSMSForm
from applicant.models import ApplicantProfile

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
        sms = SMS(applicant=profile, 
                  sent_by_us=False,
                  message=form.cleaned_data['Body'],
                  sms_sid=form.cleaned_data['SmsSid'],
                  phone_number=form.cleaned_data['From'])
        sms.save()
    return render_to_response(template,
                              {},
                              context_instance=RequestContext(request))
    