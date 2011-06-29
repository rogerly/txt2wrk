from django.contrib import admin
from call.models import Call, CallFragment

class CallFragmentInline(admin.StackedInline):
   model = CallFragment
   extra = 0
   raw_id_fields = ('call',)

class CallAdmin(admin.ModelAdmin):
    inlines = [CallFragmentInline]    
        
admin.site.register(Call, CallAdmin)
