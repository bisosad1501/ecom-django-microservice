from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, CustomerProfile, SellerProfile
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    SellerRequestSerializer,
    ApproveSellerSerializer,
    AdminCreateUserSerializer,
    UserProfileSerializer
)
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from uuid import UUID


def convert_uuid_to_str(obj):
    if isinstance(obj, UUID):
        return str(obj)
    return obj


# Permission classes với JWT Token
class TokenRequiredPermission(BasePermission):
    """Base permission class yêu cầu JWT token và xác thực user"""

    def has_permission(self, request, view):
        try:
            jwt_authenticator = JWTAuthentication()
            response = jwt_authenticator.authenticate(request)
            if response is None:
                return False
            user, token = response
            return bool(user and user.is_authenticated)
        except:
            return False


class AdminTokenPermission(TokenRequiredPermission):
    """Permission cho Admin với JWT token"""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == User.Role.ADMIN


class SellerTokenPermission(TokenRequiredPermission):
    """Permission cho Seller với JWT token"""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == User.Role.SELLER


class CustomerTokenPermission(TokenRequiredPermission):
    """Permission cho Customer với JWT token"""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == User.Role.CUSTOMER


# API Views
class LoginAPI(APIView):
    """API Đăng nhập"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            refresh['user_id'] = convert_uuid_to_str(user.id)
            refresh['role'] = user.role
            refresh['login_time'] = str(timezone.now())

            return Response({
                'user': UserSerializer(user).data,
                'user_id': str(user.id),
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class RegisterAPI(APIView):
    """API Đăng ký tài khoản mới"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh['user_id'] = convert_uuid_to_str(user.id)
            refresh['role'] = user.role
            refresh['created_at'] = str(timezone.now())

            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPI(APIView):
    """API Quản lý danh sách người dùng"""
    permission_classes = [AllowAny]

    def get(self, request):
        """Lấy danh sách tất cả người dùng"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailAPI(APIView):
    """API Quản lý thông tin chi tiết người dùng"""
    permission_classes = [TokenRequiredPermission]

    def get_object(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, user_id):
        """Lấy thông tin chi tiết người dùng"""
        user = self.get_object(user_id)
        if not user:
            return Response({"error": "Không tìm thấy người dùng"}, status=status.HTTP_404_NOT_FOUND)

        if user.id != request.user.id and request.user.role != User.Role.ADMIN:
            return Response({"error": "Không có quyền truy cập"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        """Cập nhật thông tin người dùng"""
        user = self.get_object(user_id)
        if not user:
            return Response({"error": "Không tìm thấy người dùng"}, status=status.HTTP_404_NOT_FOUND)

        if user.id != request.user.id and request.user.role != User.Role.ADMIN:
            return Response({"error": "Không có quyền chỉnh sửa"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerRequestAPI(APIView):
    """API Khách hàng gửi yêu cầu trở thành Seller"""
    permission_classes = [CustomerTokenPermission]

    def post(self, request):
        user = request.user
        if user.is_seller_request:
            return Response({"error": "Bạn đã gửi yêu cầu trước đó"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SellerRequestSerializer(user, data={"is_seller_request": True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Yêu cầu đã được gửi thành công"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveSellerAPI(APIView):
    """API Phê duyệt yêu cầu trở thành Seller"""
    permission_classes = [AdminTokenPermission]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if not user.is_seller_request:
                return Response({"error": "Người dùng chưa gửi yêu cầu"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ApproveSellerSerializer(user, data={"role": User.Role.SELLER}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Đã phê duyệt thành công"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "Không tìm thấy người dùng"}, status=status.HTTP_404_NOT_FOUND)


class UploadAvatarAPI(APIView):
    """API Tải lên ảnh đại diện"""
    permission_classes = [TokenRequiredPermission]

    def post(self, request):
        if 'avatar' not in request.FILES:
            return Response({"error": "Không tìm thấy file ảnh"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.avatar = request.FILES['avatar']
        user.save()
        return Response({"message": "Cập nhật ảnh đại diện thành công", "avatar_url": user.avatar.url})


class PendingSellerListAPI(APIView):
    """API Lấy danh sách yêu cầu trở thành Seller đang chờ duyệt"""
    permission_classes = [AdminTokenPermission]

    def get(self, request):
        pending_sellers = User.objects.filter(role=User.Role.CUSTOMER, is_seller_request=True)
        serializer = UserSerializer(pending_sellers, many=True)
        return Response(serializer.data)


class RefreshTokenAPI(APIView):
    """API Làm mới token"""
    permission_classes = [TokenRequiredPermission]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            return Response({'access': str(refresh.access_token)})
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

class SellerListAPI(APIView):
    """API Lấy danh sách người bán"""
    permission_classes = [AdminTokenPermission]

    def get(self, request):
        """Lấy danh sách người bán"""
        sellers = User.objects.filter(role=User.Role.SELLER)
        serializer = UserSerializer(sellers, many=True)
        return Response(serializer.data)


class CustomerListAPI(APIView):
    """API Lấy danh sách khách hàng"""
    permission_classes = [AdminTokenPermission]

    def get(self, request):
        """Lấy danh sách khách hàng"""
        customers = User.objects.filter(role=User.Role.CUSTOMER)
        serializer = UserSerializer(customers, many=True)
        return Response(serializer.data)

class UpdateAccountStatusAPI(APIView):
    """API Cập nhật trạng thái tài khoản"""
    permission_classes = [AdminTokenPermission]

    def post(self, request, user_id):
        """Cập nhật trạng thái tài khoản"""
        try:
            user = User.objects.get(id=user_id)
            new_status = request.data.get('status')

            if new_status not in User.AccountStatus.values:
                return Response(
                    {"error": "Trạng thái không hợp lệ"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.status = new_status
            user.save()
            return Response({
                "message": "Cập nhật trạng thái thành công",
                "status": user.status
            })

        except User.DoesNotExist:
            return Response(
                {"error": "Không tìm thấy người dùng"},
                status=status.HTTP_404_NOT_FOUND
            )