'''
Created on Jun 18, 2011

@author: Jon
'''

from django import forms
from job import models
from employer.models import EmployerProfile

class JobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['employer'].widget = forms.HiddenInput()
        self.fields['employer'].initial = EmployerProfile.objects.get(user=self.request.user)
    
    class Meta:
        model = models.Job
        fields = ('id', 
                  'title', 
                  'description', 
                  'availability', 
                  'workday',
                  'location',
                  'education',
                  'experience',
                  'industry',
                  'employer',
                  )
