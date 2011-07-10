from django.db.models import Q

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import user_passes_test
from forms import ApplicantProfileForm, MobileNotificationForm
from models import ApplicantProfile, ApplicantJob
from job.models import Job
from job_recommendation.models import JobRecommendation

@user_passes_test(lambda u: u.is_authenticated(), login_url='/applicant/login')
def applicant_profile(request, template='applicant/account/profile.html'):
    form = None 
    profile = ApplicantProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ApplicantProfileForm(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(applicant_dashboard)
    else:
        form = ApplicantProfileForm(instance=profile)
    return render_to_response(template, 
                              {'form' : form}, 
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/applicant/login')
def applicant_dashboard(request, template='applicant/account/dashboard.html'):
    profile = ApplicantProfile.objects.get(user=request.user)
    job_recommendations = JobRecommendation.objects.filter(applicant=profile).filter(Q(state=JobRecommendation.NEW_REC) | Q(state=JobRecommendation.KEPT_NEW_REC) | Q(state=JobRecommendation.SAVED_REC))
    applicant_jobs = ApplicantJob.objects.filter(applicant=profile)
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