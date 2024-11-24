# throttles.py
from rest_framework.throttling import SimpleRateThrottle

class CustomRoleBasedThrottle(SimpleRateThrottle):
    """
    Custom throttle class with different limits for admins, authenticated users, and anonymous users.
    """
    scope = 'custom'

    def get_cache_key(self, request, view):
        """
        Generate a cache key. Use user ID for authenticated users or IP for anonymous users.
        """
        if request.user.is_authenticated:
            # Authenticated users are throttled based on their user ID
            return f"throttle_{self.scope}_{request.user.id}"
        # Anonymous users are throttled based on their IP address
        return self.get_ident(request)

    def get_rate(self):
        """
        Define different rates based on the user's role.
        """
        # Access the request object indirectly
        if hasattr(self, 'user') and self.user.is_authenticated:
            if self.user.is_staff:
                return '200/minute'  # Admins
            return '20/minute'      # Authenticated users
        return '10/minute'         # Anonymous users

    def allow_request(self, request, view):
        """
        Attach the request object to the throttle class for use in `get_rate`.
        """
        self.user = request.user  # Attach the user object
        return super().allow_request(request, view)
