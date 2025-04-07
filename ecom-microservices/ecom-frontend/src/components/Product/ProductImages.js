import React, { useState, useCallback, memo } from 'react';
import {
  Box,
  Card,
  CardMedia,
  Skeleton
} from '@mui/material';
import { useIntersectionObserver } from '../../hooks/useIntersectionObserver';

const ProductImages = ({ product }) => {
  const [mainImage, setMainImage] = useState(product?.primary_image || product?.image_urls?.[0] || '/product-placeholder.jpg');
  const [imageLoaded, setImageLoaded] = useState(false);
  
  // Sử dụng IntersectionObserver để lazy load ảnh
  const [imageRef, isVisible] = useIntersectionObserver({
    threshold: 0.1,
    triggerOnce: true
  });
  
  // Log để debug
  console.log('Thông tin ảnh sản phẩm:', { 
    primary_image: product?.primary_image,
    image_urls: product?.image_urls,
    mainImage
  });
  
  // Xử lý khi chọn một ảnh thu nhỏ
  const handleThumbnailClick = useCallback((imageUrl) => {
    setMainImage(imageUrl);
    setImageLoaded(false);
  }, []);
  
  // Xử lý khi ảnh đã tải xong
  const handleImageLoad = useCallback(() => {
    setImageLoaded(true);
  }, []);
  
  // Xử lý khi có lỗi loading ảnh
  const handleImageError = useCallback(() => {
    console.error('Lỗi khi tải ảnh:', mainImage);
    setImageError(true);
    setImageLoaded(true); // Kết thúc loading state
  }, [mainImage]);
  
  // Tạo mảng ảnh an toàn
  const getProductImages = useCallback(() => {
    if (!product) return [];
    const allImages = [];
    
    // Thêm ảnh chính nếu có
    if (product.primary_image) {
      allImages.push(product.primary_image);
    }
    
    // Thêm các ảnh khác từ mảng image_urls
    if (product.image_urls && Array.isArray(product.image_urls)) {
      // Loại bỏ ảnh chính nếu đã có trong mảng image_urls
      const otherImages = product.image_urls.filter(url => url !== product.primary_image);
      allImages.push(...otherImages);
    }
    
    return allImages.length > 0 ? allImages : ['/product-placeholder.jpg'];
  }, [product]);
  
  const [imageError, setImageError] = useState(false);
  const allImages = getProductImages();
  
  if (!product) {
    return (
      <Card elevation={0} sx={{ border: '1px solid #eee', borderRadius: 2 }}>
        <Skeleton variant="rectangular" height={500} animation="wave" />
      </Card>
    );
  }
  
  return (
    <>
      <Card 
        elevation={0} 
        sx={{ 
          border: '1px solid #eee', 
          borderRadius: 2,
          position: 'relative'
        }}
        ref={imageRef}
      >
        {!imageLoaded && <Skeleton variant="rectangular" height={500} animation="wave" />}
        
        <CardMedia
          component="img"
          height="500"
          image={isVisible ? (imageError ? '/product-placeholder.jpg' : mainImage) : ''}
          alt={product.name}
          sx={{ 
            objectFit: 'contain', 
            p: 2,
            display: imageLoaded ? 'block' : 'none'
          }}
          onLoad={handleImageLoad}
          onError={handleImageError}
          loading="lazy"
        />
      </Card>
      
      {/* Hiển thị các hình ảnh thu nhỏ */}
      {allImages.length > 1 && (
        <Box sx={{ display: 'flex', mt: 2, flexWrap: 'wrap', gap: 1, justifyContent: 'center' }}>
          {allImages.map((url, index) => (
            <Box 
              key={index}
              component="img"
              src={url}
              alt={`${product.name} - góc nhìn ${index + 1}`}
              onClick={() => handleThumbnailClick(url)}
              sx={{ 
                width: 80, 
                height: 80, 
                objectFit: 'cover', 
                border: mainImage === url 
                  ? '2px solid #1976d2' 
                  : '1px solid #eee',
                borderRadius: 1,
                cursor: 'pointer',
                transition: 'border-color 0.2s ease',
                '&:hover': {
                  border: '1px solid #1976d2'
                }
              }}
              onError={(e) => {
                console.error('Lỗi khi tải ảnh thumbnail:', url);
                e.target.src = '/product-placeholder.jpg';
              }}
            />
          ))}
        </Box>
      )}
    </>
  );
};

export default memo(ProductImages); 