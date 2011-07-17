'''
Created on Jun 18, 2011

@author: Jon
'''

from math import acos, cos, radians, sin
from models import Job, JobLocation
from forms import JobForm
from signals import job_created
from applicant.models import ApplicantProfile, ApplicantJob
from employer.models import EmployerProfile
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.forms.models import inlineformset_factory

@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def manage_job(request, job_code = None, template = 'job/view_job.html'):
    if request.method == 'GET' and job_code:
        profile = EmployerProfile.objects.get(user=request.user)
        job = Job.objects.get(job_code=job_code)
        return render_to_response(template,
                                  {'job' : job, 
                                   'profile' : profile,
                                   'applications' : job.applicant_job.all() },
                                  context_instance = RequestContext(request))
    return redirect(create_job)

def view_job(request, job_code = None, is_applicant = False, template = None):
    ctxt = {}
    if request.method == 'GET' and job_code:
        job = Job.objects.all().select_related('joblocation').get(job_code=job_code)
        ctxt['job'] = job
        if is_applicant:
            ctxt['is_applicant'] = is_applicant
            applicant = ApplicantProfile.objects.get(user=request.user)
            try:
                application = ApplicantJob.objects.get(applicant=applicant, job = job)
                ctxt['already_applied'] = True
            except ApplicantJob.DoesNotExist:
                ctxt['already_applied'] = False

            try:
                latitude1 = applicant.latitude
                longitude1 = applicant.longitude

                latitude2 = job.location.all()[0].latitude
                longitude2 = job.location.all()[0].longitude

                if latitude1 is not None and latitude1 != '' and latitude2 is not None and latitude2 != '' and longitude1 is not None and longitude1 != '' and longitude2 is not None and longitude2 != '':
                    # distance calculation from
                    # http://stackoverflow.com/questions/1916953/filter-zipcodes-by-proximity-in-django-with-the-spherical-law-of-cosines
                    distance = acos(cos(radians(float(latitude1))) * cos(radians(float(latitude2))) * cos(radians(float(longitude2)) - radians(float(longitude1))) + sin(radians(float(latitude1))) * sin(radians(float(latitude2)))) * 3959
                    ctxt['distance'] = distance
            except:
                pass

        return render_to_response(template,
                                  ctxt,
                                  context_instance = RequestContext(request))
    return redirect(create_job)


@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def edit_job(request, job_code, template = 'job/edit_job.html'):
    form = None 
    job = Job.objects.get(job_code=job_code)
    JobLocationInlineFormSet = inlineformset_factory(Job, JobLocation, max_num=1, extra=1)
    
    ''' Check if user has permission to edit this job '''
    if job.employer.user != request.user:
        redirect(view_job, job_code)  
    
    if request.method == 'POST':
        form = JobForm(data=request.POST, user=request.user, instance=job)
        formset = JobLocationInlineFormSet(data=request.POST, instance=job)
        if formset.is_valid():
            formset.save()

            if form.is_valid():
                job = form.save()
                return redirect(reverse('employer_dashboard'))
    else:
        form = JobForm(instance=job, user=request.user)
        formset = JobLocationInlineFormSet(instance=job)
    return render_to_response(template, 
                              {'form' : form,
                               'formset': formset,
                               'job_code' : job_code}, 
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def create_job(request, job_code=None, template = 'job/edit_job.html'):
    jobForm = None 
    JobLocationInlineFormSet = inlineformset_factory(Job, JobLocation, max_num=1, extra=1)

    if request.method == 'POST':        
        jobForm = JobForm(data=request.POST, user=request.user)
        if jobForm.is_valid():
            job = jobForm.save(commit=False)
            formset = JobLocationInlineFormSet(data=request.POST, instance=job)
            if formset.is_valid:
                job = jobForm.save()
                formset.save()

                job_created.send(sender=job.__class__, job=job)
                return redirect(reverse('employer_dashboard'))
        else:
            formset = JobLocationInlineFormSet(data=request.POST)
            formset.is_valid
    else:
        jobForm = JobForm(user=request.user)
        employer = EmployerProfile.objects.get(user=request.user)
        formset = JobLocationInlineFormSet()
        for subform in formset:
            subform.initial = {
                'business_name': employer.business_name,
                'business_address1': employer.business_address1,
                'business_address2': employer.business_address2,
                'city': employer.city,
                'zip_code': employer.zip_code,
            }
    return render_to_response(template,
                              {'form' : jobForm,
                               'formset' : formset, } ,
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def close_job(request, job_code=None, redirect_url=None):
    try:
        job = Job.objects.get(job_code=job_code)
        job.state = Job.JOB_FILLED
        job.save()
    except Job.DoesNotExist:
        pass

    return redirect(reverse(redirect_url))