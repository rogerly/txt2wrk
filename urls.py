import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from registration.views import register
from account.forms import ApplicantLoginForm

urlpatterns = patterns('',
    # Example:
    # (r'^txt2wrk/', include('txt2wrk.foo.urls')),
    url(r'^$', 'prelaunch.views.splash'),
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    url(r'^login/',
        'account.views.do_login',
        {
         'form_class': ApplicantLoginForm,
         'template': 'applicant/account/login.html',
         },
        name='login'),
    
    url(r'^logout/',
        'django.contrib.auth.views.logout',
        {
         'next_page': '/',
         'redirect_field_name': 'next',
         },
        name='logout'),
        
    url(r'^register/', 
        register, 
        { 
         'backend': 'account.backends.ApplicantBackend',
         'template_name': 'applicant/registration/registration_form.html', 
        },
        name='register'),
                       
    url(r'^register_complete/',
        direct_to_template,
        {
         'template': 'applicant/registration/registration_complete.html',
        },
        name='registration_complete'),

    url(r'^profile/',
        'applicant.views.applicant_profile',
        {
         'template': 'applicant/account/profile.html'
        },
        name='profile'),
    url(r'^dashboard/',
        'applicant.views.applicant_dashboard',
        {
         'template' : 'applicant/account/dashboard.html'
         }
        ),
    url(r'^job/create/$',
        'job.views.create_profile',
        {
         'template' : 'employer/job/create_job.html'
         },
        name = 'create_profile'),
    url(r'^job/view/(?P<job_code>\d+)$',
        'job.views.view_profile',
        {
         'template' : 'employer/job/view_job.html'
         },
        name = 'view_profile'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {
         'document_root': settings.STATIC_MEDIA_PATH,
        }),

    url(r'^receive_sms/', 'sms.views.receive_sms',
        {
         'template': 'sms/sms_response.html',
         },
        name='receive_sms'),
)
