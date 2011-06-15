from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from registration.views import register

urlpatterns = patterns('',
    # Example:
    # (r'^txt2wrk/', include('txt2wrk.foo.urls')),
    url(r'^$', direct_to_template, {
        'template': 'about/splash.html',
    }, name="splash"),
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    url(r'^register/', 
        register, 
        { 
         'backend': 'account.backends.ApplicantBackend',
         'template_name': 'applicant/registration/registration_form.html', 
        },
        name='register'),
)
