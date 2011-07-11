'''
Created on Jul 2, 2011

@author: Jon
'''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^create/',
        'job.views.create_job',
        {
         'template' : 'employer/job/edit_job.html'
         },
        name = 'create_job'),
    url(r'^edit/(?P<job_code>\d+)$',
        'job.views.edit_job',
        {
         'template' : 'employer/job/edit_job.html'
         },
        name = 'edit_job'),
    url(r'^view/(?P<job_code>\d+)$',
        'job.views.view_job',
        {
         'template' : 'employer/job/job.html',
         'is_applicant': False,
         }, 
        name='view_job'),
    url(r'^manage/(?P<job_code>\d+)$',
        'job.views.manage_job',
        {
         'template' : 'employer/job/manage_job.html'
         },
        name='manage_job'),
    url(r'^close/(?P<job_code>\d+)$',
        'job.views.close_job',
        {'redirect_url' : 'employer_dashboard'},
        name='close_job'),
)
