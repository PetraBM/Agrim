from django.contrib.auth.models import User
from appka.models import Profile


class EmailAuthBackend:
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user

            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    profile = Profile.objects.filter(user=user)
    if not profile:
        Profile.objects.create(user=user, photo=kwargs["response"]["picture"])

