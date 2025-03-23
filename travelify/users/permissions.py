from rest_framework.permissions import BasePermission

class IsGeneralUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'general_user'
    
class IsTravelEnthusiast(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'travel_enthusiast'