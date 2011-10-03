"""
                   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions.

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.
"""


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

