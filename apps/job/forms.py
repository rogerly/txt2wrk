'''
Created on Jun 18, 2011

@author: Jon
'''

from django import forms
from job import models

class JobForm(forms.ModelForm):
    title = forms.CharField(
                widget=forms.TextInput(),
                label = 'Job Title',
                required = True
    )
    
    description = forms.CharField(
                    widget = forms.TextInput(),
                    label = 'Job Description',
                    required = True
    )
    
    availability = forms.ModelChoiceField(
                        widget = forms.Select,
                        required = True,
                        queryset = models.Availability.objects.all()
    )
    
    workday = forms.ModelMultipleChoiceField(
                    widget = forms.CheckboxSelectMultiple,
                    queryset = models.Workday.objects.all()
    )
    
    location = forms.ModelChoiceField(
                    widget = forms.Select,
                    required = True,
                    queryset = models.Location.objects.all()
    )
    
    education = forms.ModelChoiceField( 
                    widget = forms.Select,
                    required = True,
                    queryset = models.Education.objects.all()
    )
    
    experience = forms.ModelChoiceField(
                    widget = forms.Select,
                    required = True,
                    queryset = models.Experience.objects.all()
    )
    
    industry = forms.ModelMultipleChoiceField(
                    widget = forms.CheckboxSelectMultiple,
                    required = False,
                    queryset = models.Industry.objects.all()
    )
        
    class Meta:
        model = models.Job
        exclude = ('job_code')
