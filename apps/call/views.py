from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from models import Call, CallFragment, INBOUND_CHECK_JOBS
from models import *
from forms import ReceiveCallForm, HandleFragmentForm
from applicant.models import ApplicantProfile

@csrf_exempt
def receive_call(request, template=None, form_class=ReceiveCallForm):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET
    form = form_class(fields)
    context = {}
    user = None

    if form.is_valid():
        profile = None
        try:
            fragment_type = OUTBOUND_WELCOME_UNKNOWN_USER
            profile = ApplicantProfile.objects.get(mobile_number=form.cleaned_data['From'])
            user = profile.user
            
            call = Call(applicant=profile, 
                        outbound=False, 
                        call_sid=form.cleaned_data['CallSid'],
                        phone_number=form.cleaned_data['From'],
                        call_type=INBOUND_CHECK_JOBS)
            
            call.save()

            fragment_type = OUTBOUND_WELCOME_KNOWN_USER
        except ApplicantProfile.DoesNotExist:
            pass
    
        fragment = CallFragment(call=call,
                                outbound=True,
                                fragment_type=fragment_type)
        fragment.save()

    context['user'] = user

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def wrong_user(request, template=None):
    context = {}
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def enter_password(request, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET
    form = HandleFragmentForm(fields)
    context = {}

    if form.is_valid():
        fragment = CallFragment(call=form.call, outbound=True, fragment_type=OUTBOUND_ENTER_PASSWORD)
        fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def verify_password(request, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET
    form = HandleFragmentForm(fields)
    context = {}

    if form.is_valid():
        fragment = CallFragment(call=form.call, outbound=False, fragment_type=INBOUND_ENTER_PASSWORD)
        fragment.save()

        fragment = CallFragment(call=form.call, outbound=True, fragment_type=OUTBOUND_UNKNOWN_FRAGMENT)
        fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

