from django.contrib import admin
from applicant.models import ApplicantProfile, ApplicantJob

admin.site.register(ApplicantProfile)
admin.site.register(ApplicantJob)