from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from bson import ObjectId

from .models import Book
from .serializers import BookListSerializer, BookDetailSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = '_id'  # Sử dụng '_id'

    def get_object(self):
        # Chuyển đổi ObjectId cho MongoDB
        lookup_value = self.kwargs.get(self.lookup_field)
        try:
            object_id = ObjectId(lookup_value)
            return Book.objects.get(_id=object_id)
        except (TypeError, Book.DoesNotExist):
            raise generics.Http404("Sách không tồn tại")

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            # Thêm sách liên quan
            response_data = serializer.data
            response_data['related_books'] = self.get_related_books(instance)

            return Response(response_data)
        except Book.DoesNotExist:
            return Response({
                "error": "Sách không tồn tại"
            }, status=status.HTTP_404_NOT_FOUND)

    def get_related_books(self, book, limit=5):
        related_books = Book.objects.filter(
            category=book.category
        ).exclude(_id=book._id)[:limit]

        return BookListSerializer(related_books, many=True).data

class FeaturedBooksView(generics.ListAPIView):
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Book.objects.filter(
            is_featured=True,
            is_active=True
        )


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [AllowAny]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = '_id'

    def get_object(self):
        # Chuyển đổi ObjectId cho MongoDB
        lookup_value = self.kwargs.get(self.lookup_field)
        try:
            object_id = ObjectId(lookup_value)
            return Book.objects.get(_id=object_id)
        except (TypeError, Book.DoesNotExist):
            raise Http404("Sách không tồn tại")

    def update(self, request, *args, **kwargs):
        try:
            # Lấy instance sách
            instance = self.get_object()

            # Sử dụng serializer với partial=True để cho phép update từng phần
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True
            )

            # Validate dữ liệu
            serializer.is_valid(raise_exception=True)

            # Thực hiện update
            self.perform_update(serializer)

            # Trả về dữ liệu đã update
            return Response(serializer.data)

        except Book.DoesNotExist:
            return Response(
                {"error": "Không tìm thấy sách"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Log lỗi chi tiết
            print("Update Error:", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        # Phương thức này có thể được override để thêm logic tùy chỉnh
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    View xóa sách
    """
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = '_id'
