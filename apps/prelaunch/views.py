'''
Created on Jun 13, 2011

@author: Jon
'''

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from forms import PotentialUsersForm
from applicant.forms import ApplicantLoginForm
from employer.forms import EmployerLoginForm
from django.template import RequestContext

def contact(request, template=None):
    ctxt = {}
    demo = False
    if 'demo' in request.session:
        demo = request.session['demo']
    ctxt['applicant_login_form'] = ApplicantLoginForm(demo=demo)
    ctxt['employer_login_form'] = EmployerLoginForm(demo=demo)
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
    demo = False
    if 'demo' in request.session:
        demo = request.session['demo']
    ctxt['applicant_login_form'] = ApplicantLoginForm(demo=demo)
    ctxt['employer_login_form'] = EmployerLoginForm(demo=demo)
    ctxt['settings'] = settings
    return render_to_response(template, ctxt, context_instance = RequestContext(request))

# Just sets up the account for demo purposes
def demo(request, demo_mode=True, redirect_url=None):
    if demo_mode:
        request.session['demo'] = True
    else:
        del(request.session['demo'])

    if 'next' in request.GET:
        next = request.GET['next']
    else:
        next = reverse(redirect_url)
    return redirect(next)