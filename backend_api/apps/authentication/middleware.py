from re import sub
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import AccessToken

from .models import UserVisit


def parse_remote_addr(request: HttpRequest) -> str:
    """Extract client IP from request."""
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR", "")


def parse_ua_string(request: HttpRequest) -> str:
    """Extract client user-agent from request."""
    return request.headers.get("User-Agent", "")


class AuditLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        user_id = None
        if header_token is not None:
            token = str(request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1])
            try:
                user_id = AccessToken(token)['user_id']
            except:
                return None
        else:
            user_id = request.user.id

        if user_id is not None:
            path = f"{request.get_full_path()}"
            if path.startswith("/api/v1/authentication/user_logs") or path.startswith('/api/v1/core/notification/api/unread_count') or path.startswith('/api/v1/core/notification/api/unread_list'):
                exempted = True
            else:
                exempted = False

            if not exempted:
                UserVisit.objects.create(
                    user_id=user_id,
                    session_key=request.session.session_key,
                    remote_addr=parse_remote_addr(request),
                    ua_string=parse_ua_string(request),
                    url=request.get_full_path()
                )
            return None
        else:
            path = f"{request.get_full_path()}"
            exempted = True if path.startswith("/supplier/logs/json") else False

            if not exempted:
                UserVisit.objects.create(
                    session_key=request.session.session_key,
                    remote_addr=parse_remote_addr(request),
                    ua_string=parse_ua_string(request),
                    url=request.get_full_path()
                )
            return None