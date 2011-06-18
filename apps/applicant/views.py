from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_authenticated(), login_url='/login')
def profile(request, template='applicant/account/profile.html'):
    return render_to_response(template, 
                              {}, 
                              context_instance=RequestContext(request))
