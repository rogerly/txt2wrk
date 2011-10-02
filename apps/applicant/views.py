from django.db.models import Q

from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import user_passes_test
from forms import ApplicantProfileForm, MobileNotificationForm, ApplicantLoginForm
from models import ApplicantProfile, ApplicantJob
from job.models import Job
from job_recommendation.models import JobRecommendation

def verify_phone(request, template=None, mobile_number=None):
    ctxt = {}
    ctxt['mobile_number'] = mobile_number
    try:
        profile = ApplicantProfile.objects.get(mobile_number=mobile_number)
    except ApplicantProfile.DoesNotExist:
        return HttpResponseNotFound

    login_form = ApplicantLoginForm(initial={'username':mobile_number}, demo=profile.demo, verify_phone=True)
    ctxt['login_form'] = login_form
    return render_to_response(template, ctxt, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/applicant/login')
def applicant_profile(request, demo=False, template='applicant/account/profile.html'):
    form = None 
    ctxt = {}
    profile = ApplicantProfile.objects.get(user=request.user)
    ctxt['profile'] = profile
    if request.method == 'POST':
        form = ApplicantProfileForm(data=request.POST, files=request.FILES, instance=profile, user=request.user)
        print form.errors
        if form.is_valid():
            form.save()

            if 'name' in form.cleaned_data and form.cleaned_data['name'] != '':
                user = request.user

                name_parts = form.cleaned_data['name'].partition(' ')
                user.first_name = name_parts[0]
                user.last_name = name_parts[2]
                user.email = form.cleaned_data['email']

                if 'password1' in form.cleaned_data and form.cleaned_data['password1'] != '':
                    user.set_password(form.cleaned_data['password1'])

                user.save()

            return redirect(reverse('applicant_dashboard'))
    else:
        form = ApplicantProfileForm(instance=profile, user=request.user)

    ctxt['form'] = form
    return render_to_response(template,
                              ctxt,
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/applicant/login')
def applicant_dashboard(request, template='applicant/account/dashboard.html'):
    profile = ApplicantProfile.objects.get(user=request.user)
    job_recommendations = JobRecommendation.objects.filter(applicant=profile).filter(job__state=Job.JOB_OPEN).exclude(state=JobRecommendation.INVALID_REC)
    applicant_jobs = ApplicantJob.objects.filter(applicant=profile, state=ApplicantJob.APPLICATION_APPLIED).filter(job__state=Job.JOB_OPEN)
    return render_to_response(template, 
                              {'profile' : profile,
                               'applicant_jobs' : applicant_jobs,
                               'job_recommendations': job_recommendations, },
                              context_instance=RequestContext(request))


def apply(request, job_code=None, redirect_url=None):

    profile = ApplicantProfile.objects.get(user=request.user)
    try:
        job = Job.objects.get(job_code = job_code)
        application = ApplicantJob(applicant=profile, job=job)
        application.save()
    except Job.DoesNotExist:
        pass

    return redirect(reverse(redirect_url))

def remove_job(request, job_code=None, redirect_url=None):
    profile = ApplicantProfile.objects.get(user=request.user)
    try:
        job = Job.objects.get(job_code = job_code)
        recommendation = JobRecommendation.objects.get(job=job, applicant=profile)
        recommendation.state = JobRecommendation.DELETED_REC
        recommendation.save()
        try:
            application = ApplicantJob.objects.get(job=job, applicant=profile)
            application.state = 2
            application.save()
        except ApplicantJob.DoesNotExist:
            pass
    except Job.DoesNotExist, JobRecommendation.DoesNotExist:
        pass

    return redirect(reverse(redirect_url))

def view_profile(request, applicant_id=None, template='applicant/profile/profile.html'):
    applicant = ApplicantProfile.objects.get(pk=applicant_id)
    return render_to_response(template,
                              {'applicant':applicant},
                              context_instance=RequestContext(request))

