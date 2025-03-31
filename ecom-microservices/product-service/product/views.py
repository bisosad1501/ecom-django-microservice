from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from django.db.models import Q
from .models import Product, ProductStatus
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
import requests
from django.conf import settings


class ProductViewSet(viewsets.ModelViewSet):
    """
    API quản lý sản phẩm với đầy đủ CRUD và các phương thức bổ trợ.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Refresh queryset mỗi lần get"""
        return Product.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """Tạo mới sản phẩm."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        self.queryset = self.get_queryset()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        try:
            product_id = ObjectId(kwargs.get('pk'))
            product = Product.objects.get(_id=product_id)
            product_type = product.product_type

            # Chọn API phù hợp dựa trên product_type
            service_urls = {
                "BOOK": f"{settings.BOOK_SERVICE_URL}/books/{str(product._id)}/",
                "SHOE": f"{settings.SHOE_SERVICE_URL}/shoes/{str(product._id)}/",
            }

            extra_data = None  # Khởi tạo biến để lưu dữ liệu chi tiết

            if product_type in service_urls:
                try:
                    response = requests.get(service_urls[product_type])
                    if response.status_code == 200:
                        extra_data = response.json()  # Lưu thông tin chi tiết sản phẩm
                except requests.RequestException as e:
                    print(f"Error fetching {product_type} data: {str(e)}")

            serializer = self.get_serializer(product)
            product_data = serializer.data

            # Nếu có dữ liệu từ service khác, gộp vào response
            if extra_data:
                product_data["details"] = extra_data

            return Response(product_data)

        except (InvalidId, Product.DoesNotExist):
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        """Cập nhật sản phẩm."""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Xóa sản phẩm."""
        product = self.get_object()
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["patch"])
    def update_status(self, request, *args, **kwargs):
        """Cập nhật trạng thái sản phẩm."""
        instance = self.get_object()
        new_status = request.data.get("status")

        if new_status not in [s.value for s in ProductStatus]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = new_status
        instance.save()
        return Response({"message": "Status updated", "status": instance.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    def increase_views(self, request, *args, **kwargs):
        """Tăng số lượt xem sản phẩm."""
        instance = self.get_object()
        instance.total_views += 1
        instance.save()
        return Response({"message": "Views increased", "total_views": instance.total_views}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def filter(self, request):
        """Lọc sản phẩm theo giá, rating."""
        queryset = self.get_queryset()

        try:
            min_price = float(request.query_params.get("min_price", 0))
            max_price = float(request.query_params.get("max_price", float("inf")))
            min_rating = float(request.query_params.get("min_rating", 0))
        except ValueError:
            return Response({"error": "Invalid filter parameters"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = queryset.filter(base_price__gte=min_price, base_price__lte=max_price, rating__gte=min_rating)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def best_sellers(self, request):
        """Lấy danh sách sản phẩm bán chạy nhất."""
        limit = int(request.query_params.get("limit", 10))
        queryset = Product.objects.order_by("-total_sold")[:limit]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def related(self, request, *args, **kwargs):
        """Lấy danh sách sản phẩm liên quan."""
        instance = self.get_object()
        related_products = Product.objects.filter(tags__overlap=instance.tags).exclude(pk=instance.pk)[:5]

        serializer = self.get_serializer(related_products, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Lấy danh sách sản phẩm (có caching)."""
        cache_key = f"product_list_{request.query_params.get('page', 1)}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        return response

    @action(detail=True, methods=["POST"])
    def update_stock(self, request, *args, **kwargs):
        """Cập nhật số lượng tồn kho."""
        product = self.get_object()
        try:
            quantity_change = int(request.data.get("quantity_change", 0))
            product.update_stock(quantity_change)
            return Response({"message": "Stock updated successfully", "new_quantity": product.quantity})
        except (ValueError, TypeError):
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def add_to_wishlist(self, request, *args, **kwargs):
        """Thêm sản phẩm vào wishlist của người dùng."""
        user = request.user
        product = self.get_object()

        wishlist = cache.get(f"wishlist_{user.id}", set())
        wishlist.add(product.id)
        cache.set(f"wishlist_{user.id}", wishlist, timeout=86400)

        return Response({"message": "Product added to wishlist", "wishlist_count": len(wishlist)})

    @action(detail=False, methods=["GET"])
    def latest_products(self, request):
        """Lấy danh sách sản phẩm mới nhất."""
        products = Product.objects.filter(status=ProductStatus.ACTIVE).order_by("-created_at")[:10]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def recommend(self, request):
        """Gợi ý sản phẩm dựa trên lịch sử mua hàng."""
        user = request.user
        past_orders = cache.get(f"user_purchases_{user.id}", set())

        if not past_orders:
            return Response({"message": "No recommendations available"})

        recommended_products = Product.objects.filter(
            Q(category_path__in=past_orders) | Q(tags__overlap=list(past_orders))
        ).exclude(id__in=past_orders)[:10]

        serializer = self.get_serializer(recommended_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def bulk_update(self, request):
        """Cập nhật hàng loạt sản phẩm."""
        data = request.data.get("products", [])
        updated_products = []

        for product_data in data:
            try:
                product = Product.objects.get(pk=product_data["_id"])
                serializer = self.get_serializer(product, data=product_data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    updated_products.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                continue  # Bỏ qua sản phẩm không tồn tại

        return Response({"updated_products": updated_products}, status=status.HTTP_200_OK)

    @api_view(["GET"])
    def check_product_exists(request, product_id):
        """Kiểm tra xem sản phẩm có tồn tại không"""
        exists = Product.objects.filter(_id=product_id).exists()
        return Response({"exists": exists}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def create_book_product(self, request):
        """Tạo sản phẩm sách và thông tin chi tiết của sách"""

        # 1️⃣ Chuẩn bị dữ liệu sản phẩm
        product_data = {
            "sku": request.data.get("sku"),  # 🔹 Mã sản phẩm duy nhất
            "name": request.data.get("name"),
            "product_type": "BOOK",
            "category_path": request.data.get("category_path", []),
            "base_price": request.data.get("base_price"),
            "sale_price": request.data.get("sale_price"),
            "quantity": request.data.get("quantity", 0),
            "low_stock_threshold": request.data.get("low_stock_threshold", 10),  # 🔹 Ngưỡng cảnh báo
            "primary_image": request.data.get("primary_image"),
            "image_urls": request.data.get("image_urls", []),
            "seller_id": request.data.get("seller_id"),
            "vendor_id": request.data.get("vendor_id"),
            "brand": request.data.get("brand"),
            "status": request.data.get("status", "ACTIVE"),
            "weight": request.data.get("weight"),
            "dimensions": request.data.get("dimensions", {}),
            "tags": request.data.get("tags", []),

            # 🔹 **Bổ sung thêm thông tin cần thiết**
            "total_views": 0,  # Ban đầu chưa có lượt xem
            "total_sold": 0,  # Ban đầu chưa bán được sản phẩm nào
            "rating": 0.0,  # Ban đầu chưa có đánh giá
            "review_count": 0,  # Chưa có đánh giá nào
            "last_sold_at": None  # Chưa có lịch sử bán hàng
        }

        # 2️⃣ Tạo sản phẩm trong Product Service
        serializer = self.get_serializer(data=product_data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # 3️⃣ Thêm product_id vào book_data để liên kết với Product
        book_data = {
            "product_id": str(product._id),  # 🔹 Liên kết với `Product`
            "title": request.data.get("name"),
            "authors": request.data.get("authors", []),
            "translator": request.data.get("translator"),
            "publisher": request.data.get("publisher"),
            "publication_date": request.data.get("publication_date"),
            "edition": request.data.get("edition"),
            "series": request.data.get("series"),
            "language": request.data.get("language"),
            "book_format": request.data.get("book_format"),
            "isbn_13": request.data.get("isbn_13"),
            "reading_age": request.data.get("reading_age"),
            "page_count": request.data.get("page_count"),
            "summary": request.data.get("summary"),
            "table_of_contents": request.data.get("table_of_contents", []),
            "sample_url": request.data.get("sample_url")
        }

        # 4️⃣ Gửi request tới Book Service để tạo sách
        try:
            book_response = requests.post(
                f"{settings.BOOK_SERVICE_URL}/books/",
                json=book_data
            )

            if book_response.status_code != 201:
                # Nếu tạo book thất bại, xóa product đã tạo
                product.delete()
                return Response({
                    "error": "Không thể tạo thông tin chi tiết sách",
                    "book_error": book_response.json()
                }, status=status.HTTP_400_BAD_REQUEST)

            # 5️⃣ Trả về thông tin Product + Book
            response_data = {
                "product": serializer.data,
                "book": book_response.json()
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except requests.RequestException as e:
            # Nếu lỗi kết nối, xóa product đã tạo
            product.delete()
            return Response({
                "error": "Lỗi kết nối tới Book Service",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["POST"])
    def create_shoe_product(self, request):
        """Tạo sản phẩm giày và thông tin chi tiết của giày"""

        # 1️⃣ Chuẩn bị dữ liệu sản phẩm
        product_data = {
            "sku": request.data.get("sku"),
            "name": request.data.get("name"),
            "product_type": "SHOE",
            "category_path": request.data.get("category_path", []),
            "base_price": request.data.get("base_price"),
            "sale_price": request.data.get("sale_price"),
            "quantity": request.data.get("quantity", 0),
            "low_stock_threshold": request.data.get("low_stock_threshold", 10),
            "primary_image": request.data.get("primary_image"),
            "image_urls": request.data.get("image_urls", []),
            "seller_id": request.data.get("seller_id"),
            "vendor_id": request.data.get("vendor_id"),
            "brand": request.data.get("brand"),
            "status": request.data.get("status", "ACTIVE"),
            "weight": request.data.get("weight"),
            "dimensions": request.data.get("dimensions", {}),
            "tags": request.data.get("tags", []),
            "total_views": 0,
            "total_sold": 0,
            "rating": 0.0,
            "review_count": 0,
            "last_sold_at": None
        }

        # 2️⃣ Tạo sản phẩm trong Product Service
        serializer = self.get_serializer(data=product_data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # 3️⃣ Chuẩn bị dữ liệu giày
        shoe_data = {
            "product_id": str(product._id),
            "size": request.data.get("size"),
            "color": request.data.get("color"),
            "material": request.data.get("material"),
            "gender": request.data.get("gender"),
            "sport_type": request.data.get("sport_type"),
            "style": request.data.get("style"),
            "closure_type": request.data.get("closure_type"),
            "sole_material": request.data.get("sole_material"),
            "upper_material": request.data.get("upper_material"),
            "waterproof": request.data.get("waterproof", False),
            "breathability": request.data.get("breathability"),
            "recommended_terrain": request.data.get("recommended_terrain"),
            "warranty_period": request.data.get("warranty_period", 12)
        }

        # 4️⃣ Gửi request tới Shoe Service để tạo giày
        try:
            shoe_response = requests.post(
                f"{settings.SHOE_SERVICE_URL}/shoes/",
                json=shoe_data
            )

            if shoe_response.status_code != 201:
                # Nếu tạo shoe thất bại, xóa product đã tạo
                product.delete()
                return Response({
                    "error": "Không thể tạo thông tin chi tiết giày",
                    "shoe_error": shoe_response.json()
                }, status=status.HTTP_400_BAD_REQUEST)

            # 5️⃣ Trả về thông tin Product + Shoe
            response_data = {
                "product": serializer.data,
                "shoe": shoe_response.json()
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except requests.RequestException as e:
            # Nếu lỗi kết nối, xóa product đã tạo
            product.delete()
            return Response({
                "error": "Lỗi kết nối tới Shoe Service",
                "detail": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)