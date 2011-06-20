'''
Created on Jun 18, 2011

@author: Jon
'''

from forms import JobForm
from models import Job
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext

def view_profile(request, job_code = None, template = 'job/view_job.html'):
    if request.method == 'GET' and job_code:
        job = Job.objects.get(job_code=job_code)
        return render_to_response(template, {'job': job}, context_instance = RequestContext(request))
    return render_to_response('job/create_job.html', {'form' : JobForm()}, context_instance = RequestContext(request))


def create_profile(request, template = 'job/create_job.html'):
    form = None
    if request.method == 'GET':
        form = JobForm()
    else:
        form = JobForm(data=request.POST)
        if form.is_valid():
            job = form.save()
            return redirect(view_profile, job_code = job.job_code)
    return render_to_response(template, {'form' : form}, context_instance = RequestContext(request))  

    