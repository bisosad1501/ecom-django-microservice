from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # User Authentication
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', views.LogoutAPI.as_view(), name='logout'),
    
    # User Management
    path('users/', views.UserListAPI.as_view(), name='user-list'),
    path('users/<uuid:user_id>/', views.UserDetailAPI.as_view(), name='user-detail'),
    path('customers/', views.CustomerListAPI.as_view(), name='customer-list'),
    path('sellers/', views.SellerListAPI.as_view(), name='seller-list'),
    path('sellers/pending/', views.PendingSellerListAPI.as_view(), name='pending-seller-list'),
    
    # Seller Request/Approval
    path('seller-request/', views.SellerRequestAPI.as_view(), name='seller-request'),
    path('seller-approve/<uuid:user_id>/', views.ApproveSellerAPI.as_view(), name='seller-approve'),
    
    # Email & Password
    path('verify-email/', views.EmailVerificationAPI.as_view(), name='verify-email'),
    path('password-reset-request/', views.PasswordResetRequestAPI.as_view(), name='password-reset-request'),
    path('password-reset/', views.PasswordResetConfirmAPI.as_view(), name='password-reset'),
    
    # Two-Factor Authentication
    path('2fa/setup/', views.TwoFactorSetupAPI.as_view(), name='2fa-setup'),
    path('2fa/verify/', views.TwoFactorVerifyAPI.as_view(), name='2fa-verify'),
    
    # Additional functionality
    path('auth/refresh/', views.RefreshTokenAPI.as_view(), name='refresh-token'),
    path('upload-avatar/', views.UploadAvatarAPI.as_view(), name='upload-avatar'),
    path('status/<str:user_id>/', views.UpdateAccountStatusAPI.as_view(), name='update-status'),
    path('check/', views.UserCheckAPI.as_view(), name='user-check'),
    path('roles/', views.UserCheckAPI.as_view(), name='user-roles'),
    
    # New APIs for enhanced functionality
    path('insights/', views.UserInsightsAPI.as_view(), name='user-insights'),
    path('insights/<uuid:user_id>/', views.UserInsightsAPI.as_view(), name='user-insights-detail'),
    path('seller-analytics/', views.SellerAnalyticsAPI.as_view(), name='seller-analytics'),
    path('seller-analytics/<uuid:seller_id>/', views.SellerAnalyticsAPI.as_view(), name='seller-analytics-detail'),
    path('account-security/', views.AccountSecurityAPI.as_view(), name='account-security'),
    path('me/', views.UserProfileAPI.as_view(), name='user-profile'),
]