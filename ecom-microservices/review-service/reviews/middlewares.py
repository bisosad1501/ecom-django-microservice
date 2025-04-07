class PathPrefixMiddleware:
    """
    Middleware để xử lý các path prefix trong review service
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Print the original path for debugging
        original_path = request.path
        original_path_info = request.path_info
        
        # Xử lý cả trường hợp từ API gateway và truy cập trực tiếp
        if request.path.startswith('/api/reviews/'):
            request.path = request.path.replace('/api/reviews/', '/reviews/', 1)
            request.path_info = request.path_info.replace('/api/reviews/', '/reviews/', 1)
        elif request.path.startswith('/api/review/'):
            request.path = request.path.replace('/api/review/', '/reviews/', 1)
            request.path_info = request.path_info.replace('/api/review/', '/reviews/', 1)
        
        # Print the modified path for debugging
        print(f"PathPrefixMiddleware: Original path: {original_path} -> Modified path: {request.path}")
        
        response = self.get_response(request)
        return response 