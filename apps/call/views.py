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
                call.phone_number=phone
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
    applicant = call.applicant
    context['applicant'] = applicant

    if form.is_valid():
        user = applicant.user
        context['user'] = user
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
    context['applicant'] = call.applicant

    fragment = CallFragment(call=call, outbound=False, fragment_type=CallFragment.INBOUND_ENTER_PASSWORD)
    fragment.save()

    if form.is_valid():
        if len(form.cleaned_data['Digits']) == 0:
            context['new_number'] = True
        fragment_type=CallFragment.OUTBOUND_UNKNOWN_FRAGMENT
        context['jobs'] = call.applicant.recommendations.filter(state__lte=JobRecommendation.KEPT_NEW_REC).filter(job__state=Job.JOB_OPEN)
        context['saved_jobs'] = call.applicant.recommendations.filter(state=JobRecommendation.SAVED_REC).filter(job__state=Job.JOB_OPEN)
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
def new_listings(request, job_recommendation_id=None, job_index=1, job_total=1, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form

    context['job_index'] = int(job_index)
    if job_recommendation_id is not None:
        context['job_index'] = int(job_index) + 1
    context['job_total'] = int(job_total)

    context['listing_type'] = 1
    
    call = Call.objects.get(call_sid=fields['CallSid'])
    jobs = call.applicant.recommendations.filter(state__lte=JobRecommendation.KEPT_NEW_REC).filter(job__state=Job.JOB_OPEN)
    if job_recommendation_id is not None:
        jobs = jobs.filter(id__gt=job_recommendation_id)
    jobs = jobs.order_by('id')
    context['jobs'] = jobs
    saved_jobs = call.applicant.recommendations.filter(state=JobRecommendation.SAVED_REC).filter(job__state=Job.JOB_OPEN)
    saved_jobs.order_by('id')
    context['saved_jobs'] = saved_jobs

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
def handle_listing(request, listing_type=None, job_recommendation_id=None, job_index=1, job_total=1, detail=False, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    context['listing_type'] = listing_type
    context['job_index'] = int(job_index)
    context['job_total'] = int(job_total)
    context['detail'] = detail

    call = Call.objects.get(call_sid=fields['CallSid'])
    if int(listing_type) == 1:
        jobs = call.applicant.recommendations.filter(state__lte=JobRecommendation.KEPT_NEW_REC).filter(job__state=Job.JOB_OPEN)
    else:
        jobs = call.applicant.recommendations.filter(state__lte=JobRecommendation.SAVED_REC).filter(job__state=Job.JOB_OPEN)
    if job_recommendation_id is not None:
        jobs = jobs.filter(id__gte=job_recommendation_id)
    jobs = jobs.order_by('id')
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
def handle_listen_saved(request, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    call = Call.objects.get(call_sid=fields['CallSid'])

    saved_jobs = call.applicant.recommendations.filter(state=JobRecommendation.SAVED_REC).filter(job__state=Job.JOB_OPEN)
    saved_jobs.order_by('id')
    context['saved_jobs'] = saved_jobs

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
def saved_listings(request, job_recommendation_id=None, job_index=1, job_total=1, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    
    context['job_index'] = int(job_index)
    if job_recommendation_id is not None:
        context['job_index'] = int(job_index) + 1
    context['job_total'] = int(job_total)

    context['listing_type'] = 2

    call = Call.objects.get(call_sid=fields['CallSid'])
    jobs = call.applicant.recommendations.filter(state=JobRecommendation.SAVED_REC).filter(job__state=Job.JOB_OPEN)
    if job_recommendation_id is not None:
        jobs = jobs.filter(id__gt=job_recommendation_id)
    jobs = jobs.order_by('id')
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
def listing_info(request, listing_type=None, job_recommendation_id=None, job_index=1, job_total=1, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    context['job_index'] = int(job_index)
    context['job_total'] = int(job_total)

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
def apply(request, listing_type=None, job_recommendation_id=None, job_index=1, job_total=1, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    context['job_index'] = int(job_index)
    context['job_total'] = int(job_total)
    
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
def save_listing(request, listing_type=None, job_recommendation_id=None, job_index=1, job_total=1, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    context['job_index'] = job_index
    context['job_total'] = job_total

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
def delete_listing(request, listing_type=None, job_recommendation_id=None, job_index=1, job_total=1, template=None):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = HandleFragmentForm(fields)
    context = {}
    context['form'] = form
    context['job_index'] = int(job_index)
    context['job_total'] = int(job_total)
    
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

