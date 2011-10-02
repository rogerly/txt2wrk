from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import user_passes_test
from forms import EmployerProfileForm
from models import EmployerProfile
from applicant.models import ApplicantJob
from job.models import Job

@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def employer_profile(request, first_time_setup=False, template='employer/account/profile.html'):
    form = None 
    ctxt = {}
    ctxt['first_time_setup'] = first_time_setup
    if request.method == 'POST':
        form = EmployerProfileForm(data=request.POST, instance=EmployerProfile.objects.get(user=request.user), first_time_setup=first_time_setup, user=request.user)
        if form.is_valid():
            form.save()

            if 'first_name' in form.cleaned_data and form.cleaned_data['first_name'] != '':
                user = request.user
                profile = EmployerProfile.objects.get(user=user)
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.username = form.cleaned_data['username']

                if 'password1' in form.cleaned_data and form.cleaned_data['password1'] != '':
                    user.set_password(form.cleaned_data['password1'])

                user.save()
            return redirect(reverse('employer_dashboard'))
    else:
        form = EmployerProfileForm(instance=EmployerProfile.objects.get(user=request.user), first_time_setup=first_time_setup, user=request.user)
    
    ctxt['form'] = form
    ctxt['request'] = request
    return render_to_response(template, 
                              ctxt, 
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def employer_dashboard(request, template='employer/account/dashboard.html'):
    profile = EmployerProfile.objects.get(user=request.user)
    jobs = profile.jobs.all().filter(state=Job.JOB_OPEN).extra(select={'active_applicants':'SELECT COUNT(*) FROM applicant_applicantjob WHERE state=%d AND applicant_applicantjob.job_id=job_job.id' % (ApplicantJob.APPLICATION_APPLIED,),},)

    return render_to_response(template, 
                              {'profile' : profile,
                               'jobs' :jobs },
                              context_instance=RequestContext(request))
