from partymaker.models import User


class AuthBackend(object):
    def authenticate(self, request, name=None):
        try:
            user = User.objects.get(name=name)
        except User.DoesNotExist:
            user = User(name=name)
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
