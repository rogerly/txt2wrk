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

    url(r'^new_listings/(?P<job_recommendation_id>\d+)/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.new_listings',
        {
         'template': 'call/fragments/new_listings.html',
         },
        name='call_new_listings'),

    url(r'^new_listings/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.new_listings',
        {
         'template': 'call/fragments/new_listings.html',
         },
        name='call_new_listings'),

    url(r'^new_listings/(?P<job_recommendation_id>\d+)/',
        'call.views.new_listings',
        {
         'template': 'call/fragments/new_listings.html',
         },
        name='call_new_listings'),

    url(r'^new_listings/',
        'call.views.new_listings',
        {
         'template': 'call/fragments/new_listings.html',
         },
        name='call_new_listings'),

    url(r'^handle_listing/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.handle_listing',
        {
            'template': 'call/fragments/handle_listing.html',
        },
        name='handle_listing'),

    url(r'^handle_listing_detail/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.handle_listing',
        {
            'template': 'call/fragments/handle_listing.html',
            'detail': True,
        },
        name='handle_listing_detail'),

    url(r'^listing_info/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.listing_info',
        {
         'template': 'call/fragments/listing_info.html',
         },
        name='call_listing_info'),

    url(r'^listing_info/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/',
        'call.views.listing_info',
        {
         'template': 'call/fragments/listing_info.html',
         },
        name='call_listing_info'),

    url(r'^listing_info/(?P<job_recommendation_id>\d+)/',
        'call.views.listing_info',
        {
         'template': 'call/fragments/listing_info.html',
         },
        name='call_listing_info'),

    url(r'^apply/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.apply',
        {
         'template': 'call/fragments/apply.html',
         },
        name='call_apply'),

    url(r'^apply/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/',
        'call.views.apply',
        {
         'template': 'call/fragments/apply.html',
         },
        name='call_apply'),

    url(r'^apply/(?P<job_recommendation_id>\d+)/',
        'call.views.apply',
        {
         'template': 'call/fragments/apply.html',
         },
        name='call_apply'),

    url(r'^save_listing/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.save_listing',
        {
         'template': 'call/fragments/save_listing.html',
         },
        name='call_save_listing'),

    url(r'^save_listing/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/',
        'call.views.save_listing',
        {
         'template': 'call/fragments/save_listing.html',
         },
        name='call_save_listing'),

    url(r'^save_listing/(?P<job_recommendation_id>\d+)/',
        'call.views.save_listing',
        {
         'template': 'call/fragments/save_listing.html',
         },
        name='call_save_listing'),

    url(r'^delete_listing/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.delete_listing',
        {
         'template': 'call/fragments/delete_listing.html',
         },
        name='call_delete_listing'),

    url(r'^delete_listing/(?P<listing_type>\d+)/(?P<job_recommendation_id>\d+)/',
        'call.views.delete_listing',
        {
         'template': 'call/fragments/delete_listing.html',
         },
        name='call_delete_listing'),

    url(r'^delete_listing/(?P<job_recommendation_id>\d+)/',
        'call.views.delete_listing',
        {
         'template': 'call/fragments/delete_listing.html',
         },
        name='call_delete_listing'),

    url(r'^saved_listings/(?P<job_recommendation_id>\d+)/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.saved_listings',
        {
         'template': 'call/fragments/saved_listings.html',
         },
        name='call_saved_listings'),

    url(r'^saved_listings/(?P<job_index>\d+)/(?P<job_total>\d+)/',
        'call.views.saved_listings',
        {
         'template': 'call/fragments/saved_listings.html',
         },
        name='call_saved_listings'),

    url(r'^saved_listings/(?P<job_recommendation_id>\d+)/',
        'call.views.saved_listings',
        {
         'template': 'call/fragments/saved_listings.html',
         },
        name='call_saved_listings'),

    url(r'^saved_listings/',
        'call.views.new_listings',
        {
         'template': 'call/fragments/saved_listings.html',
         },
        name='call_saved_listings'),

    url(r'^job_code/',
        'call.views.job_code',
        {
         'template': 'call/fragments/job_code.html',
         },
        name='call_job_code'),

    url(r'^hangup/',
        'call.views.hangup',
        {
         'template': 'call/fragments/hangup.html',
         },
        name='call_hangup'),
)