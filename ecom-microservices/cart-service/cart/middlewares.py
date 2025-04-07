class PathPrefixMiddleware:
    """
    Middleware để xử lý các path prefix trong cart service
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Xử lý cả trường hợp từ API gateway và truy cập trực tiếp
        if request.path.startswith('/api/carts/'):
            # Từ API gateway đến cart service: /api/carts/X -> /cart/X
            request.path = request.path.replace('/api/carts/', '/cart/')
            request.path_info = request.path_info.replace('/api/carts/', '/cart/')
        
        response = self.get_response(request)
        return response 