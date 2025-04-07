import React, { useState, useCallback, memo } from 'react';
import { 
  Card, 
  CardContent, 
  CardMedia, 
  Typography, 
  CardActions, 
  Button, 
  Rating, 
  Box,
  IconButton,
  Skeleton
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import './ProductCard.css';

// Props comparison function để tránh render lại không cần thiết
const areEqual = (prevProps, nextProps) => {
  return (
    prevProps.product.id === nextProps.product.id &&
    prevProps.inWishlist === nextProps.inWishlist &&
    prevProps.product.price === nextProps.product.price
  );
};

const ProductCard = ({ product, onAddToCart, onToggleWishlist, inWishlist }) => {
  const navigate = useNavigate();
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  
  // Chuyển qua trang chi tiết sản phẩm
  const handleProductClick = useCallback(() => {
    navigate(`/products/${product.id}`);
  }, [navigate, product.id]);
  
  // Xử lý thêm vào giỏ hàng với preventDefault để tránh bubbling
  const handleAddToCart = useCallback((event) => {
    event.stopPropagation();
    onAddToCart(product);
  }, [onAddToCart, product]);
  
  // Xử lý thêm vào wishlist
  const handleToggleWishlist = useCallback((event) => {
    event.stopPropagation();
    onToggleWishlist(product);
  }, [onToggleWishlist, product]);

  // Xử lý khi ảnh loaded
  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  // Xử lý khi có lỗi loading ảnh
  const handleImageError = () => {
    setImageError(true);
    setImageLoaded(true); // Kết thúc loading state
  };
  
  // Tính giảm giá nếu có
  const discountPercent = product.originalPrice && product.price < product.originalPrice
    ? Math.round((1 - (product.price / product.originalPrice)) * 100)
    : 0;
  
  return (
    <Card className="product-card">
      <Box className="product-image-container" onClick={handleProductClick}>
        {!imageLoaded && (
          <Skeleton 
            variant="rectangular" 
            height={200} 
            animation="wave" 
            className="product-image-skeleton"
          />
        )}
        
        <CardMedia
          component="img"
          height="200"
          image={imageError ? '/images/placeholder.jpg' : (product.imageUrl || '/images/placeholder.jpg')}
          alt={product.name}
          className="product-image"
          style={{ display: imageLoaded ? 'block' : 'none' }}
          loading="lazy"
          onLoad={handleImageLoad}
          onError={handleImageError}
        />
        
        {discountPercent > 0 && (
          <Box className="product-discount-badge">
            -{discountPercent}%
          </Box>
        )}
      </Box>

      <CardContent sx={{ pb: 0 }} onClick={handleProductClick}>
        <Typography 
          gutterBottom 
          variant="h6" 
          component="div" 
          className="product-title"
        >
          {product.name}
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Rating 
            name="read-only" 
            value={product.rating || 0} 
            precision={0.5} 
            readOnly 
            size="small" 
          />
          <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
            ({product.reviewCount || 0})
          </Typography>
        </Box>
        
        <Typography variant="h6" color="primary">
          {product.price?.toLocaleString('vi-VN')} ₫
          {product.originalPrice && product.originalPrice > product.price && (
            <Typography 
              component="span" 
              variant="body2" 
              color="text.secondary" 
              sx={{ textDecoration: 'line-through', ml: 1 }}
            >
              {product.originalPrice.toLocaleString('vi-VN')} ₫
            </Typography>
          )}
        </Typography>
      </CardContent>
      
      <CardActions className="product-actions">
        <Button 
          size="small" 
          variant="contained" 
          startIcon={<AddShoppingCartIcon />}
          onClick={handleAddToCart}
          className="add-to-cart-button"
        >
          Thêm vào giỏ
        </Button>
        
        <IconButton 
          aria-label="add to wishlist"
          onClick={handleToggleWishlist}
          color={inWishlist ? "error" : "default"}
          className="wishlist-button"
        >
          {inWishlist ? <FavoriteIcon /> : <FavoriteBorderIcon />}
        </IconButton>
      </CardActions>
    </Card>
  );
};

// Export memoized component để tránh render lại không cần thiết
export default memo(ProductCard, areEqual); 