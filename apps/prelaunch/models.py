'''
Created on Jun 13, 2011

@author: Jon
'''
from django.db import models

class PotentialUsers(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    comments = models.CharField(max_length=100)
    