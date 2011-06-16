'''
Created on Jun 13, 2011

@author: Jon
'''
from django.db import models

class PotentialUsers(models.Model):
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    email = models.CharField(max_length=200)
    comments = models.CharField(max_length=200,blank=True)
    
    