from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Kiểm tra người dùng có phải là admin hay không
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsSeller(BasePermission):
    """
    Kiểm tra người dùng có phải là seller hay không
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_seller


class IsCustomer(BasePermission):
    """
    Kiểm tra người dùng có phải là customer hay không
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_customer


class IsSelf(BasePermission):
    """
    Kiểm tra người dùng hiện tại có phải là chính người dùng được truy vấn hay không
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
        
    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id')
        if user_id:
            return str(request.user.id) == user_id
        return True  # Nếu không có user_id trong URL, để permission khác kiểm tra


class IsAccountOwner(BasePermission):
    """
    Kiểm tra người dùng hiện tại có phải là chủ sở hữu của tài khoản hay không
    """
    def has_object_permission(self, request, view, obj):
        # Kiểm tra xem obj có phải là User instance hoặc có thuộc tính user không
        if hasattr(obj, 'user'):
            return obj.user.id == request.user.id
        return obj.id == request.user.id


class IsSellerProfileOwner(BasePermission):
    """
    Kiểm tra người dùng hiện tại có phải là chủ sở hữu của seller profile hay không
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user.id == request.user.id
        return False


class IsVerifiedUser(BasePermission):
    """
    Kiểm tra người dùng đã được xác thực email hay chưa
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_verified 