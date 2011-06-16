'''
Created on Jun 15, 2011

@author: Jon
'''
from models import PotentialUsers
from django import forms
from django.forms import ModelForm,TextInput,Textarea
    
class PotentialUsersForm(ModelForm):
    comments = forms.CharField(widget = Textarea(attrs={
                                'onFocus' : "this.value=''; setbg('#e5fff3');",
                                'onBlur' : "setbg('white')"}),
                                initial="""Thoughts on who could use this app? \nHave some questions? \nLet us know! \n(optional)""",
                                required = False 
                            )
    first_name = forms.CharField(widget = TextInput(attrs={'value' : "Your first name (optional)",
                                     'onFocus' : "if (this.value == this.defaultValue) {this.value='';}",
                                     'onBlur' : "if (this.value == '') {this.value = this.defaultValue;}"
                                    }), initial = "Your last name (optional)",
                                 required = False)
    last_name = forms.CharField(widget = TextInput(attrs={
                                     'onFocus' : "if (this.value == this.defaultValue) {this.value='';}",
                                     'onBlur' : "if (this.value == '') {this.value = this.defaultValue;}"
                                    }), initial = "Your last name (optional)",
                                required = False)
    email = forms.CharField(widget = TextInput(attrs={
                                     'onFocus' : "if (this.value == this.defaultValue) {this.value='';}",
                                     'onBlur' : "if (this.value == '') {this.value = this.defaultValue;}"
                                    }), initial = 'Your email (required)', 
                                required = True)
    
    def is_email_default(self):
        return self.data['email'] != 'Your email (required)';
    
    class Meta:
        model = PotentialUsers


