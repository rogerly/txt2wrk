from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import JobRecommendationForm

def assign_job(request, template=None):
    demo = False
    if 'demo' in request.session:
        demo = True

    if request.POST:
        form = JobRecommendationForm(request.POST, demo=demo)
        ctxt = {}
        ctxt['form'] = form
        if form.is_valid():
            ctxt['success'] = True
            ctxt['form'] = JobRecommendationForm(demo=demo)
            form.save()

        return render_to_response(template, ctxt, context_instance = RequestContext(request))

    return render_to_response(template, {'form': JobRecommendationForm(demo=demo)}, context_instance = RequestContext(request))
