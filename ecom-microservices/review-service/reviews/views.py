from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
import requests

from .models import VerifiedReview, GeneralReview, ReviewComment
from .serializers import (
    VerifiedReviewSerializer,
    GeneralReviewSerializer,
    ReviewCommentSerializer
)

import logging

logger = logging.getLogger(__name__)  # Logger để theo dõi lỗi và request


class ReviewViewSet(viewsets.ViewSet):
    def get_user_info(self, user_id, token):
        try:
            url = f'http://customer-service:8001/user/detail/{user_id}/'
            headers = {'Authorization': f'Bearer {token}'} if token else {}
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                return response.json()
            logger.warning(f"User not found (status: {response.status_code})")
        except requests.RequestException as e:
            logger.error(f"Error fetching user info: {e}", exc_info=True)
        return None

    def get_product_info(self, product_id):
        try:
            response = requests.get(f'http://book-service:8002/books/detail/{product_id}/', timeout=5)
            return response.json() if response.status_code == 200 else None
        except requests.RequestException:
            return None

    def verify_purchase(self, user_id, product_id):
        try:
            response = requests.get(
                f'http://cart-service:8003/orders/verify-purchase/',
                params={'user_id': user_id, 'product_id': product_id},
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    @action(detail=False, methods=['GET'], url_path='product_reviews/(?P<product_id>[^/.]+)')
    def product_reviews(self, request, product_id=None):
        product_info = self.get_product_info(product_id)
        if not product_info:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        verified_reviews = VerifiedReview.objects.filter(product_id=product_id, is_hidden=False)
        general_reviews = GeneralReview.objects.filter(product_id=product_id, is_hidden=False)

        total_reviews = verified_reviews.count() + general_reviews.count()
        average_rating = (
            (verified_reviews.aggregate(Avg('rating'))['rating__avg'] or 0) * verified_reviews.count()
            + (general_reviews.aggregate(Avg('rating'))['rating__avg'] or 0) * general_reviews.count()
        ) / total_reviews if total_reviews > 0 else 0

        return Response({
            'product': product_info,
            'stats': {'total_reviews': total_reviews, 'average_rating': round(average_rating, 2)},
            'verified_reviews': VerifiedReviewSerializer(verified_reviews, many=True).data,
            'general_reviews': GeneralReviewSerializer(general_reviews, many=True).data
        })

    @action(detail=False, methods=['GET'], url_path='user_reviews/(?P<user_id>[^/.]+)')
    def user_reviews(self, request, user_id=None):
        user_token = request.auth or request.headers.get("Authorization", "").split("Bearer ")[-1]
        user_info = self.get_user_info(user_id, user_token)
        if not user_info:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        verified_reviews = VerifiedReview.objects.filter(user_id=user_id, is_hidden=False)
        general_reviews = GeneralReview.objects.filter(user_id=user_id, is_hidden=False)

        return Response({
            'user': user_info,
            'total_reviews': verified_reviews.count() + general_reviews.count(),
            'verified_reviews': VerifiedReviewSerializer(verified_reviews, many=True).data,
            'general_reviews': GeneralReviewSerializer(general_reviews, many=True).data
        })

    @action(detail=False, methods=['POST'], url_path='vote/(?P<review_id>[^/.]+)')
    def vote(self, request, review_id=None):
        review = VerifiedReview.objects.filter(pk=review_id).first() or GeneralReview.objects.filter(pk=review_id).first()
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

        vote_type = request.data.get('vote_type')
        if vote_type == 'helpful':
            review.helpful_votes += 1
        elif vote_type == 'not_helpful':
            review.not_helpful_votes += 1
        else:
            return Response({'error': 'Invalid vote type'}, status=status.HTTP_400_BAD_REQUEST)

        review.save()
        return Response({'status': 'vote recorded'})

    @action(detail=False, methods=['POST'], url_path='report/(?P<review_id>[^/.]+)')
    def report(self, request, review_id=None):
        review = VerifiedReview.objects.filter(pk=review_id).first() or GeneralReview.objects.filter(pk=review_id).first()
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

        review.report_count += 1
        if review.report_count >= 5:
            review.is_hidden = True
        review.save()
        return Response({'status': 'report recorded'})

    @action(detail=False, methods=['POST'], url_path='add_comment/(?P<review_id>[^/.]+)')
    def add_comment(self, request, review_id=None):
        try:
            review = VerifiedReview.objects.get(pk=review_id)
        except VerifiedReview.DoesNotExist:
            try:
                review = GeneralReview.objects.get(pk=review_id)
            except GeneralReview.DoesNotExist:
                return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewCommentSerializer(data=request.data, context={'review': review})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['PATCH'], url_path='update_rating/(?P<review_id>[^/.]+)')
    def update_rating(self, request, review_id=None):
        review = VerifiedReview.objects.filter(pk=review_id).first() or GeneralReview.objects.filter(pk=review_id).first()
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

        new_rating = request.data.get('rating')
        if new_rating is None or not (1 <= int(new_rating) <= 5):
            return Response({'error': 'Invalid rating. Must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

        review.rating = int(new_rating)
        review.is_edited = True
        review.save()

        serializer = VerifiedReviewSerializer(review) if isinstance(review, VerifiedReview) else GeneralReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)