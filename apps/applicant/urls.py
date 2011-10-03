from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import register
from applicant.forms import ApplicantLoginForm, DemoApplicantRegistrationForm

urlpatterns = patterns('',
    url(r'^login/',
        'account.views.do_login',
        {
         'form_class': ApplicantLoginForm,
         'template': 'applicant/account/login.html',
         },
        name='applicant_login'),
    
    url(r'^logout/',
        'account.views.do_logout',
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
         'extra_context': {'settings':settings,},
         },
        name='applicant_register'),
                       
    url(r'^demo_register/',
        register,
        {
         'backend': 'applicant.backends.DemoApplicantBackend',
         'template_name': 'applicant/registration/registration_form.html',
         'extra_context': {'settings':settings,},
         },
        name='demo_applicant_register'),

    url(r'^verify_phone/(?P<mobile_number>[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9])/',
        'applicant.views.verify_phone',
        {
            'template': 'applicant/registration/verify_phone.html',
        },
        name='verify_phone'),

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

    url(r'^view/(?P<applicant_id>\d+)/(?P<job_id>\d+)$',
        'applicant.views.view_profile',
        {
         'template': 'applicant/profile/profile.html'
        },
        name='applicant_view_profile'),
    url(r'^job/view/(?P<job_code>\d+)$',
        'job.views.view_job',
        {
         'template' : 'applicant/job/job.html',
         'is_applicant': True,
         },
        name='applicant_view_job'),

    url(r'^job/apply/(?P<job_code>\d+)$',
        'applicant.views.apply',
        {'redirect_url' : 'applicant_dashboard'},
        name='applicant_apply'),

    url(r'^job/remove/(?P<job_code>\d+)$',
        'applicant.views.remove_job',
        {'redirect_url' : 'applicant_dashboard'},
        name='applicant_remove_job'),
)