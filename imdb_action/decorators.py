from imdb_action.models import AdminData, UserData
from django.http import HttpResponse
from imdb_action.common_helper import http_response_smart

def admin_required(function):
    def _decorated(request, *args, **kwargs):
        try:
            secure_key = request.POST.get('secure_key')
            if not secure_key:
                return HttpResponse(http_response_smart({}, "Unauthorized", "Invalid Admin session"), status = 401)
            if AdminData.objects.filter(password = secure_key, is_active=1).exists():
                request.session = secure_key
            else:
                return HttpResponse(http_response_smart({}, "Unauthorized", "User not authorized to perform this action"), status = 401)
        except Exception as e:
            return HttpResponse(http_response_smart({}, "Does not Exist", "Current user does not exist in Database"), status=401)
        return function(request, *args, **kwargs)
    return _decorated

def api_login_required(function):
    def _decorated(request, *args, **kwargs):
        try:
            user_key = request.POST.get('user_key')
            if not user_key:
                return HttpResponse(http_response_smart({}, "Unauthorized", "Invalid User session"), status = 401)
            if UserData.objects.filter(password = user_key, is_active=1).exists():
                request.session = user_key
            else:
                return HttpResponse(http_response_smart({}, "Unauthorized", "User not authorized to perform this action"), status = 401)
        except Exception as e:
            return HttpResponse(http_response_smart({}, "Does not Exist", "Current user does not exist in Database"), status=401)
        return function(request, *args, **kwargs)
    return _decorated
