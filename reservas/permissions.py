from rest_framework import permissions

class IsAuthenticated(permissions.BasePermission):
    """Verifica se usuário está autenticado"""
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'id') and request.user.is_active)

class IsCustomer(permissions.BasePermission):
    """Apenas clientes"""
    def has_permission(self, request, view):
        return (hasattr(request, 'user') and 
                request.user and 
                request.user.user_type == 'customer')

class IsHotelStaff(permissions.BasePermission):
    """Apenas funcionários"""
    def has_permission(self, request, view):
        return (hasattr(request, 'user') and 
                request.user and 
                request.user.user_type == 'staff')

class IsAdmin(permissions.BasePermission):
    """Apenas administradores"""
    def has_permission(self, request, view):
        return (hasattr(request, 'user') and 
                request.user and 
                request.user.user_type == 'admin')

class IsOwnerOrStaff(permissions.BasePermission):
    """Dono do recurso ou staff/admin"""
    def has_object_permission(self, request, view, obj):
        # Se for staff ou admin, pode acessar
        if request.user.user_type in ['staff', 'admin']:
            return True
        
        # Se for customer, só pode acessar próprios recursos
        if hasattr(obj, 'customer'):
            return obj.customer.id == request.user.id
        elif hasattr(obj, 'user'):
            return obj.user.id == request.user.id
        
        return False