from django.contrib import admin
from job.models import Job,Workday,Industry,JobLocation

class JobLocationInline(admin.StackedInline):
   model = JobLocation
   extra = 1

class JobAdmin(admin.ModelAdmin):
    inlines = [JobLocationInline]


admin.site.register(Job, JobAdmin)
admin.site.register(Workday)
admin.site.register(Industry)
