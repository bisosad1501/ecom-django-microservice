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

class ReviewViewSet(viewsets.ViewSet):
    def get_user_info(self, user_id):
        try:
            user_id_str = str(user_id).strip()
            url = f'http://customer-service:8001/user/detail/{user_id}/'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

    def get_product_info(self, product_id):
        try:
            response = requests.get(
                f'http://book-service:8002/books/detail/{product_id}/',
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
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

        verified = VerifiedReview.objects.filter(product_id=product_id, is_hidden=False).select_related()
        general = GeneralReview.objects.filter(product_id=product_id, is_hidden=False).select_related()

        verified_data = VerifiedReviewSerializer(verified, many=True).data
        general_data = GeneralReviewSerializer(general, many=True).data

        verified_avg = verified.aggregate(Avg('rating'))['rating__avg'] or 0
        general_avg = general.aggregate(Avg('rating'))['rating__avg'] or 0
        verified_count = verified.count()
        general_count = general.count()
        total_reviews = verified_count + general_count
        average_rating = (
            (verified_avg * verified_count) + (general_avg * general_count)
        ) / total_reviews if total_reviews > 0 else 0

        data = {
            'product': product_info,
            'stats': {
                'total_reviews': total_reviews,
                'average_rating': round(average_rating, 2)
            },
            'verified_reviews': verified_data,
            'general_reviews': general_data
        }
        return Response(data)

    @action(detail=False, methods=['POST'])
    def create_review(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')

        user_info = self.get_user_info(user_id)
        if not user_info:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        product_info = self.get_product_info(product_id)
        if not product_info:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        is_verified = self.verify_purchase(user_id, product_id)

        existing_review = GeneralReview.objects.filter(user_id=user_id, product_id=product_id).first()

        if existing_review:
            if is_verified:
                verified_review = VerifiedReview.objects.create(
                    user_id=existing_review.user_id,
                    product_id=existing_review.product_id,
                    rating=existing_review.rating,
                    title=existing_review.title,
                    comment=existing_review.comment,
                    media_urls=existing_review.media_urls,
                    helpful_votes=existing_review.helpful_votes,
                    not_helpful_votes=existing_review.not_helpful_votes,
                    report_count=existing_review.report_count,
                    created_at=existing_review.created_at,
                    updated_at=existing_review.updated_at,
                    is_anonymous=existing_review.is_anonymous,
                    is_hidden=existing_review.is_hidden,
                )
                existing_review.delete()
                return Response(VerifiedReviewSerializer(verified_review).data, status=status.HTTP_200_OK)
            return Response({'error': 'User has already reviewed this product'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = VerifiedReviewSerializer if is_verified else GeneralReviewSerializer
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='user_reviews/(?P<user_id>[^/.]+)')
    def user_reviews(self, request, user_id=None):
        user_info = self.get_user_info(user_id)
        if not user_info:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        verified = VerifiedReview.objects.filter(user_id=user_id, is_hidden=False)
        general = GeneralReview.objects.filter(user_id=user_id, is_hidden=False)

        data = {
            'user': user_info,
            'total_reviews': verified.count() + general.count(),
            'verified_reviews': VerifiedReviewSerializer(verified, many=True).data,
            'general_reviews': GeneralReviewSerializer(general, many=True).data
        }
        return Response(data)

    @action(detail=False, methods=['POST'], url_path='vote/(?P<review_id>[^/.]+)')
    def vote(self, request, review_id=None):
        try:
            review = VerifiedReview.objects.get(pk=review_id)
        except VerifiedReview.DoesNotExist:
            try:
                review = GeneralReview.objects.get(pk=review_id)
            except GeneralReview.DoesNotExist:
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
        try:
            review = VerifiedReview.objects.get(pk=review_id)
        except VerifiedReview.DoesNotExist:
            try:
                review = GeneralReview.objects.get(pk=review_id)
            except GeneralReview.DoesNotExist:
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PATCH'], url_path='update_rating/(?P<review_id>[^/.]+)')
    def update_rating(self, request, review_id=None):
        try:
            review = VerifiedReview.objects.get(pk=review_id)
            serializer_class = VerifiedReviewSerializer
        except VerifiedReview.DoesNotExist:
            try:
                review = GeneralReview.objects.get(pk=review_id)
                serializer_class = GeneralReviewSerializer
            except GeneralReview.DoesNotExist:
                return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

        new_rating = request.data.get('rating')
        if new_rating is None or not (1 <= int(new_rating) <= 5):
            return Response({'error': 'Invalid rating. Must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

        review.rating = new_rating
        review.is_edited = True
        review.save()

        return Response(serializer_class(review).data, status=status.HTTP_200_OK)