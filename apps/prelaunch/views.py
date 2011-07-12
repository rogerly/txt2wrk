'''
Created on Jun 13, 2011

@author: Jon
'''

from django.conf import settings
from django.shortcuts import render_to_response
from forms import PotentialUsersForm
from applicant.forms import ApplicantLoginForm
from employer.forms import EmployerLoginForm
from django.template import RequestContext

def contact(request, template=None):
    ctxt = {}
    ctxt['applicant_login_form'] = ApplicantLoginForm()
    ctxt['employer_login_form'] = EmployerLoginForm()
    ctxt['settings'] = settings
    if request.POST:
        form = PotentialUsersForm(request.POST)
        if form.is_valid():
            form.save()
            ctxt['form'] = PotentialUsersForm()
            ctxt['success'] = True
        else:
            ctxt['form'] = form
    else:
        ctxt['form'] = PotentialUsersForm()
    return render_to_response(template, ctxt,
                context_instance = RequestContext(request))

def splash(request, template=None):

    ctxt = {}
    ctxt['applicant_login_form'] = ApplicantLoginForm()
    ctxt['employer_login_form'] = EmployerLoginForm()
    ctxt['settings'] = settings
    return render_to_response(template, ctxt, context_instance = RequestContext(request))