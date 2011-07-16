from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout as logout_view
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login

from applicant.models import ApplicantProfile
from employer.models import EmployerProfile

@csrf_exempt
def do_login(request, template='account/login.html', form_class=None):
    
    next = request.GET.get('next')
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            login(request, form.user)
            if next:
                return redirect(next)
            else:
                try:
                    profile = ApplicantProfile.objects.get(user=form.user)
                except ApplicantProfile.DoesNotExist:
                    profile = EmployerProfile.objects.get(user=form.user)

                if profile.demo:
                    request.session['demo'] = True

                return redirect(profile.get_login_destination())
    else:
        form = form_class()

    return render_to_response(template,
                              {
                               'form': form,
                               'next': next,
                               },
                              context_instance=RequestContext(request))

@csrf_exempt
def do_logout(request, next_page=None, template_name='account/logout.html', redirect_field_name=REDIRECT_FIELD_NAME):
    user = request.user
    print user
    demo = False
    if user is not None:
        try:
            profile = ApplicantProfile.objects.get(user=user)
        except ApplicantProfile.DoesNotExist:
            profile = EmployerProfile.objects.get(user=user)

        print profile
        if profile is not None:
            demo = profile.demo

    print demo

    return_value = logout_view(request, next_page, template_name, redirect_field_name)
    if demo:
        print 'demo is true'
        request.session['demo'] = True

    return return_value
