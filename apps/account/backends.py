from django.contrib.auth.models import User

from applicant.models import ApplicantProfile
from employer.models import EmployerProfile

class ApplicantModelBackend(object):
    def authenticate(self, username=None, password=None, demo=False):
        try:
            if '@' in username:
                user = User.objects.get(email__iexact=username)
            elif '-' in username:
                try:
                    profile = ApplicantProfile.objects.get(mobile_number=username, demo=demo)
                    user = profile.user
                except ApplicantProfile.DoesNotExist:
                    return None
            else:
#                try:
                user = User.objects.get(username__iexact='%s%s' % (username, '_demo' if demo else ''))
#                    profile = EmployerProfile.objects.get(user__username=username, demo=demo)
#                    user = profile.user
#                except EmployerProfile.DoesNotExist:
#                    return None
#                    user = User.objects.get(username=username)

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

