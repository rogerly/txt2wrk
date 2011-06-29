from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name='%(class)s'
                                )

    class Meta:
        abstract = True
        
    def get_login_destination(self):
        raise NotImplementedError
