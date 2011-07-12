'''
Created on Jun 15, 2011

@author: Jon
'''
from models import PotentialUsers
from django import forms
    
class PotentialUsersForm(forms.ModelForm):
    comments = forms.CharField(widget = forms.Textarea(), required = True)
    first_name = forms.CharField(widget = forms.TextInput(), required = True)
    last_name = forms.CharField(widget = forms.TextInput(), required = True)
    email = forms.CharField(widget = forms.TextInput(), required = True)
    confirm_email = forms.CharField(label='Confirm Email', widget = forms.TextInput(), required = True)

    def clean(self):
        if 'email' in self.cleaned_data and 'confirm_email' in self.cleaned_data:
            if self.cleaned_data['email'] != self.cleaned_data['confirm_email']:
                raise forms.ValidationError("Emails did not match")

        return super(PotentialUsersForm, self).clean()

    class Meta:
        model = PotentialUsers


