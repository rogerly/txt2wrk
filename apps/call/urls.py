from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^receive_call/',
        'call.views.receive_call',
        {
         'template': 'call/fragments/welcome.html',
         },
        name='call_welcome'),
    
    url(r'^wrong_user/',
        'call.views.wrong_user',
        {
         'template': 'call/fragments/wrong_user.html',
         },
        name='call_wrong_user'),

    url(r'^enter_password/',
        'call.views.enter_password',
        {
         'template': 'call/fragments/enter_password.html',
         },
        name='call_enter_password'),

    url(r'^verify_password/',
        'call.views.verify_password',
        {
         'template': 'call/fragments/verify_password.html',
         },
        name='call_verify_password'),

    url(r'^main_menu/',
        'call.views.main_menu',
        {
         'template': 'call/fragments/main_menu.html',
         },
        name='call_main_menu'),

    url(r'^new_listings/',
        'call.views.new_listings',
        {
         'template': 'call/fragments/new_listings.html',
         },
        name='call_new_listings'),

    url(r'^saved_listings/',
        'call.views.main_menu',
        {
         'template': 'call/fragments/saved_listings.html',
         },
        name='call_saved_listings'),

    url(r'^job_code/',
        'call.views.main_menu',
        {
         'template': 'call/fragments/job_code.html',
         },
        name='call_job_code'),

    url(r'^hangup/',
        direct_to_template,
        {
         'template': 'call/fragments/hangup.html',
         },
        name='call_hangup'),
)