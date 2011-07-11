from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import register
from employer.forms import EmployerLoginForm

urlpatterns = patterns('',
    url(r'^login/',
        'account.views.do_login',
        {
         'form_class': EmployerLoginForm,
         'template': 'employer/account/login.html',
         },
        name='employer_login'),
    
    url(r'^logout/',
        'django.contrib.auth.views.logout',
        {
         'next_page': '/',
         'redirect_field_name': 'next',
         },
        name='employer_logout'),
        
    url(r'^register/', 
        register, 
        { 
         'backend': 'employer.backends.EmployerBackend',
         'template_name': 'employer/registration/registration_form.html',
         'extra_context': {'settings':settings,},
        },
        name='employer_register'),
                       
    url(r'^register_complete/',
        direct_to_template,
        {
         'template': 'employer/registration/registration_complete.html',
        },
        name='employer_registration_complete'),

    url(r'^setup_profile/',
        'employer.views.employer_profile',
        {
         'template': 'employer/account/profile.html',
         'first_time_setup': True,
        },
        name='employer_profile_setup'),

    url(r'^profile/',
        'employer.views.employer_profile',
        {
         'template': 'employer/account/profile.html'
        },
        name='employer_profile'),

    url(r'^dashboard/',
        'employer.views.employer_dashboard',
        {
         'template' : 'employer/account/dashboard.html'
        },
        name='employer_dashboard'),
)