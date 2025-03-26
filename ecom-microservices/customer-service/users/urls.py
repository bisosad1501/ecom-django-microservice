from django.urls import path
from .views import RegisterAPI, LoginAPI, UserListAPI, UserDetailAPI

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='customer-login'),
    path('register/', RegisterAPI.as_view(), name='customer-register'),
    path('list/', UserListAPI.as_view(), name='customer-list'),
    path('detail/<uuid:id>/', UserDetailAPI.as_view(), name='user-detail'),
]
