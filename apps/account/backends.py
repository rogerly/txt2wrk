from django.contrib.auth.models import User

from applicant.models import ApplicantProfile
from employer.models import EmployerProfile

class ApplicantModelBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            if '@' in username:
                user = User.objects.get(email__iexact=username)
            elif '-' in username:
                try:
                    profile = ApplicantProfile.objects.get(mobile_number=username)
                    user = profile.user
                except ApplicantProfile.DoesNotExist:
                    return None
            else:
                user = User.objects.get(username__iexact=username)

            # Check to see if user is active (email confirmation) and if not for now return Does not exist -> FIX_ME
            if not user.is_active:
                raise User.DoesNotExist
            
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

