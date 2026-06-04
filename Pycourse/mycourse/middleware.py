class AdminRoleMiddleware:
    """Adds is_admin_role to request for easy template access."""
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            request.is_admin = request.user.is_staff or getattr(request.user, 'role', '') == 'admin'
        else:
            request.is_admin = False
        return self.get_response(request)
