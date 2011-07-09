from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from models import Call, CallFragment, INBOUND_CHECK_JOBS
from models import *
from forms import ReceiveCallForm, HandleFragmentForm, VerifyPasswordForm, JobCodeFragmentForm, HandleDifferentPhoneForm
from applicant.models import ApplicantProfile, ApplicantJob
from job.models import Job
from job_recommendation.models import JobRecommendation

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
            fragment_type = CallFragment.OUTBOUND_WELCOME_UNKNOWN_USER
            profile = ApplicantProfile.objects.get(mobile_number=form.cleaned_data['From'])
            user = profile.user
            
            call = Call(applicant=profile, 
                        outbound=False, 
                        call_sid=form.cleaned_data['CallSid'],
                        phone_number=form.cleaned_data['From'],
                        call_type=INBOUND_CHECK_JOBS)
            
            call.save()

            fragment_type = CallFragment.OUTBOUND_WELCOME_KNOWN_USER
        except ApplicantProfile.DoesNotExist:
            call = Call(outbound=False, 
                        call_sid=form.cleaned_data['CallSid'],
                        phone_number=form.cleaned_data['From'],
                        call_type=INBOUND_CHECK_JOBS)
            
            call.save()
    
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
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET
    form = HandleDifferentPhoneForm(fields)
    context = {}
    context['form'] = form

    call = Call.objects.get(call_sid=fields['CallSid'])
    
    if form.is_valid():
        if 'Digits' in form.cleaned_data and form.cleaned_data['Digits'] != '':
            phone = form.cleaned_data['Digits']
            if len(phone) == 12:
                profile = ApplicantProfile.objects.get(mobile_number=phone)
                call.applicant=profile
                call.save()
                
                context['applicant'] = profile

        fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_ENTER_PASSWORD)
        fragment.save()

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
    context['form'] = form

    call = Call.objects.get(call_sid=fields['CallSid'])

    if form.is_valid():
        fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_ENTER_PASSWORD)
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
    form = VerifyPasswordForm(fields)
    context = {}
    context['form'] = form

    call = Call.objects.get(call_sid=fields['CallSid'])

    fragment = CallFragment(call=call, outbound=False, fragment_type=CallFragment.INBOUND_ENTER_PASSWORD)
    fragment.save()

    if form.is_valid():
        fragment_type=CallFragment.OUTBOUND_UNKNOWN_FRAGMENT
        context['jobs'] = call.applicant.recommendations.filter(state__lte=JobRecommendation.KEPT_NEW_REC)
    else:
        fragment_type=CallFragment.OUTBOUND_WRONG_PASSWORD

    fragment = CallFragment(call=call, outbound=True, fragment_type=fragment_type)
    fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def main_menu(request, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form

    call = Call.objects.get(call_sid=fields['CallSid'])
    context['jobs'] = call.applicant.recommendations.filter(state__lte=JobRecommendation.KEPT_NEW_REC)

    if form.is_valid():
        if 'Digits' in form.cleaned_data and form.cleaned_data['Digits'] != '':
            context['digits'] = form.cleaned_data['Digits']
            fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.INBOUND_MAIN_MENU_CHOICE)
            fragment.save()
        else:
            fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_MAIN_MENU)
            fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def new_listings(request, job_recommendation_id=None, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    
    call = Call.objects.get(call_sid=fields['CallSid'])
    jobs = call.applicant.recommendations.filter(state__lte=JobRecommendation.KEPT_NEW_REC)
    if job_recommendation_id is not None:
        jobs = jobs.filter(id__gt=job_recommendation_id)
    context['jobs'] = jobs

    if form.is_valid():
        if 'Digits' in form.cleaned_data and form.cleaned_data['Digits'] != '':
            context['digits'] = form.cleaned_data['Digits']
        else:
            fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_ENTER_PASSWORD)
            fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def saved_listings(request, job_recommendation_id=None, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    
    call = Call.objects.get(call_sid=fields['CallSid'])
    jobs = call.applicant.recommendations.filter(state=JobRecommendation.SAVED_REC)
    if job_recommendation_id is not None:
        jobs = jobs.filter(id__gt=job_recommendation_id)
    context['jobs'] = jobs

    if form.is_valid():
        if 'Digits' in form.cleaned_data and form.cleaned_data['Digits'] != '':
            context['digits'] = form.cleaned_data['Digits']
        else:
            fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_ENTER_PASSWORD)
            fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def listing_info(request, listing_type=None, job_recommendation_id=None, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    
    call = Call.objects.get(call_sid=fields['CallSid'])
    recommendation = JobRecommendation.objects.get(id=job_recommendation_id)
    context['recommendation'] = recommendation
    context['listing_type'] = listing_type

    if form.is_valid():
        if 'Digits' in form.cleaned_data and form.cleaned_data['Digits'] != '':
            context['digits'] = form.cleaned_data['Digits']
        else:
            fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_ENTER_PASSWORD)
            fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def apply(request, listing_type=None, job_recommendation_id=None, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    
    call = Call.objects.get(call_sid=fields['CallSid'])
    recommendation = JobRecommendation.objects.get(id=job_recommendation_id)
    applications = ApplicantJob.objects.filter(job=recommendation.job, applicant=recommendation.applicant)
    if applications.count() == 0:
        application = ApplicantJob(job=recommendation.job, applicant=recommendation.applicant)
        application.save()
    context['recommendation'] = recommendation
    context['listing_type'] = listing_type

    fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_ENTER_PASSWORD)
    fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def save_listing(request, listing_type=None, job_recommendation_id=None, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    
    call = Call.objects.get(call_sid=fields['CallSid'])
    recommendation = JobRecommendation.objects.get(id=job_recommendation_id)
    recommendation.state = JobRecommendation.SAVED_REC
    recommendation.save()
    context['recommendation'] = recommendation
    context['listing_type'] = listing_type

    fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_ENTER_PASSWORD)
    fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def delete_listing(request, listing_type=None, job_recommendation_id=None, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    
    call = Call.objects.get(call_sid=fields['CallSid'])
    recommendation = JobRecommendation.objects.get(id=job_recommendation_id)
    recommendation.state = JobRecommendation.DELETED_REC
    recommendation.save()
    context['recommendation'] = recommendation
    context['listing_type'] = listing_type

    fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_ENTER_PASSWORD)
    fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def job_code(request, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = JobCodeFragmentForm(fields)
    context = {}
    context['form'] = form

    call = Call.objects.get(call_sid=fields['CallSid'])

    if form.is_valid():
        if 'Digits' in form.cleaned_data and form.cleaned_data['Digits'] != '':
            job = Job.objects.get(job_code=form.cleaned_data['Digits'])
            recommendation = JobRecommendation.objects.filter(applicant=call.applicant).get(job=job)
            context['recommendation'] = recommendation
            context['digits'] = form.cleaned_data['Digits']
            fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.INBOUND_MAIN_MENU_CHOICE)
            fragment.save()
        else:
            fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_MAIN_MENU)
            fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def hangup(request, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form

    call = Call.objects.get(call_sid=fields['CallSid'])

    if form.is_valid():
        fragment = CallFragment(call=call, outbound=True, fragment_type=CallFragment.OUTBOUND_ENTER_PASSWORD)
        fragment.save()

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

