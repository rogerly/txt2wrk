'''
Created on Jun 13, 2011

@author: Jon
'''

from django.shortcuts import render_to_response
from forms import PotentialUsersForm
from django.template import RequestContext

def splash(request):
    newform = PotentialUsersForm()
    if request.POST:
        form = PotentialUsersForm(request.POST)
        if form.is_valid() and form.is_email_default():
            form.save()
            return render_to_response('about/prerelease.html', {'form' : newform, 'success_message' : 'Submission successful!' },
                context_instance = RequestContext(request))
        else:
            return render_to_response('about/prerelease.html', {'form' : form, 'error_message' : "There was a problem with your submission.  Please make sure you've entered an email address. " },
                context_instance = RequestContext(request))
        
    return render_to_response('about/prerelease.html', {'form' : newform },
                context_instance = RequestContext(request))

    