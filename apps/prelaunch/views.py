'''
Created on Jun 13, 2011

@author: Jon
'''

from django.shortcuts import render_to_response
from models import InterestedUsersForm
from django.template import RequestContext

def splash(request):
    if request.POST:
        form = InterestedUsersForm(request.POST)
        if form.is_valid():
            form.save()
    
    form = InterestedUsersForm()

    return render_to_response('about/splash.html', {'form' : form },
                context_instance = RequestContext(request))