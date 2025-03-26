
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
    path('', include('payment.urls')),
    path('', include('shipping.urls')),
]