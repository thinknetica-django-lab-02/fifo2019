
class MobileVersionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        http_user_agent = request.META.get('HTTP_USER_AGENT', '')

        if 'Mobile' in http_user_agent:
            request.is_mobile = True

        return self.get_response(request)
