from django.contrib import admin
from job.models import Job,Availability,Workday,Location,Education,Experience,Industry

admin.site.register(Job)
admin.site.register(Availability)
admin.site.register(Workday)
admin.site.register(Location)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Industry)