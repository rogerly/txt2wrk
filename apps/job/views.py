'''
Created on Jun 18, 2011

@author: Jon
'''

from models import Job
from forms import JobForm
from employer.models import EmployerProfile
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext

@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def manage_job(request, job_code = None, template = 'job/view_job.html'):
    if request.method == 'GET' and job_code:
        profile = EmployerProfile.objects.get(user=request.user)
        job = Job.objects.get(job_code=job_code)
        return render_to_response(template,
                                  {'job' : job, 
                                   'profile' : profile,
                                   'applicants' : job.applicants.all() }, 
                                  context_instance = RequestContext(request))
    return redirect(create_job)


def view_job(request, job_code = None, template = 'employer/view_job.html'):
    if request.method == 'GET' and job_code:
        job = Job.objects.get(job_code=job_code)
        return render_to_response(template,
                                  {'job' : job}, 
                                  context_instance = RequestContext(request))
    return redirect(create_job)


@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def edit_job(request, job_code, template = 'job/edit_job.html'):
    form = None 
    job = Job.objects.get(job_code=job_code)
    
    ''' Check if user has permission to edit this job '''
    if job.employer.user != request.user:
        redirect(view_job, job_code)  
    
    
    if request.method == 'POST':        
        form = JobForm(data=request.POST, user=request.user, instance=job)

        if form.is_valid():
            job = form.save()
            return redirect(view_job, job_code)
    else:
        form = JobForm(instance=job, user=request.user)
    return render_to_response(template, 
                              {'form' : form, 
                               'job_code' : job_code}, 
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def create_job(request, job_code=None, template = 'job/edit_job.html'):
    jobForm = None 
    
    if request.method == 'POST':        
        jobForm = JobForm(data=request.POST, user=request.user)
        if jobForm.is_valid():
            job = jobForm.save(request.user)
            return redirect(view_job, job.job_code)
    else:
        jobForm = JobForm(user=request.user)
    return render_to_response(template, 
                              {'form' : jobForm } ,
                              context_instance=RequestContext(request))



    