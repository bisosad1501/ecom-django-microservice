import os
import requests
import json
import random
import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ReviewClient:
    """
    Client để tương tác với Review Service
    """
    
    def __init__(self, base_url=None):
        """
        Khởi tạo client với URL của review service
        
        Args:
            base_url (str, optional): URL cơ sở của review service. 
                                     Mặc định sẽ lấy từ biến môi trường.
        """
        self.base_url = base_url or os.environ.get('REVIEW_SERVICE_URL', 'http://review-service:8004')
        self.timeout = 3  # Giảm thời gian timeout cho requests (giây)
        self.use_mock_data = os.environ.get('USE_MOCK_DATA', 'false').lower() == 'true'
        self.mock_data_size = int(os.environ.get('MOCK_DATA_SIZE', '200'))
        
        # Biến để lưu trữ cache dữ liệu mẫu
        self._mock_products = None
        self._mock_reviews = None
    
    def _build_url(self, endpoint: str) -> str:
        """
        Xây dựng URL đầy đủ cho endpoint
        
        Args:
            endpoint (str): Endpoint để gọi API
            
        Returns:
            str: URL đầy đủ
        """
        # URL format: http://review-service:8004/reviews/endpoint
        return f"{self.base_url}/reviews/{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Xử lý response từ API
        
        Args:
            response (requests.Response): Response từ request
            
        Returns:
            Dict[str, Any]: Dữ liệu JSON từ response
            
        Raises:
            Exception: Nếu request thất bại
        """
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = f"Request failed with status code {response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f": {error_detail.get('detail', '')}"
            except:
                error_msg += f": {response.text}"
            
            raise Exception(error_msg)
    
    def get_product_reviews(self, product_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Lấy danh sách reviews cho một sản phẩm
        
        Args:
            product_id (str): ID của sản phẩm
            limit (int, optional): Số lượng reviews tối đa. Mặc định là 100.
            offset (int, optional): Vị trí bắt đầu. Mặc định là 0.
            
        Returns:
            Dict[str, Any]: Dữ liệu reviews
        """
        # Cập nhật endpoint để khớp với định dạng của review-service
        endpoint = f"product_reviews/{product_id}"
        url = self._build_url(endpoint)
        
        params = {
            'limit': limit,
            'offset': offset
        }
        
        try:
            # Nếu mock data được bật, sử dụng dữ liệu mẫu
            if self.use_mock_data:
                return self._generate_mock_product_reviews(product_id, limit)
                
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.RequestException as e:
            logger.error(f"Error fetching reviews for product {product_id}: {str(e)}")
            
            # Tự động chuyển sang dữ liệu mẫu khi lỗi
            logger.info("Đang tạo dữ liệu mẫu...")
            mock_data = self._generate_mock_product_reviews(product_id, limit)
            return mock_data
    
    def get_user_reviews(self, user_id: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Lấy danh sách reviews của một người dùng
        
        Args:
            user_id (str): ID của người dùng
            limit (int, optional): Số lượng reviews tối đa. Mặc định là 50.
            offset (int, optional): Vị trí bắt đầu. Mặc định là 0.
            
        Returns:
            Dict[str, Any]: Dữ liệu reviews
        """
        # Cập nhật endpoint để khớp với định dạng của review-service
        endpoint = f"user_reviews/{user_id}"
        url = self._build_url(endpoint)
        
        params = {
            'limit': limit,
            'offset': offset
        }
        
        try:
            # Nếu mock data được bật, sử dụng dữ liệu mẫu
            if self.use_mock_data:
                return self._generate_mock_user_reviews(user_id, limit)
                
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.RequestException as e:
            logger.error(f"Error fetching reviews for user {user_id}: {str(e)}")
            
            # Tự động chuyển sang dữ liệu mẫu khi lỗi
            logger.info("Đang tạo dữ liệu mẫu...")
            mock_data = self._generate_mock_user_reviews(user_id, limit)
            return mock_data
    
    def get_review_by_id(self, review_id: str) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin chi tiết của một review
        
        Args:
            review_id (str): ID của review
            
        Returns:
            Optional[Dict[str, Any]]: Dữ liệu review hoặc None nếu không tìm thấy
        """
        # Không có endpoint cụ thể trong review-service cho việc này
        # Tạm thời giữ nguyên để tương thích ngược
        endpoint = f"review/{review_id}"
        url = self._build_url(endpoint)
        
        try:
            # Nếu mock data được bật, sử dụng dữ liệu mẫu
            if self.use_mock_data:
                return self._generate_mock_review(review_id)
                
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 404:
                return None
            return self._handle_response(response)
        except requests.RequestException as e:
            logger.error(f"Error fetching review {review_id}: {str(e)}")
            
            # Tự động chuyển sang dữ liệu mẫu khi lỗi
            return self._generate_mock_review(review_id)
    
    def create_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tạo một review mới
        
        Args:
            review_data (Dict[str, Any]): Dữ liệu review
            
        Returns:
            Dict[str, Any]: Review đã tạo
        """
        # Cập nhật endpoint để khớp với định dạng của review-service
        endpoint = "create_review"
        url = self._build_url(endpoint)
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            if self.use_mock_data:
                # Tạo ID mới cho review
                review_id = str(uuid.uuid4())
                mock_review = {**review_data, "id": review_id, "created_at": datetime.now().isoformat()}
                return mock_review
                
            response = requests.post(
                url, 
                data=json.dumps(review_data),
                headers=headers,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            logger.error(f"Error creating review: {str(e)}")
            
            # Tạo mock review khi lỗi
            review_id = str(uuid.uuid4())
            mock_review = {**review_data, "id": review_id, "created_at": datetime.now().isoformat()}
            return mock_review
    
    def _get_mock_products(self) -> List[str]:
        """
        Tạo danh sách sản phẩm mẫu
        
        Returns:
            List[str]: Danh sách ID sản phẩm
        """
        if self._mock_products is None:
            self._mock_products = [f"PROD{i:03d}" for i in range(1, 6)]
        return self._mock_products
    
    def _generate_mock_reviews(self) -> List[Dict[str, Any]]:
        """
        Tạo danh sách reviews mẫu
        
        Returns:
            List[Dict[str, Any]]: Danh sách reviews
        """
        if self._mock_reviews is not None:
            return self._mock_reviews
            
        reviews = []
        products = self._get_mock_products()
        
        positive_comments = [
            "Sản phẩm này rất tốt, tôi rất hài lòng",
            "Chất lượng tuyệt vời, đáng đồng tiền",
            "Giao hàng nhanh, đóng gói cẩn thận",
            "Rất hài lòng, sẽ mua lại lần sau",
            "Sản phẩm vượt quá mong đợi của tôi"
        ]
        
        neutral_comments = [
            "Sản phẩm tạm được, không có gì đặc biệt",
            "Chất lượng ở mức trung bình",
            "Cũng được, nhưng có thể tốt hơn",
            "Không tệ nhưng cũng không quá xuất sắc",
            "Giao hàng hơi chậm nhưng sản phẩm ổn"
        ]
        
        negative_comments = [
            "Sản phẩm kém chất lượng, không đáng tiền",
            "Thất vọng với sản phẩm này",
            "Không giống như mô tả, cảm thấy bị lừa",
            "Giao hàng chậm, đóng gói cẩu thả",
            "Chất lượng kém, không nên mua"
        ]
        
        for i in range(self.mock_data_size):
            # Quyết định loại review (60% verified, 40% general)
            is_verified = random.random() < 0.6
            
            # Chọn sản phẩm ngẫu nhiên
            product_id = random.choice(products)
            
            # Tạo ID người dùng
            user_id = str(uuid.uuid4())
            
            # Tạo ngày ngẫu nhiên trong 6 tháng gần đây
            days_ago = random.randint(0, 180)
            created_date = datetime.now() - timedelta(days=days_ago)
            
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
            
            # Tạo dữ liệu review
            review = {
                "id": str(uuid.uuid4()),
                "product_id": product_id,
                "user_id": user_id,
                "rating": rating,
                "title": title,
                "comment": comment,
                "created_at": created_date.isoformat(),
                "helpful_votes": random.randint(0, 50),
                "not_helpful_votes": random.randint(0, 10),
                "is_verified": is_verified
            }
            
            # Thêm thông tin cho verified review
            if is_verified:
                review["order_id"] = f"ORDER{random.randint(1000, 9999)}"
                review["purchase_date"] = (created_date - timedelta(days=random.randint(5, 30))).isoformat()
                review["quality_rating"] = random.randint(1, 5)
                review["value_rating"] = random.randint(1, 5)
                review["shipping_rating"] = random.randint(1, 5)
            
            reviews.append(review)
        
        self._mock_reviews = reviews
        logger.info(f"Đã tạo {len(reviews)} reviews mẫu cho {len(products)} sản phẩm.")
        return reviews
    
    def _generate_mock_product_reviews(self, product_id: str, limit: int = 100) -> Dict[str, Any]:
        """
        Tạo dữ liệu mẫu cho reviews của một sản phẩm
        
        Args:
            product_id (str): ID của sản phẩm
            limit (int): Số lượng reviews tối đa
            
        Returns:
            Dict[str, Any]: Dữ liệu reviews mẫu
        """
        all_reviews = self._generate_mock_reviews()
        
        # Lọc reviews theo product_id
        product_reviews = [r for r in all_reviews if r["product_id"] == product_id]
        
        # Chia reviews thành verified và general
        verified_reviews = [r for r in product_reviews if r.get("is_verified", False)]
        general_reviews = [r for r in product_reviews if not r.get("is_verified", False)]
        
        # Giới hạn số lượng reviews
        verified_reviews = verified_reviews[:limit//2]
        general_reviews = general_reviews[:limit - len(verified_reviews)]
        
        # Tính thống kê
        all_product_reviews = verified_reviews + general_reviews
        total_reviews = len(all_product_reviews)
        average_rating = sum(r["rating"] for r in all_product_reviews) / total_reviews if total_reviews > 0 else 0
        
        return {
            "product": {"id": product_id, "name": f"Sản phẩm {product_id}"},
            "stats": {
                "total_reviews": total_reviews,
                "average_rating": round(average_rating, 1)
            },
            "verified_reviews": verified_reviews,
            "general_reviews": general_reviews
        }
    
    def _generate_mock_user_reviews(self, user_id: str, limit: int = 50) -> Dict[str, Any]:
        """
        Tạo dữ liệu mẫu cho reviews của một người dùng
        
        Args:
            user_id (str): ID của người dùng
            limit (int): Số lượng reviews tối đa
            
        Returns:
            Dict[str, Any]: Dữ liệu reviews mẫu
        """
        all_reviews = self._generate_mock_reviews()
        
        # Lọc reviews theo user_id
        user_reviews = [r for r in all_reviews if r["user_id"] == user_id]
        
        # Nếu không có reviews, tạo một số reviews mới
        if not user_reviews:
            products = self._get_mock_products()
            user_reviews = []
            
            for i in range(min(10, limit)):
                product_id = random.choice(products)
                rating = random.randint(1, 5)
                
                review = {
                    "id": str(uuid.uuid4()),
                    "product_id": product_id,
                    "user_id": user_id,
                    "rating": rating,
                    "title": f"Đánh giá của tôi về {product_id}",
                    "comment": f"Đây là đánh giá số {i+1} của tôi",
                    "created_at": (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat(),
                    "helpful_votes": random.randint(0, 20),
                    "not_helpful_votes": random.randint(0, 5),
                    "is_verified": random.random() < 0.7
                }
                
                if review["is_verified"]:
                    review["order_id"] = f"ORDER{random.randint(1000, 9999)}"
                    review["purchase_date"] = (datetime.now() - timedelta(days=random.randint(10, 100))).isoformat()
                    review["quality_rating"] = random.randint(1, 5)
                    review["value_rating"] = random.randint(1, 5)
                    review["shipping_rating"] = random.randint(1, 5)
                
                user_reviews.append(review)
        
        # Chia reviews thành verified và general
        verified_reviews = [r for r in user_reviews if r.get("is_verified", False)]
        general_reviews = [r for r in user_reviews if not r.get("is_verified", False)]
        
        # Giới hạn số lượng reviews
        verified_reviews = verified_reviews[:limit//2]
        general_reviews = general_reviews[:limit - len(verified_reviews)]
        
        return {
            "user": {"id": user_id},
            "total_reviews": len(verified_reviews) + len(general_reviews),
            "verified_reviews": verified_reviews,
            "general_reviews": general_reviews
        }
    
    def _generate_mock_review(self, review_id: str) -> Optional[Dict[str, Any]]:
        """
        Tạo dữ liệu mẫu cho một review cụ thể
        
        Args:
            review_id (str): ID của review
            
        Returns:
            Optional[Dict[str, Any]]: Dữ liệu review mẫu
        """
        all_reviews = self._generate_mock_reviews()
        
        # Tìm review theo ID
        for review in all_reviews:
            if review["id"] == review_id:
                return review
        
        # Nếu không tìm thấy, tạo một review mới
        products = self._get_mock_products()
        product_id = random.choice(products)
        
        review = {
            "id": review_id,
            "product_id": product_id,
            "user_id": str(uuid.uuid4()),
            "rating": random.randint(1, 5),
            "title": f"Đánh giá về {product_id}",
            "comment": "Đây là một đánh giá mẫu được tạo tự động",
            "created_at": datetime.now().isoformat(),
            "helpful_votes": random.randint(0, 20),
            "not_helpful_votes": random.randint(0, 5),
            "is_verified": True,
            "order_id": f"ORDER{random.randint(1000, 9999)}",
            "purchase_date": (datetime.now() - timedelta(days=random.randint(10, 100))).isoformat(),
            "quality_rating": random.randint(1, 5),
            "value_rating": random.randint(1, 5),
            "shipping_rating": random.randint(1, 5)
        }
        
        return review

# Helper function để sử dụng trong module khác
def fetch_reviews(product_id, limit=100):
    """
    Helper function để lấy reviews cho một sản phẩm
    
    Args:
        product_id (str): ID của sản phẩm
        limit (int, optional): Số lượng reviews tối đa. Mặc định là 100.
        
    Returns:
        List[Dict[str, Any]]: Danh sách reviews
    """
    client = ReviewClient()
    response = client.get_product_reviews(product_id, limit=limit)
    
    # Kết hợp cả verified_reviews và general_reviews
    verified_reviews = response.get('verified_reviews', [])
    general_reviews = response.get('general_reviews', [])
    
    # Chuyển đổi các reviews để đảm bảo chúng có cấu trúc đồng nhất
    all_reviews = []
    
    for review in verified_reviews + general_reviews:
        transformed_review = {
            'id': review.get('id'),
            'product_id': review.get('product_id'),
            'user_id': review.get('user_id'),
            'rating': review.get('rating', 0),
            'title': review.get('title', ''),
            'comment': review.get('comment', ''),
            'date': review.get('created_at', datetime.now().isoformat()),
            'is_verified': 'order_id' in review,
            'helpful_votes': review.get('helpful_votes', 0),
            'not_helpful_votes': review.get('not_helpful_votes', 0)
        }
        all_reviews.append(transformed_review)
    
    return all_reviews