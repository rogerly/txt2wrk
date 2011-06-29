from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from forms import ReceiveCallForm
from applicant.models import ApplicantProfile

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
            profile = ApplicantProfile.objects.get(mobile_number=form.cleaned_data['From'])
            user = profile.user
        except ApplicantProfile.DoesNotExist:
            pass
    
    context['user'] = user

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def wrong_user(request, template=None):
    context = {}
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def enter_password(request, template=None):
    context = {}
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

@csrf_exempt
def verify_password(request, template=None):
    context = {}
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

