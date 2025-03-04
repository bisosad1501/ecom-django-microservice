from django.urls import path
from .views import (
    CreateCartAPI,
    AddItemToCartView,
    RemoveItemFromCartView,
    GetCartView,
    UpdateCartItemView
)

urlpatterns = [
    # ✅ Tạo giỏ hàng (chưa dùng đến nếu giỏ hàng tự động tạo khi thêm sản phẩm)
    path('cart/create/<uuid:user_id>/', CreateCartAPI.as_view(), name='create-cart'),

    # ✅ Thêm sản phẩm vào giỏ hàng
    path('cart/add-item/', AddItemToCartView.as_view(), name='add-item-to-cart'),

    # ✅ Xóa sản phẩm khỏi giỏ hàng
    path('cart/remove-item/', RemoveItemFromCartView.as_view(), name='remove-item-from-cart'),

    # ✅ Lấy danh sách sản phẩm trong giỏ hàng của user
    path('cart/get/<uuid:user_id>/', GetCartView.as_view(), name='get-cart'),

    # ✅ Cập nhật số lượng sản phẩm trong giỏ hàng
    path('cart/update-item/', UpdateCartItemView.as_view(), name='update-cart-item'),
]