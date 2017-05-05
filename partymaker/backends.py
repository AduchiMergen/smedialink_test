from partymaker.models import User


class AuthBackend(object):
    def authenticate(self, name=None, photo=None):
        user, created = User.objects.update_or_create(name=name, defaults={'photo': photo})
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
