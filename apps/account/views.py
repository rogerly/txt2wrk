from django.conf import settings

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
                    try:
                        profile = EmployerProfile.objects.get(user=form.user)
                    except EmployerProfile.DoesNotExist:
                        return redirect(reverse('splash'))

                return redirect(profile.get_login_destination())
    else:
        form = form_class()

    return render_to_response(template,
                              {
                               'form': form,
                               'next': next,
                               'settings': settings,
                               },
                              context_instance=RequestContext(request))

@csrf_exempt
def do_logout(request, next_page=None, template_name='account/logout.html', redirect_field_name=REDIRECT_FIELD_NAME):
    user = request.user
    if user is not None:
        try:
            profile = ApplicantProfile.objects.get(user=user)
        except ApplicantProfile.DoesNotExist:
            profile = EmployerProfile.objects.get(user=user)

    return_value = logout_view(request, next_page, template_name, redirect_field_name)

    return return_value
