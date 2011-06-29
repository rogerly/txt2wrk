from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import user_passes_test
from forms import EmployerProfileForm
from models import EmployerProfile

@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def employer_profile(request, template='employer/account/profile.html'):
    form = None 
    if request.method == 'POST':
        form = EmployerProfileForm(data=request.POST, instance=EmployerProfile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return redirect(employer_dashboard)
    else:
        form = EmployerProfileForm(instance=EmployerProfile.objects.get(user=request.user))
    return render_to_response(template, 
                              {'form' : form}, 
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/employer/login')
def employer_dashboard(request, template='employer/account/dashboard.html'):
    profile = EmployerProfile.objects.get(user=request.user)
    return render_to_response(template, 
                              {'profile' : profile },
                              context_instance=RequestContext(request))
