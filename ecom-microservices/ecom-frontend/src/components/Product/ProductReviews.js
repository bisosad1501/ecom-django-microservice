import React, { memo, useState, useCallback } from 'react';
import {
  Box,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  Paper,
  Rating,
  Divider,
  Pagination
} from '@mui/material';
import { ThumbUp as ThumbUpIcon } from '@mui/icons-material';
import { useIntersectionObserver } from '../../hooks/useIntersectionObserver';

// Review item component
const ReviewItem = memo(({ review }) => {
  const [helpful, setHelpful] = useState(false);
  const [helpfulCount, setHelpfulCount] = useState(review.helpful_count || 0);
  
  const handleMarkHelpful = useCallback(() => {
    if (!helpful) {
      setHelpfulCount(prev => prev + 1);
      setHelpful(true);
    }
  }, [helpful]);
  
  // Sử dụng IntersectionObserver cho lazy loading ảnh đánh giá
  const [reviewImagesRef, reviewImagesVisible] = useIntersectionObserver({
    threshold: 0.1,
    triggerOnce: true
  });
  
  return (
    <ListItem divider alignItems="flex-start" sx={{ py: 2 }}>
      <ListItemText
        primary={
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Box display="flex" alignItems="center">
              <Typography variant="subtitle1" sx={{ mr: 2, fontWeight: 'bold' }}>
                {review.user_name}
              </Typography>
              <Rating value={review.rating} readOnly size="small" />
            </Box>
            <Typography variant="body2" color="text.secondary">
              {new Date(review.created_at).toLocaleDateString('vi-VN')}
            </Typography>
          </Box>
        }
        secondary={
          <>
            <Typography variant="body1" sx={{ mt: 1 }}>
              {review.comment}
            </Typography>
            {review.images && review.images.length > 0 && (
              <Box 
                ref={reviewImagesRef}
                sx={{ display: 'flex', gap: 1, mt: 1, flexWrap: 'wrap' }}
              >
                {reviewImagesVisible && review.images.map((image, index) => (
                  <Box
                    key={index}
                    component="img"
                    src={image}
                    alt={`Ảnh đánh giá ${index + 1}`}
                    sx={{ 
                      width: 80, 
                      height: 80, 
                      borderRadius: 1,
                      objectFit: 'cover' 
                    }}
                    loading="lazy"
                  />
                ))}
              </Box>
            )}
            <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
              <Button 
                size="small" 
                startIcon={<ThumbUpIcon />}
                onClick={handleMarkHelpful}
                disabled={helpful}
                color={helpful ? "primary" : "inherit"}
              >
                Hữu ích ({helpfulCount})
              </Button>
              <Button size="small">
                Trả lời
              </Button>
            </Box>
          </>
        }
      />
    </ListItem>
  );
});

// Main component
const ProductReviews = ({ reviews = [] }) => {
  const [page, setPage] = useState(1);
  const reviewsPerPage = 5;
  
  const handleChangePage = useCallback((event, newPage) => {
    setPage(newPage);
    
    // Cuộn trang lên trên khi chuyển trang
    window.scrollTo({
      top: document.getElementById('reviews-section')?.offsetTop - 100 || 0,
      behavior: 'smooth'
    });
  }, []);
  
  // Tính toán reviews hiện tại dựa trên phân trang
  const currentReviews = reviews.slice(
    (page - 1) * reviewsPerPage,
    page * reviewsPerPage
  );
  
  return (
    <Box id="reviews-section">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h6">
          Đánh giá sản phẩm ({reviews.length})
        </Typography>
        <Button variant="outlined" size="small">
          Viết đánh giá
        </Button>
      </Box>
      
      <Divider sx={{ mb: 2 }} />
      
      {reviews.length > 0 ? (
        <>
          <List>
            {currentReviews.map((review) => (
              <ReviewItem key={review.id} review={review} />
            ))}
          </List>
          
          {reviews.length > reviewsPerPage && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
              <Pagination 
                count={Math.ceil(reviews.length / reviewsPerPage)} 
                page={page} 
                onChange={handleChangePage}
                color="primary"
                siblingCount={1}
              />
            </Box>
          )}
        </>
      ) : (
        <Paper variant="outlined" sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="body1" sx={{ mb: 2 }}>
            Sản phẩm này chưa có đánh giá.
          </Typography>
          <Button variant="contained">
            Viết đánh giá đầu tiên
          </Button>
        </Paper>
      )}
    </Box>
  );
};

export default memo(ProductReviews); 