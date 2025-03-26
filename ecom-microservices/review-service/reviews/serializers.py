from rest_framework import serializers
from django.utils import timezone
from .models import VerifiedReview, GeneralReview, ReviewComment

class BaseReviewSerializer(serializers.ModelSerializer):
    is_edited = serializers.SerializerMethodField()

    def get_is_edited(self, obj):
        return obj.created_at != obj.updated_at

    class Meta:
        fields = [
            'id', 'product_id', 'user_id', 'rating',
            'title', 'comment', 'media_urls',
            'helpful_votes', 'not_helpful_votes', 'report_count',
            'created_at', 'updated_at', 'is_anonymous',
            'is_hidden', 'is_edited'
        ]
        read_only_fields = [
            'helpful_votes', 'not_helpful_votes', 'report_count',
            'created_at', 'updated_at', 'is_hidden'
        ]

class VerifiedReviewSerializer(BaseReviewSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return ReviewCommentSerializer(obj.comments.all(), many=True).data

    class Meta(BaseReviewSerializer.Meta):
        model = VerifiedReview
        fields = BaseReviewSerializer.Meta.fields + [
            'order_id', 'purchase_date',
            'quality_rating', 'value_rating', 'shipping_rating',
            'seller_response', 'seller_response_date', 'comments'
        ]
        read_only_fields = BaseReviewSerializer.Meta.read_only_fields + [
            'seller_response', 'seller_response_date'
        ]

class VerifiedReviewCreateSerializer(VerifiedReviewSerializer):
    class Meta(VerifiedReviewSerializer.Meta):
        read_only_fields = [
            'helpful_votes', 'not_helpful_votes', 'report_count',
            'created_at', 'updated_at', 'is_hidden',
            'seller_response', 'seller_response_date'
        ]

class GeneralReviewSerializer(BaseReviewSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return ReviewCommentSerializer(obj.comments.all(), many=True).data

    class Meta(BaseReviewSerializer.Meta):
        model = GeneralReview
        fields = BaseReviewSerializer.Meta.fields + ['comments']

class GeneralReviewCreateSerializer(GeneralReviewSerializer):
    class Meta(GeneralReviewSerializer.Meta):
        read_only_fields = [
            'helpful_votes', 'not_helpful_votes', 'report_count',
            'created_at', 'updated_at', 'is_hidden'
        ]

class SellerResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedReview
        fields = ['seller_response']

    def update(self, instance, validated_data):
        instance.seller_response = validated_data.get('seller_response')
        instance.seller_response_date = timezone.now()
        instance.save()
        return instance


class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = ['id', 'user_id', 'text', 'created_at', 'verified_review', 'general_review']

    def create(self, validated_data):
        review = self.context.get('review')
        if isinstance(review, VerifiedReview):
            validated_data['verified_review'] = review
        elif isinstance(review, GeneralReview):
            validated_data['general_review'] = review
        else:
            raise serializers.ValidationError("Invalid review type")

        return super().create(validated_data)