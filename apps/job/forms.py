'''
Created on Jun 18, 2011

@author: Jon
'''

from django import forms
from employer import models
from job import models

class JobForm(forms.ModelForm):
    workday = forms.ModelMultipleChoiceField(
                    widget = forms.CheckboxSelectMultiple,
                    label = 'Days available to work',
                    queryset = models.Workday.objects.all()
    )
    
    industry = forms.ModelMultipleChoiceField(
                    widget = forms.CheckboxSelectMultiple,
                    label = 'Please select areas with the most experience',
                    queryset = models.Industry.objects.all()
    )
    
    def save(self, user=None, commit=True):
        job = super(JobForm, self).save(commit=commit)

        if user:
            employer = models.EmployerProfile.objects.get(user=self.request.user)
            job.employer = employer

        if commit:
            job.save()

        return job
    
    class Meta:
        model = models.Job
        fields = ('id', 
                  'description', 
                  'availability', 
                  'workday',
                  'education',
                  'experience',
                  'industry',
                  )

