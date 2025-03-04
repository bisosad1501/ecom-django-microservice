from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    FeaturedBooksView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # Danh sách sách
    path('list/', BookListView.as_view(), name='book-list'),

    # Chi tiết sách
    path('detail/<str:_id>/', BookDetailView.as_view(), name='book-detail'),

    # Sách nổi bật
    path('featured/', FeaturedBooksView.as_view(), name='featured-books'),

    # Thêm, sửa, xóa sách
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('update/<str:_id>/', BookUpdateView.as_view(), name='book-update'),
    path('delete/<str:_id>/', BookDeleteView.as_view(), name='book-delete'),
]
