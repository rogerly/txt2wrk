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
)