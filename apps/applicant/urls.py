from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import register
from applicant.forms import ApplicantLoginForm

urlpatterns = patterns('',
    url(r'^login/',
        'account.views.do_login',
        {
         'form_class': ApplicantLoginForm,
         'template': 'applicant/account/login.html',
         },
        name='applicant_login'),
    
    url(r'^logout/',
        'django.contrib.auth.views.logout',
        {
         'next_page': '/',
         'redirect_field_name': 'next',
         },
        name='applicant_logout'),
        
    url(r'^register/', 
        register, 
        { 
         'backend': 'applicant.backends.ApplicantBackend',
         'template_name': 'applicant/registration/registration_form.html', 
        },
        name='applicant_register'),
                       
    url(r'^register_complete/',
        direct_to_template,
        {
         'template': 'applicant/registration/registration_complete.html',
        },
        name='applicant_registration_complete'),

    url(r'^profile/',
        'applicant.views.applicant_profile',
        {
         'template': 'applicant/account/profile.html'
        },
        name='applicant_profile'),
    url(r'^dashboard/',
        'applicant.views.applicant_dashboard',
        {
         'template' : 'applicant/account/dashboard.html'
         },
        name='applicant_dashboard'),

    url(r'^job/view/(?P<job_code>\d+)$',
        'job.views.view_job',
        {
         'template' : 'applicant/job/job.html'
         },
        name='applicant_view_job'),
)