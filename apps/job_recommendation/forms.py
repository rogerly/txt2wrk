from django import forms

from models import JobRecommendation

class JobRecommendationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobRecommendationForm, self).__init__(*args, **kwargs)

        self.fields['state'].widget = forms.HiddenInput()

    class Meta:
        model = JobRecommendation
