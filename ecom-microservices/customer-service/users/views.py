from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import User, CustomerProfile, SellerProfile, EmailVerification, PasswordReset, LoginHistory, AuditLog
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    LoginSerializer,
    CustomerSerializer,
    SellerSerializer,
    SellerRequestSerializer,
    ApproveSellerSerializer,
    AdminCreateUserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
    TwoFactorSetupSerializer,
    TwoFactorVerifySerializer,
    LogoutSerializer,
    LoginHistorySerializer,
    UserDetailSerializer
)
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from uuid import UUID
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import TokenError
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import socket
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .permissions import IsAdmin, IsSeller, IsCustomer, IsSelf, IsAccountOwner, IsSellerProfileOwner, IsVerifiedUser


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
        return super().has_permission(request, view) and request.user.is_admin


class SellerTokenPermission(TokenRequiredPermission):
    """Permission cho Seller với JWT token"""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_seller


class CustomerTokenPermission(TokenRequiredPermission):
    """Permission cho Customer với JWT token"""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_customer


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the object or an admin
        return obj == request.user or request.user.role == 'admin'


# API Views
class LoginAPI(APIView):
    """API Đăng nhập"""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Kiểm tra trạng thái tài khoản
        if user.status == 'banned':
            return Response({'detail': 'Tài khoản đã bị khóa.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Lưu lịch sử đăng nhập
        LoginHistory.objects.create(
            user=user,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=True
        )
        
        # Cập nhật last_login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Đăng nhập user
        login(request, user)
        
        # Kiểm tra nếu user đã bật 2FA
        if user.is_2fa_enabled:
            return Response({
                'detail': 'Yêu cầu xác thực 2FA',
                'user_id': user.id,
                'requires_2fa': True
            }, status=status.HTTP_200_OK)
        
        # Tạo token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RegisterAPI(generics.CreateAPIView):
    """API Đăng ký tài khoản mới"""
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.status = 'pending'
        user.save()
        
        # Tạo email verification token
        verification = EmailVerification.objects.create(user=user)
        
        # Gửi email xác thực
        self.send_verification_email(user, verification)
        
        # Tạo token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    def send_verification_email(self, user, verification):
        """Gửi email xác thực tài khoản"""
        verify_url = f"{settings.FRONTEND_URL}/verify-email/{verification.token}/"
        context = {
            'user': user,
            'verify_url': verify_url,
            'expiry_hours': settings.EMAIL_VERIFICATION_EXPIRY_HOURS
        }
        html_message = render_to_string('email/verification_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Xác thực tài khoản của bạn',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )


class UserListAPI(generics.ListAPIView):
    """API Quản lý danh sách người dùng"""
    serializer_class = UserSerializer
    '''permission_classes = [IsAdminUser]'''
    queryset = User.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Lọc theo vai trò
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        # Lọc theo trạng thái
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Tìm kiếm
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        return queryset


class UserDetailAPI(generics.RetrieveUpdateAPIView):
    """API Quản lý thông tin chi tiết người dùng"""
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        if user_id == 'me':
            return self.request.user
        return get_object_or_404(User, id=user_id)

    def get(self, request, *args, **kwargs):
        """Lấy thông tin chi tiết người dùng"""
        user = self.get_object()
        serializer = self.get_serializer(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """Cập nhật thông tin người dùng"""
        return self.update(request, *args, **kwargs)


class SellerRequestAPI(APIView):
    """
    🚀 API để yêu cầu trở thành người bán
    
    * Chỉ cho phép người dùng đã xác thực
    * Yêu cầu trở thành người bán từ khách hàng
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        # Kiểm tra user đã là seller chưa
        if user.is_seller:
            return Response(
                {"detail": "Bạn đã là người bán."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Kiểm tra user đã gửi yêu cầu trở thành seller chưa
        if user.is_seller_request:
            return Response(
                {"detail": "Bạn đã gửi yêu cầu trở thành người bán, vui lòng chờ phê duyệt."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Lấy thông tin từ request để lưu các chi tiết yêu cầu
        data = request.data
        
        # Lưu yêu cầu trở thành seller
        user.is_seller_request = True
        user.save()
        
        # Lưu thông tin seller profile cơ bản (chưa active)
        store_name = data.get('store_name', f"{user.username}'s Store")
        business_registration = data.get('business_registration', '')
        store_description = data.get('store_description', '')
        
        seller_profile, created = SellerProfile.objects.get_or_create(
            user=user,
            defaults={
                'store_name': store_name,
                'business_registration_number': business_registration,
                'store_description': store_description
            }
        )
        
        if not created:
            # Cập nhật thông tin nếu profile đã tồn tại
            seller_profile.store_name = store_name
            seller_profile.business_registration_number = business_registration
            seller_profile.store_description = store_description
            seller_profile.save()
        
        # Lưu log
        AuditLog.log_action(
            action_type=AuditLog.ActionType.SELLER_REQUEST,
            actor=user,
            target_user=user,
            description=f"Yêu cầu trở thành người bán của {user.username}",
            request=request,
            new_state={'store_name': store_name}
        )
        
        # Thông báo thành công và thêm thông tin có ích
        estimated_time = timezone.now() + timezone.timedelta(days=2)
        
        return Response({
            "detail": "Đã gửi yêu cầu trở thành người bán thành công.",
            "request_id": str(user.id),
            "status": "pending",
            "submitted_at": timezone.now(),
            "estimated_review_by": estimated_time,
            "store_name": store_name,
            "next_steps": "Yêu cầu của bạn đang được xem xét. Bạn sẽ nhận được email thông báo khi có kết quả."
        }, status=status.HTTP_201_CREATED)


class ApproveSellerAPI(APIView):
    """
    ✅ API phê duyệt/từ chối yêu cầu trở thành người bán
    
    * Chỉ admin mới có quyền sử dụng API này
    * Phê duyệt: is_approve=true, từ chối: is_approve=false
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request, user_id):
        # Lấy thông tin user
        seller_user = get_object_or_404(User, id=user_id)
        
        # Kiểm tra xem user này có phải là seller_request không
        if not seller_user.is_seller_request:
            return Response(
                {"detail": "Người dùng này chưa gửi yêu cầu trở thành người bán."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Lấy thông tin từ request
        is_approve = request.data.get('is_approve', False)
        reason = request.data.get('reason', '')
        
        # Nếu phê duyệt yêu cầu
        if is_approve:
            # Cập nhật vai trò cho user
            seller_user.is_seller = True
            seller_user.is_seller_request = False
            
            # Cập nhật status nếu chưa active
            if seller_user.status == User.Status.PENDING:
                seller_user.status = User.Status.ACTIVE
                
            seller_user.save()
            
            # Kiểm tra và tạo/cập nhật SellerProfile nếu cần
            if not hasattr(seller_user, 'seller_profile'):
                # Tạo profile mặc định cho seller nếu chưa có
                seller_profile = SellerProfile.objects.create(
                    user=seller_user,
                    store_name=f"{seller_user.username}'s Store"
                )
            else:
                # Cập nhật thông tin nếu cần
                seller_profile = seller_user.seller_profile
                seller_profile.save()
            
            # Lưu log hành động phê duyệt
            AuditLog.log_action(
                action_type=AuditLog.ActionType.SELLER_APPROVE,
                actor=request.user,
                target_user=seller_user,
                description=f"Phê duyệt yêu cầu trở thành người bán cho {seller_user.username}",
                request=request,
                previous_state={'is_seller': False, 'is_seller_request': True},
                new_state={'is_seller': True, 'is_seller_request': False}
            )
            
            # Trả về thông tin chi tiết
            return Response({
                "detail": "Đã phê duyệt người dùng thành người bán.",
                "user": {
                    "id": str(seller_user.id),
                    "username": seller_user.username,
                    "email": seller_user.email,
                    "roles": seller_user.get_roles()
                },
                "seller_profile": {
                    "store_name": seller_profile.store_name,
                    "profile_completion": "30%"
                },
                "next_steps": "Người bán nên hoàn thiện thông tin hồ sơ và tải lên các giấy tờ xác minh.",
                "profile_url": f"/seller/profile/{seller_user.id}/edit"
            }, status=status.HTTP_200_OK)
        else:
            # Từ chối yêu cầu
            seller_user.is_seller_request = False
            seller_user.save()
            
            # Lưu log hành động từ chối
            AuditLog.log_action(
                action_type=AuditLog.ActionType.SELLER_REJECT,
                actor=request.user,
                target_user=seller_user,
                description=f"Từ chối yêu cầu trở thành người bán cho {seller_user.username}. Lý do: {reason}",
                request=request,
                previous_state={'is_seller_request': True},
                new_state={'is_seller_request': False}
            )
            
            # Trả về thông tin chi tiết
            return Response({
                "detail": "Đã từ chối yêu cầu trở thành người bán.",
                "user": {
                    "id": str(seller_user.id),
                    "username": seller_user.username,
                    "email": seller_user.email
                },
                "reason": reason,
                "can_reapply": True,
                "reapply_after": timezone.now() + timezone.timedelta(days=30),
                "support_contact": "support@example.com"
            }, status=status.HTTP_200_OK)


class UploadAvatarAPI(APIView):
    """API Tải lên ảnh đại diện"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if 'avatar' not in request.FILES:
            return Response({'detail': 'Không có file được tải lên'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user.avatar = request.FILES['avatar']
        user.save()
        
        return Response({
            'detail': 'Tải lên ảnh đại diện thành công',
            'avatar_url': request.build_absolute_uri(user.avatar.url)
        }, status=status.HTTP_200_OK)


class PendingSellerListAPI(APIView):
    """API Lấy danh sách yêu cầu trở thành Seller đang chờ duyệt"""
    permission_classes = [IsAdminUser]

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


class SellerListAPI(generics.ListAPIView):
    """API Lấy danh sách người bán"""
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Trả về User objects có is_seller=True
        queryset = User.objects.filter(is_seller=True)
        
        # Lọc theo trạng thái
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Tìm kiếm
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        return queryset
    
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class CustomerListAPI(generics.ListAPIView):
    """API Lấy danh sách khách hàng"""
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = User.objects.filter(is_customer=True)
        
        # Lọc theo trạng thái
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Tìm kiếm
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        return queryset
        
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class UpdateAccountStatusAPI(APIView):
    """API Cập nhật trạng thái tài khoản"""
    permission_classes = [IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        status_value = request.data.get('status')
        if status_value not in dict(User.STATUS_CHOICES).keys():
            return Response({'detail': 'Trạng thái không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.status = status_value
        user.save()
        
        return Response({'detail': f'Cập nhật trạng thái tài khoản thành công: {status_value}'}, status=status.HTTP_200_OK)


class LogoutAPI(APIView):
    """API Đăng xuất"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            # Lấy refresh token từ request
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({'detail': 'Đăng xuất thành công'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPI(APIView):
    """API Thay đổi mật khẩu"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Đổi mật khẩu thành công'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPI(APIView):
    """API Yêu cầu đặt lại mật khẩu"""
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            reset = PasswordReset.objects.create(user=user)
            self.send_reset_email(user, reset)
        except User.DoesNotExist:
            # Không trả về lỗi để đảm bảo an toàn thông tin
            pass
        
        return Response({
            'detail': 'Nếu email tồn tại trong hệ thống, chúng tôi đã gửi hướng dẫn đặt lại mật khẩu.'
        }, status=status.HTTP_200_OK)
    
    def send_reset_email(self, user, reset):
        """Gửi email đặt lại mật khẩu"""
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset.token}/"
        context = {
            'user': user,
            'reset_url': reset_url,
            'expiry_hours': settings.PASSWORD_RESET_EXPIRY_HOURS
        }
        html_message = render_to_string('email/password_reset_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Đặt lại mật khẩu',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )


class PasswordResetConfirmAPI(APIView):
    """
    🔑 API đặt lại mật khẩu
    
    * Không yêu cầu xác thực (vì người dùng đang đặt lại mật khẩu)
    * Xác nhận mã đặt lại mật khẩu và cập nhật mật khẩu mới
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Lấy dữ liệu từ request
        token = request.data.get('token')
        password = request.data.get('password')
        password_confirm = request.data.get('password_confirm')
        
        # Kiểm tra token
        if not token:
            return Response(
                {"detail": "Token đặt lại mật khẩu không được cung cấp."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Kiểm tra mật khẩu
        if not password or not password_confirm:
            return Response(
                {"detail": "Vui lòng cung cấp mật khẩu mới và xác nhận mật khẩu."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if password != password_confirm:
            return Response(
                {"detail": "Mật khẩu mới và xác nhận mật khẩu không khớp."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Kiểm tra độ phức tạp của mật khẩu
        if len(password) < 8:
            return Response(
                {"detail": "Mật khẩu phải có ít nhất 8 ký tự."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Tìm token đặt lại mật khẩu
        try:
            password_reset = get_object_or_404(
                PasswordReset, 
                token=token, 
                is_used=False
            )
            
            # Kiểm tra token còn hạn không
            if not password_reset.is_valid():
                return Response(
                    {"detail": "Token đặt lại mật khẩu đã hết hạn."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Lấy user và cập nhật mật khẩu
            user = password_reset.user
            user.set_password(password)
            
            # Lưu thông tin thời gian thay đổi mật khẩu
            if hasattr(user, 'password_last_changed'):
                user.password_last_changed = timezone.now()
                
            user.save()
            
            # Đánh dấu token đã được sử dụng
            password_reset.is_used = True
            password_reset.save()
            
            # Đăng xuất tất cả các thiết bị khác (bằng cách vô hiệu hóa tất cả refresh tokens)
            # Điều này không được thực hiện tại đây vì cần thông tin request
            # Thay vào đó, sẽ cung cấp cảnh báo bảo mật
            
            # Tạo token mới để đăng nhập
            refresh = RefreshToken.for_user(user)
            
            # Ghi log hành động đặt lại mật khẩu
            AuditLog.log_action(
                action_type=AuditLog.ActionType.SECURITY_CHANGE,
                actor=user,
                target_user=user,
                description=f"Đặt lại mật khẩu thành công cho tài khoản {user.username}"
            )
            
            # Ghi log cảnh báo bảo mật
            AuditLog.log_action(
                action_type=AuditLog.ActionType.SECURITY_ALERT,
                actor=user,
                target_user=user,
                description=f"Mật khẩu đã được thay đổi cho tài khoản {user.username}"
            )
            
            # Trả về thông tin đặt lại mật khẩu thành công
            return Response({
                "detail": "Đặt lại mật khẩu thành công!",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                },
                "security_alert": True,
                "other_sessions_active": True,
                "security_recommendations": [
                    "Hãy đăng xuất khỏi tất cả các thiết bị khác nếu bạn không nhận ra yêu cầu này.",
                    "Bật xác thực hai yếu tố để bảo vệ tài khoản của bạn."
                ]
            }, status=status.HTTP_200_OK)
            
        except (ValueError, PasswordReset.DoesNotExist):
            return Response(
                {"detail": "Token đặt lại mật khẩu không hợp lệ hoặc đã được sử dụng."}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class EmailVerificationRequestAPI(APIView):
    """API Yêu cầu gửi lại email xác thực"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        
        if user.is_verified:
            return Response({'detail': 'Tài khoản đã được xác thực'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Tạo token mới
        verification = EmailVerification.objects.create(user=user)
        
        # Gửi email
        verify_url = f"{settings.FRONTEND_URL}/verify-email/{verification.token}/"
        context = {
            'user': user,
            'verify_url': verify_url,
            'expiry_hours': settings.EMAIL_VERIFICATION_EXPIRY_HOURS
        }
        html_message = render_to_string('email/verification_email.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Xác thực tài khoản của bạn',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
        
        return Response({'detail': 'Email xác thực đã được gửi'}, status=status.HTTP_200_OK)


class EmailVerificationAPI(APIView):
    """
    ✉️ API xác thực email
    
    * Không yêu cầu xác thực (vì có thể truy cập từ email)
    * Xác nhận email người dùng bằng token
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Lấy token từ query params
        token = request.query_params.get('token')
        if not token:
            return Response(
                {"detail": "Token xác thực không hợp lệ."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Xác nhận token và user
            verification = get_object_or_404(EmailVerification, token=token, is_used=False)
            
            # Kiểm tra token còn hạn không
            if not verification.is_valid():
                return Response(
                    {"detail": "Token xác thực đã hết hạn."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Cập nhật trạng thái xác thực cho user
            user = verification.user
            user.is_verified = True
            
            # Kích hoạt tài khoản nếu đang ở trạng thái pending
            if user.status == User.Status.PENDING:
                user.status = User.Status.ACTIVE
                
            user.save()
            
            # Đánh dấu token đã được sử dụng
            verification.is_used = True
            verification.save()
            
            # Tạo JWT token để user có thể đăng nhập ngay
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            
            # Ghi log
            AuditLog.log_action(
                action_type=AuditLog.ActionType.USER_UPDATE,
                actor=user,
                target_user=user,
                description=f"Xác minh email thành công cho {user.email}",
                previous_state={'is_verified': False, 'status': User.Status.PENDING},
                new_state={'is_verified': True, 'status': User.Status.ACTIVE}
            )
            
            # Trả về thông tin và token
            return Response({
                "detail": "Xác thực email thành công!",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "status": user.status,
                    "is_verified": user.is_verified,
                    "roles": user.get_roles()
                },
                "tokens": tokens,
                "redirect_url": "/login"
            }, status=status.HTTP_200_OK)
            
        except (ValueError, EmailVerification.DoesNotExist):
            return Response(
                {"detail": "Token xác thực không hợp lệ hoặc đã được sử dụng."}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class TwoFactorSetupAPI(generics.GenericAPIView):
    """API Thiết lập xác thực hai yếu tố"""
    serializer_class = TwoFactorSetupSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.is_2fa_enabled:
            return Response({
                'is_enabled': True
            }, status=status.HTTP_200_OK)
        
        # Tạo secret mới nếu chưa có
        if not user.otp_secret:
            user.generate_otp_secret()
        
        # Tạo QR code
        user.generate_qr_code()
        
        return Response({
            'is_enabled': False,
            'secret': user.otp_secret,
            'qr_code': request.build_absolute_uri(user.otp_qr.url) if user.otp_qr else None
        }, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'is_enabled': user.is_2fa_enabled,
            'detail': '2FA đã được ' + ('bật' if user.is_2fa_enabled else 'tắt')
        }, status=status.HTTP_200_OK)


class TwoFactorVerifyAPI(APIView):
    """API Xác thực OTP"""
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = TwoFactorVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Lưu lịch sử đăng nhập
        LoginHistory.objects.create(
            user=user,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=True
        )
        
        # Tạo token mới
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LoginHistoryAPI(generics.ListAPIView):
    """API Lấy lịch sử đăng nhập"""
    serializer_class = LoginHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LoginHistory.objects.filter(user=self.request.user)


class PendingSellerRequestsAPI(generics.ListAPIView):
    """API lấy danh sách yêu cầu trở thành người bán đang chờ duyệt"""
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return User.objects.filter(is_seller_request=True, role='customer')


class SellerRequestListAPI(generics.ListAPIView):
    """API Lấy danh sách yêu cầu làm người bán"""
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return User.objects.filter(is_seller_request=True, is_seller=False)


class UserCheckAPI(APIView):
    """API Kiểm tra thông tin chi tiết người dùng để debug"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Kiểm tra tất cả các trường có sẵn
        fields = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'role': user.role,
            'status': user.status,
            'is_verified': user.is_verified,
            'is_seller_request': user.is_seller_request,
            'avatar': str(user.avatar) if user.avatar else None,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
        }
        
        # Kiểm tra các trường boolean
        if hasattr(user, 'is_customer'):
            fields['is_customer'] = user.is_customer
        else:
            fields['is_customer'] = 'Field not found'
            
        if hasattr(user, 'is_seller'):
            fields['is_seller'] = user.is_seller
        else:
            fields['is_seller'] = 'Field not found'
            
        if hasattr(user, 'is_admin'):
            fields['is_admin'] = user.is_admin
        else:
            fields['is_admin'] = 'Field not found'
        
        # Kiểm tra phương thức get_roles
        if hasattr(user, 'get_roles'):
            try:
                fields['get_roles'] = user.get_roles()
            except Exception as e:
                fields['get_roles_error'] = str(e)
        else:
            fields['get_roles'] = 'Method not found'
        
        return Response(fields, status=status.HTTP_200_OK)


class UserInsightsAPI(APIView):
    """
    🔍 API để lấy các insights về hành vi người dùng
    
    * Cần quyền Admin hoặc chính người dùng đó
    * Trả về phân tích hành vi mua sắm, sở thích và lịch sử tương tác
    """
    permission_classes = [IsAuthenticated, (IsAdmin | IsSelf)]
    
    def get(self, request, user_id=None):
        # Xác định người dùng cần lấy insights
        if user_id:
            user = get_object_or_404(User, id=user_id)
            # Kiểm tra quyền: Chỉ Admin hoặc chính người dùng mới có thể xem
            if not request.user.is_admin and request.user.id != user.id:
                return Response(
                    {"detail": "Bạn không có quyền xem insights của người dùng này"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            user = request.user
            
        # Kiểm tra và lấy profile người dùng
        if not hasattr(user, 'customer_profile'):
            return Response(
                {"detail": "Người dùng không có customer profile"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        profile = user.customer_profile
        
        # Dữ liệu phân tích
        insights = {
            "user_id": str(user.id),
            "username": user.username,
            
            # Thông tin mua sắm
            "shopping_behaviors": {
                "purchase_frequency": profile.purchase_frequency,
                "avg_order_value": str(profile.avg_order_value),
                "preferred_categories": profile.preferred_categories,
                "preferred_payment": profile.preferred_payment_method,
                "preferred_shipping": profile.preferred_shipping_method,
                "cart_abandonment_rate": profile.cart_abandonment_rate,
                "last_purchase": profile.last_purchase_at,
            },
            
            # Thông tin tương tác
            "engagement": {
                "last_active": profile.last_active,
                "review_activity": {
                    "review_count": profile.review_count,
                    "avg_rating_given": profile.avg_rating,
                },
                "wishlist_count": profile.wishlist_count,
                "marketing_preferences": {
                    "email_subscribed": profile.marketing_emails,
                    "sms_subscribed": profile.sms_notifications,
                }
            },
            
            # Khuyến nghị cho admin
            "recommendations": {
                "churn_risk": profile.churn_risk,
                "customer_segment": profile.customer_type,
                "lifetime_value": str(profile.lifetime_value),
                "potential_interests": profile.preferred_categories[:3] if profile.preferred_categories else [],
                "suggested_offers": self._get_suggested_offers(profile)
            },
            
            # Thông tin về phiếu giảm giá
            "coupon_data": {
                "available_coupons": profile.coupon_count,
                "coupons_used": profile.coupon_usage,
                "special_offers": profile.special_offers
            }
        }
        
        # Ghi log hoạt động
        AuditLog.log_action(
            action_type=AuditLog.ActionType.USER_DATA_ACCESS,
            actor=request.user,
            target_user=user,
            description=f"Truy cập insights của người dùng {user.username}",
            request=request
        )
        
        return Response(insights, status=status.HTTP_200_OK)
    
    def _get_suggested_offers(self, profile):
        """Hàm phụ trợ để đề xuất ưu đãi phù hợp cho người dùng"""
        suggested = []
        
        # Nếu khách hàng có loyalty points cao
        if profile.loyalty_points > 500:
            suggested.append({
                "type": "loyalty_discount",
                "title": "Giảm giá đặc biệt cho khách hàng trung thành",
                "discount": "15%"
            })
            
        # Nếu khách hàng có nguy cơ churn cao
        if profile.churn_risk > 0.6:
            suggested.append({
                "type": "retention_offer",
                "title": "Ưu đãi giữ chân khách hàng",
                "discount": "20%",
                "expiry_days": 7
            })
            
        # Nếu khách hàng có giá trị cao
        if profile.lifetime_value > 10000000:  # 10 triệu VND
            suggested.append({
                "type": "vip_offer",
                "title": "Ưu đãi VIP",
                "perks": ["Miễn phí vận chuyển", "Ưu tiên xử lý", "Quà tặng"]
            })
            
        return suggested


class SellerAnalyticsAPI(APIView):
    """
    📊 API để lấy các chỉ số phân tích chi tiết cho người bán
    
    * Cần quyền Admin hoặc chính người bán đó
    * Trả về các chỉ số hiệu suất, xu hướng và so sánh
    """
    permission_classes = [IsAuthenticated, (IsAdmin | IsSeller)]
    
    def get(self, request, seller_id=None):
        # Xác định người bán cần lấy analytics
        if seller_id:
            seller = get_object_or_404(User, id=seller_id, is_seller=True)
            # Kiểm tra quyền: Chỉ Admin hoặc chính người bán mới có thể xem
            if not request.user.is_admin and request.user.id != seller.id:
                return Response(
                    {"detail": "Bạn không có quyền xem analytics của người bán này"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            if not request.user.is_seller:
                return Response(
                    {"detail": "Bạn không phải là người bán"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            seller = request.user
            
        # Kiểm tra và lấy profile người bán
        if not hasattr(seller, 'seller_profile'):
            return Response(
                {"detail": "Không tìm thấy hồ sơ người bán"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        profile = seller.seller_profile
        
        # Tính toán tỷ lệ chuyển đổi (giả định, sẽ được tính toán từ dữ liệu thực tế)
        conversion_rate = 0.05  # 5% mặc định
        
        # Dữ liệu phân tích
        analytics = {
            "seller_id": str(seller.id),
            "store_name": profile.store_name or f"{seller.username}'s Store",
            
            # Chỉ số kinh doanh
            "business_metrics": {
                "total_sales": str(profile.total_sales),
                "products_count": profile.products_count,
                "total_orders": 0,  # Sẽ lấy từ order service
                "conversion_rate": conversion_rate,
                "return_rate": profile.return_rate,
                "followers": profile.total_followers,
            },
            
            # Chỉ số dịch vụ
            "service_metrics": {
                "store_rating": profile.store_rating,
                "avg_shipping_time": profile.avg_shipping_time,
                "response_time": profile.response_time,
                "reviews_count": profile.total_reviews,
            },
            
            # Trạng thái xác minh
            "verification_status": {
                "identity_verified": profile.is_identity_verified,
                "business_verified": profile.is_business_verified,
            },
            
            # Performance so với trung bình
            "performance_comparison": {
                "sales_vs_average": "above_average",  # Placeholder - sẽ được tính toán từ dữ liệu thực tế
                "rating_vs_average": "average" if 3.5 <= profile.store_rating <= 4.2 else "below_average" if profile.store_rating < 3.5 else "above_average",
                "shipping_vs_average": "needs_improvement" if profile.avg_shipping_time and profile.avg_shipping_time > 3 else "good",
                "response_vs_average": "needs_improvement" if profile.response_time and profile.response_time > 24 else "good",
            },
            
            # Khuyến nghị cải thiện
            "improvement_suggestions": self._get_improvement_suggestions(profile),
            
            # Thông tin hoạt động
            "activity": {
                "last_active": profile.last_active,
                "opened_since": profile.opened_since,
                "account_health": "good" if profile.store_rating >= 4.0 and profile.return_rate < 0.05 else "average" if profile.store_rating >= 3.0 else "needs_improvement"
            }
        }
        
        # Ghi log hoạt động
        AuditLog.log_action(
            action_type=AuditLog.ActionType.SELLER_DATA_ACCESS,
            actor=request.user,
            target_user=seller,
            description=f"Truy cập analytics của người bán {seller.username}",
            request=request
        )
        
        return Response(analytics, status=status.HTTP_200_OK)
    
    def _get_improvement_suggestions(self, profile):
        """Hàm phụ trợ để đề xuất các cải thiện cho người bán"""
        suggestions = []
        
        # Kiểm tra từng chỉ số và đưa ra gợi ý
        if profile.store_rating < 4.0:
            suggestions.append({
                "area": "customer_satisfaction",
                "title": "Cải thiện đánh giá cửa hàng",
                "description": "Đánh giá cửa hàng của bạn thấp hơn mức lý tưởng. Hãy xem xét các đánh giá của khách hàng và cải thiện dịch vụ.",
                "action_url": "/seller/reviews"
            })
            
        if profile.response_time and profile.response_time > 12:
            suggestions.append({
                "area": "customer_service",
                "title": "Cải thiện thời gian phản hồi",
                "description": "Thời gian phản hồi khách hàng của bạn quá dài. Hãy cố gắng trả lời khách hàng nhanh hơn để cải thiện trải nghiệm.",
                "action_url": "/seller/messages"
            })
            
        if profile.avg_shipping_time and profile.avg_shipping_time > 3:
            suggestions.append({
                "area": "logistics",
                "title": "Cải thiện thời gian giao hàng",
                "description": "Thời gian giao hàng trung bình của bạn dài hơn đối thủ. Hãy tối ưu quy trình xử lý đơn hàng và giao hàng.",
                "action_url": "/seller/shipping-settings"
            })
            
        if profile.return_rate > 0.05:  # 5%
            suggestions.append({
                "area": "product_quality",
                "title": "Giảm tỉ lệ hoàn trả",
                "description": "Tỉ lệ hoàn trả của bạn cao hơn mức trung bình. Hãy xem xét lý do khách hàng trả hàng và cải thiện chất lượng sản phẩm.",
                "action_url": "/seller/returns"
            })
            
        if not profile.is_identity_verified or not profile.is_business_verified:
            suggestions.append({
                "area": "verification",
                "title": "Xác minh danh tính và doanh nghiệp",
                "description": "Hoàn thành xác minh để tăng độ tin cậy và tiếp cận nhiều khách hàng hơn.",
                "action_url": "/seller/verification"
            })
        
        return suggestions


class AccountSecurityAPI(APIView):
    """
    🔒 API để lấy thông tin về bảo mật tài khoản
    
    * Cần xác thực
    * Trả về thông tin phiên đăng nhập, thay đổi gần đây và các cảnh báo
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Lấy lịch sử đăng nhập gần đây
        login_history = user.login_history.all()[:5]
        recent_logins = []
        
        for login in login_history:
            recent_logins.append({
                "timestamp": login.login_time,
                "ip_address": login.ip_address,
                "device": login.device,
                "location": login.location,
                "success": login.success
            })
        
        # Lấy lịch sử thay đổi từ AuditLog
        recent_changes = []
        user_changes = AuditLog.objects.filter(
            target_user=user,
            action_type__in=[
                AuditLog.ActionType.USER_UPDATE,
                AuditLog.ActionType.SECURITY_CHANGE,
                AuditLog.ActionType.SELLER_APPROVE
            ]
        )[:5]
        
        for change in user_changes:
            recent_changes.append({
                "timestamp": change.timestamp,
                "action": change.get_action_type_display(),
                "actor": change.actor.username if change.actor else "System",
                "description": change.description
            })
        
        # Xác định các cảnh báo bảo mật
        security_alerts = []
        
        # Kiểm tra 2FA
        if not user.is_2fa_enabled and (user.is_admin or user.is_seller):
            security_alerts.append({
                "level": "warning",
                "message": "Bạn chưa bật xác thực hai yếu tố. Đây là tính năng bảo mật quan trọng cho tài khoản của bạn.",
                "action": "enable_2fa",
                "action_url": "/user/security/2fa"
            })
        
        # Kiểm tra đăng nhập từ địa điểm lạ
        # (giả định logic kiểm tra địa điểm đăng nhập bất thường)
        unusual_logins = login_history.filter(location__isnull=False).exclude(location__in=["Hanoi, Vietnam", "Ho Chi Minh City, Vietnam"])
        if unusual_logins.exists():
            security_alerts.append({
                "level": "high",
                "message": "Phát hiện đăng nhập từ địa điểm bất thường.",
                "action": "review_logins",
                "action_url": "/user/security/login-history"
            })
        
        # Dữ liệu phản hồi
        security_data = {
            "user_id": str(user.id),
            "username": user.username,
            "security_status": "good" if user.is_2fa_enabled else "needs_improvement",
            
            # Thông tin bảo mật
            "security_features": {
                "two_factor_auth": user.is_2fa_enabled,
                "password_last_changed": user.password_last_changed if hasattr(user, 'password_last_changed') else None,
                "recovery_email": user.email,
                "recovery_phone": user.phone
            },
            
            # Lịch sử đăng nhập và thay đổi
            "recent_activity": {
                "login_sessions": recent_logins,
                "recent_changes": recent_changes
            },
            
            # Cảnh báo bảo mật
            "security_alerts": security_alerts
        }
        
        return Response(security_data, status=status.HTTP_200_OK)


class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
        
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)