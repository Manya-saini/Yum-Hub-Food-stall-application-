from django.contrib.auth.backends import ModelBackend
from .models import Profile

class ProfileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, user_type=None):
        print(f"Username: {username}, User Type: {user_type}, Password: {password}")
        try:
            user = Profile.objects.get(username=username, user_type=user_type)
            print(user)
            if user.check_password(password):
                return user
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None