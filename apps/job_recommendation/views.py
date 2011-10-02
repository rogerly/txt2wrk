from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import JobRecommendationForm

def assign_job(request, template=None):

    if request.POST:
        form = JobRecommendationForm(request.POST)
        ctxt = {}
        ctxt['form'] = form
        if form.is_valid():
            ctxt['success'] = True
            ctxt['form'] = JobRecommendationForm()
            form.save()

        return render_to_response(template, ctxt, context_instance = RequestContext(request))

    return render_to_response(template, {'form': JobRecommendationForm()}, context_instance = RequestContext(request))
