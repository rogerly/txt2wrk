'''
Created on Jun 18, 2011

@author: Jon
'''

from django import forms
from employer import models
from job import models

from common.helpers import CheckboxSelectMultipleDiv

class JobForm(forms.ModelForm):
    workday = forms.ModelMultipleChoiceField(
                    widget = CheckboxSelectMultipleDiv,
                    label = 'Days available to work',
                    queryset = models.Workday.objects.all()
    )
    
    industry = forms.ModelMultipleChoiceField(
                    widget = CheckboxSelectMultipleDiv,
                    label = 'Please select areas with the most experience',
                    queryset = models.Industry.objects.all().order_by('name')
    )

    edit_location = forms.CharField(
                    widget = forms.HiddenInput(),
                    label = '',
                    required = False,
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['employer'].widget = forms.HiddenInput()
        self.fields['employer'].initial = models.EmployerProfile.objects.get(user=self.user)
        self.fields['employer'].required = False
        
    class Meta:
        model = models.Job
        fields = ('title', 
                  'description', 
                  'availability', 
                  'workday',
                  'education',
                  'experience',
                  'industry',
                  'employer'
                  )

