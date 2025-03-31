import random
import uuid
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from reviews.models import VerifiedReview, GeneralReview

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho review service'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100, help='Số lượng review tạo mới')
        parser.add_argument('--products', type=int, default=10, help='Số lượng sản phẩm')
        parser.add_argument('--users', type=int, default=20, help='Số lượng người dùng')
        parser.add_argument('--clear', action='store_true', help='Xóa hết dữ liệu cũ trước khi tạo mới')

    def handle(self, *args, **options):
        count = options['count']
        product_count = options['products']
        user_count = options['users']
        clear_data = options['clear']
        
        # Tạo danh sách sản phẩm
        products = [f"PROD{i:03d}" for i in range(1, product_count + 1)]
        
        # Tạo danh sách người dùng
        users = [uuid.uuid4() for _ in range(user_count)]
        
        # Danh sách các comment cho review tiếng Việt
        positive_comments = [
            "Sản phẩm này rất tốt, tôi rất hài lòng",
            "Chất lượng tuyệt vời, đáng đồng tiền",
            "Giao hàng nhanh, đóng gói cẩn thận",
            "Rất hài lòng, sẽ mua lại lần sau",
            "Sản phẩm vượt quá mong đợi của tôi",
            "Chất lượng cao, giá cả phải chăng",
            "Tuyệt vời, không có gì để phàn nàn",
            "Đúng như mô tả, rất ưng ý",
            "Dịch vụ khách hàng tốt, sản phẩm chất lượng",
            "Mua lần thứ hai và vẫn rất hài lòng",
        ]
        
        neutral_comments = [
            "Sản phẩm tạm được, không có gì đặc biệt",
            "Chất lượng ở mức trung bình",
            "Cũng được, nhưng có thể tốt hơn",
            "Không tệ nhưng cũng không quá xuất sắc",
            "Giao hàng hơi chậm nhưng sản phẩm ổn",
            "Đúng với giá tiền, không nhiều không ít",
            "Tạm chấp nhận được",
            "Có một số điểm tốt, một số điểm chưa tốt",
            "Không như mong đợi nhưng cũng không tệ",
            "Cần cải thiện thêm một chút",
        ]
        
        negative_comments = [
            "Sản phẩm kém chất lượng, không đáng tiền",
            "Thất vọng với sản phẩm này",
            "Không giống như mô tả, cảm thấy bị lừa",
            "Giao hàng chậm, đóng gói cẩu thả",
            "Chất lượng kém, không nên mua",
            "Không hoạt động đúng như quảng cáo",
            "Rất tệ, sẽ không bao giờ mua lại",
            "Phí tiền, chất lượng quá kém",
            "Dịch vụ khách hàng tệ, sản phẩm lỗi",
            "Hàng nhái, không phải hàng chính hãng",
        ]
        
        # Số lượng review đã tạo
        verified_created = 0
        general_created = 0
        
        # Xóa dữ liệu cũ nếu được yêu cầu
        if clear_data:
            self.stdout.write(self.style.WARNING('Đang xóa dữ liệu cũ...'))
            VerifiedReview.objects.all().delete()
            GeneralReview.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Đã xóa dữ liệu cũ'))
        
        # Tạo review mới
        for i in range(count):
            # Quyết định loại review (60% verified, 40% general)
            is_verified = random.random() < 0.6
            
            # Chọn sản phẩm ngẫu nhiên
            product_id = random.choice(products)
            
            # Chọn người dùng ngẫu nhiên kết hợp với timestamp để tránh trùng lặp
            # Mỗi user có thể có nhiều review cho cùng một sản phẩm ở các thời điểm khác nhau
            base_user_id = random.choice(users)
            user_id = uuid.uuid4()  # Tạo ID người dùng duy nhất cho mỗi review
            
            # Tạo ngày giả ngẫu nhiên trong 6 tháng gần đây
            days_ago = random.randint(0, 180)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            seconds_ago = random.randint(0, 59)
            created_date = timezone.now() - timedelta(
                days=days_ago, 
                hours=hours_ago, 
                minutes=minutes_ago,
                seconds=seconds_ago
            )
            
            # Xác định rating (1-5)
            rating = random.randint(1, 5)
            
            # Chọn comment dựa trên rating
            if rating >= 4:
                comment = random.choice(positive_comments) + f" (Review {i+1})"
            elif rating == 3:
                comment = random.choice(neutral_comments) + f" (Review {i+1})"
            else:
                comment = random.choice(negative_comments) + f" (Review {i+1})"
            
            # Tạo tiêu đề
            title = f"Đánh giá sản phẩm {product_id} - {i+1}"
            
            # Tạo các trường chung
            review_data = {
                'product_id': product_id,
                'user_id': user_id,
                'rating': rating,
                'title': title,
                'comment': comment,
                'created_at': created_date,
                'updated_at': created_date,
                'is_anonymous': random.random() < 0.2,  # 20% ẩn danh
                'is_hidden': False,
                'helpful_votes': random.randint(0, 50),
                'not_helpful_votes': random.randint(0, 10),
                'report_count': random.randint(0, 3),
            }
            
            try:
                if is_verified:
                    # Tạo thông tin đơn hàng
                    order_id = f"ORDER{random.randint(1000, 9999)}_{i}"
                    purchase_date = created_date - timedelta(days=random.randint(5, 30))
                    
                    # Thêm các trường cho Verified Review
                    review_data.update({
                        'order_id': order_id,
                        'purchase_date': purchase_date,
                        'quality_rating': random.randint(1, 5),
                        'value_rating': random.randint(1, 5),
                        'shipping_rating': random.randint(1, 5),
                    })
                    
                    # Thêm phản hồi từ người bán cho một số đánh giá (30%)
                    if random.random() < 0.3:
                        review_data.update({
                            'seller_response': 'Cảm ơn bạn đã đánh giá sản phẩm. Chúng tôi rất trân trọng phản hồi của bạn.',
                            'seller_response_date': created_date + timedelta(days=random.randint(1, 7)),
                        })
                    
                    # Tạo Verified Review
                    VerifiedReview.objects.create(**review_data)
                    verified_created += 1
                else:
                    # Tạo General Review
                    GeneralReview.objects.create(**review_data)
                    general_created += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Lỗi khi tạo review: {e}'))
                continue
        
        self.stdout.write(self.style.SUCCESS(f'Đã tạo {verified_created} verified reviews và {general_created} general reviews')) 