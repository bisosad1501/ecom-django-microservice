from django.urls import path
from .views import ReviewViewSet

urlpatterns = [
    # Lấy danh sách đánh giá theo sản phẩm
    path('product_reviews/<str:product_id>/',
         ReviewViewSet.as_view({'get': 'product_reviews'}),
         name='product-reviews'),

    # Tạo đánh giá mới
    path('create_review/',
         ReviewViewSet.as_view({'post': 'create_review'}),
         name='create-review'),

    # Lấy danh sách đánh giá theo người dùng
    path('user_reviews/<str:user_id>/',
         ReviewViewSet.as_view({'get': 'user_reviews'}),
         name='user-reviews'),

    # Bình chọn review là hữu ích / không hữu ích
    path('vote/<str:review_id>/',
         ReviewViewSet.as_view({'post': 'vote'}),
         name='vote-review'),

    # Báo cáo review vi phạm
    path('report/<str:review_id>/',
         ReviewViewSet.as_view({'post': 'report'}),
         name='report-review'),

    # Thêm bình luận vào review
    path('add_comment/<str:review_id>/',
         ReviewViewSet.as_view({'post': 'add_comment'}),
         name='add-comment'),

    # Cập nhật rating cho review
    path('update_rating/<str:review_id>/',
         ReviewViewSet.as_view({'patch': 'update_rating'}),
         name='update-rating'),
]