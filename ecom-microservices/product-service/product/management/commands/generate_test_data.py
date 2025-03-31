import random
import uuid
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from product.models import Product, ProductStatus

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho product service'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=20, help='Số lượng sản phẩm tạo mới')
        parser.add_argument('--clear', action='store_true', help='Xóa hết dữ liệu cũ trước khi tạo mới')

    def handle(self, *args, **options):
        count = options['count']
        clear_data = options['clear']
        
        # Xóa dữ liệu cũ nếu được yêu cầu
        if clear_data:
            self.stdout.write(self.style.WARNING('Đang xóa dữ liệu cũ...'))
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Đã xóa dữ liệu cũ'))
        
        # Danh sách loại sản phẩm
        product_types = ["BOOK", "SHOE", "CLOTHING", "ELECTRONICS"]
        
        # Danh sách thương hiệu
        brands = ["BRAND001", "BRAND002", "BRAND003", "BRAND004", "BRAND005"]
        
        # Danh sách tên sản phẩm tiếng Việt
        product_names = [
            "Đắc Nhân Tâm", 
            "Tuổi Trẻ Đáng Giá Bao Nhiêu", 
            "Giày Thể Thao Cao Cấp",
            "Áo Khoác Mùa Đông",
            "Đồng Hồ Thông Minh",
            "Điện Thoại Di Động",
            "Máy Tính Xách Tay",
            "Tai Nghe Không Dây",
            "Bàn Phím Cơ",
            "Chuột Gaming",
            "Bàn Làm Việc",
            "Ghế Công Thái Học",
            "Nồi Cơm Điện",
            "Nồi Chiên Không Dầu",
            "Tủ Lạnh Mini",
            "Máy Lọc Không Khí",
            "Máy Lọc Nước",
            "Sách Lập Trình Python",
            "Truyện Ngắn Nguyễn Nhật Ánh",
            "Từ Điển Anh-Việt"
        ]
        
        # Danh sách mô tả sản phẩm
        descriptions = [
            "Sản phẩm chất lượng cao, được sản xuất từ những nguyên liệu tốt nhất.",
            "Thiết kế hiện đại, phù hợp với mọi lứa tuổi.",
            "Sản phẩm mới nhất của năm 2023, với nhiều tính năng vượt trội.",
            "Bảo hành chính hãng 12 tháng, 1 đổi 1 trong 30 ngày đầu.",
            "Sản phẩm được nhập khẩu trực tiếp từ nước ngoài.",
            "Hàng chính hãng, giá cả phải chăng.",
            "Sản phẩm hot nhất thị trường hiện nay.",
            "Chiết khấu cao cho đơn hàng số lượng lớn.",
            "Sản phẩm được kiểm định chất lượng nghiêm ngặt trước khi đến tay người tiêu dùng.",
            "Giao hàng nhanh chóng, đóng gói cẩn thận."
        ]
        
        # Danh sách danh mục
        categories = [
            "books/fiction", 
            "books/non-fiction", 
            "shoes/sneakers", 
            "shoes/formal",
            "clothing/t-shirts",
            "clothing/jackets",
            "electronics/smartphones",
            "electronics/laptops",
            "electronics/accessories",
            "home/furniture"
        ]
        
        # Danh sách tags
        all_tags = [
            "bestseller", "trending", "sale", "new", "limited", "popular",
            "premium", "budget", "imported", "luxury", "casual", "formal",
            "sport", "compact", "lightweight", "durable", "waterproof", "wireless"
        ]
        
        created_products = 0
        
        for i in range(count):
            try:
                # Tạo ID sản phẩm
                product_id = f"PROD{i+1:03d}"
                
                # Chọn ngẫu nhiên các thuộc tính
                product_type = random.choice(product_types)
                name = random.choice(product_names) + f" {i+1}"
                brand = random.choice(brands)
                category = random.choice(categories)
                description = random.choice(descriptions)
                
                # Tạo ngày giả ngẫu nhiên trong 1 năm gần đây
                days_ago = random.randint(0, 365)
                created_date = timezone.now() - timedelta(days=days_ago)
                
                # Tạo giá cả ngẫu nhiên
                base_price = random.randint(100000, 5000000)  # Giá từ 100k đến 5M VND
                sale_price = base_price * random.uniform(0.7, 0.95) if random.random() < 0.3 else None
                
                # Tạo đánh giá và số lượng
                rating = round(random.uniform(3.0, 5.0), 1)  # Rating từ 3.0 đến 5.0
                rating_count = random.randint(5, 200)
                quantity = random.randint(0, 100)
                total_sold = random.randint(10, 1000)
                total_views = random.randint(100, 5000)
                
                # Chọn tags ngẫu nhiên (2-5 tags)
                num_tags = random.randint(2, 5)
                tags = random.sample(all_tags, num_tags)
                
                # Xác định trạng thái sản phẩm (90% active, 5% pending, 5% inactive)
                status_roll = random.random()
                if status_roll < 0.9:
                    status = ProductStatus.ACTIVE
                elif status_roll < 0.95:
                    status = ProductStatus.PENDING
                else:
                    status = ProductStatus.INACTIVE
                
                # Tạo đặc tính (attributes) ngẫu nhiên dựa trên loại sản phẩm
                attributes = {}
                
                if product_type == "BOOK":
                    attributes = {
                        "author": f"Tác giả {random.randint(1, 10)}",
                        "publisher": f"NXB {random.randint(1, 5)}",
                        "pages": random.randint(100, 500),
                        "language": random.choice(["Vietnamese", "English"]),
                        "isbn": f"978-3-16-{random.randint(100000, 999999)}-{random.randint(0, 9)}"
                    }
                elif product_type == "SHOE":
                    attributes = {
                        "size": random.randint(35, 45),
                        "color": random.choice(["Đen", "Trắng", "Xám", "Xanh dương", "Đỏ"]),
                        "material": random.choice(["Da", "Vải", "Tổng hợp"]),
                        "gender": random.choice(["Nam", "Nữ", "Unisex"])
                    }
                elif product_type == "CLOTHING":
                    attributes = {
                        "size": random.choice(["S", "M", "L", "XL", "XXL"]),
                        "color": random.choice(["Đen", "Trắng", "Xanh", "Đỏ", "Vàng"]),
                        "material": random.choice(["Cotton", "Polyester", "Linen", "Wool"]),
                        "gender": random.choice(["Nam", "Nữ", "Unisex"])
                    }
                elif product_type == "ELECTRONICS":
                    attributes = {
                        "warranty": f"{random.randint(6, 36)} tháng",
                        "power": f"{random.randint(10, 100)}W",
                        "weight": f"{random.uniform(0.5, 5.0):.1f} kg",
                        "color": random.choice(["Đen", "Trắng", "Bạc"])
                    }
                
                # Tạo ảnh sản phẩm giả
                image_urls = [
                    f"https://example.com/images/{product_id}_1.jpg",
                    f"https://example.com/images/{product_id}_2.jpg"
                ]
                
                # Tạo sản phẩm mới
                product = Product.objects.create(
                    _id=product_id,
                    product_type=product_type,
                    name=name,
                    slug=name.lower().replace(" ", "-"),
                    brand=brand,
                    description=description,
                    category_path=category,
                    base_price=base_price,
                    sale_price=sale_price,
                    quantity=quantity,
                    rating=rating,
                    rating_count=rating_count,
                    total_sold=total_sold,
                    total_views=total_views,
                    attributes=attributes,
                    tags=tags,
                    image_urls=image_urls,
                    status=status,
                    created_at=created_date,
                    updated_at=created_date
                )
                
                created_products += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Lỗi khi tạo sản phẩm: {e}'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'Đã tạo {created_products} sản phẩm')) 