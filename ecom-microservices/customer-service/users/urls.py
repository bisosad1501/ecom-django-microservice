
from django.urls import path
from .views import (
    RegisterAPI,
    LoginAPI,
    UserListAPI,
    UserDetailAPI,
    SellerRequestAPI,
    ApproveSellerAPI,
    UploadAvatarAPI,
    SellerListAPI,
    CustomerListAPI,
    UpdateAccountStatusAPI,
    PendingSellerListAPI,
    RefreshTokenAPI,
)

app_name = 'users'

urlpatterns = [
    # Authentication URLs
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('auth/refresh/', RefreshTokenAPI.as_view(), name='refresh_token'),

    # User Management URLs
    path('list/', UserListAPI.as_view(), name='user-list'),
    path('detail/<uuid:user_id>/', UserDetailAPI.as_view(), name='user-detail'),
    path('upload-avatar/', UploadAvatarAPI.as_view(), name='upload-avatar'),

    # Role-based User Lists
    path('sellers/', SellerListAPI.as_view(), name='seller-list'),
    path('customers/', CustomerListAPI.as_view(), name='customer-list'),

    # Seller Management URLs
    path('seller-requests/', SellerRequestAPI.as_view(), name='seller-request'),
    path('seller-requests/pending/', PendingSellerListAPI.as_view(), name='pending-seller-list'),
    path('seller-requests/approve/<uuid:user_id>/', ApproveSellerAPI.as_view(), name='approve-seller'),

    # Account Status Management
    path('status/<uuid:user_id>/', UpdateAccountStatusAPI.as_view(), name='update-account-status'),
]