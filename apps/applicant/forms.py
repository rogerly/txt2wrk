from django import forms
from job import models
from models import ApplicantProfile

class ApplicantProfileForm(forms.ModelForm):
    
    availability = forms.ModelChoiceField(
                        widget = forms.Select,
                        required = True,
                        label = 'Available to start',
                        queryset = models.Availability.objects.all()
    )
    
    workday = forms.ModelMultipleChoiceField(
                    widget = forms.CheckboxSelectMultiple,
                    label = 'Workdays',
                    queryset = models.Workday.objects.all()
    )
    
    location = forms.ModelChoiceField(
                    widget = forms.Select,
                    required = True,
                    label = 'Locations',
                    queryset = models.Location.objects.all()
    )
    
    education = forms.ModelChoiceField( 
                    widget = forms.Select,
                    required = True,
                    label = 'Highest Education',
                    queryset = models.Education.objects.all()
    )
    
    experience = forms.ModelChoiceField(
                    widget = forms.Select,
                    required = True,
                    label = 'Years of Work Experience',
                    queryset = models.Experience.objects.all()
    )
    
    industry = forms.ModelMultipleChoiceField(
                    widget = forms.CheckboxSelectMultiple,
                    required = False,
                    label = 'Please select areas with the most experience',
                    queryset = models.Industry.objects.all()
    )
    
    class Meta:
        model = ApplicantProfile
        exclude = ('mobile_number', 'confirmed_phone', 'user')