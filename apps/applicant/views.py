from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import user_passes_test
from forms import ApplicantProfileForm, MobileNotificationForm
from models import ApplicantProfile, ApplicantJob

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
    applicant_jobs = ApplicantJob.objects.filter(applicant=profile)
    return render_to_response(template, 
                              {'profile' : profile,
                               'applicant_jobs' : applicant_jobs },
                              context_instance=RequestContext(request))