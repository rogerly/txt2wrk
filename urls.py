from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from registration.views import register
from applicant.forms import ApplicantLoginForm

urlpatterns = patterns('',
    # Example:
    # (r'^txt2wrk/', include('txt2wrk.foo.urls')),
    url(r'^$', 'prelaunch.views.splash', { 'template': 'about/splash.html', }, name='splash'),
    url(r'^contact/$', 'prelaunch.views.contact', { 'template': 'about/contact.html', }, name='contact'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^applicant/', include('applicant.urls')),

    (r'^employer/', include('employer.urls')),
    
    (r'^call/', include('call.urls')),

    (r'^job/', include('job.urls')),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {
         'document_root': settings.STATIC_MEDIA_PATH,
        }),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {
         'document_root': settings.STATIC_MEDIA_PATH,
        }),
    url(r'^receive_sms/', 'sms.views.receive_sms',
        {
         'template': 'sms/sms_response.html',
         },
        name='receive_sms'),

    url(r'^demo/(?P<demo_mode>\w+)/$', 'prelaunch.views.demo', { 'redirect_url': 'splash' }, name='demo'),
    url(r'^demo/$', 'prelaunch.views.demo', { 'redirect_url': 'splash' }, name='demo'),

    url (r'^assign_job/', 'job_recommendation.views.assign_job',
        { 'template': 'job/assign_job.html',},
        name='assign_job'),
)
