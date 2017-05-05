from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class CheckAdminMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user.is_superuser = request.META['REMOTE_ADDR'] == getattr(settings, 'ADMIN_IP')
