from django.core.urlresolvers import reverse
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
