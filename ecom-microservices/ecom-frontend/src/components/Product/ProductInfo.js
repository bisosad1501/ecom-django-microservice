import React, { memo } from 'react';
import {
  Box,
  Typography,
  Divider,
  Chip,
  Button,
  Paper,
  Grid,
  Rating,
  IconButton
} from '@mui/material';
import {
  ShoppingCart as ShoppingCartIcon,
  Favorite as FavoriteIcon,
  FavoriteBorder as FavoriteBorderIcon,
  LocalShipping as LocalShippingIcon,
  AssignmentReturn as AssignmentReturnIcon,
  Payment as PaymentIcon,
  Verified as VerifiedIcon,
  Facebook as FacebookIcon,
  WhatsApp as WhatsAppIcon,
  Pinterest as PinterestIcon,
  Twitter as TwitterIcon
} from '@mui/icons-material';

// Price component memoized
const ProductPrice = memo(({ product }) => {
  const hasDiscount = product.sale_price && product.sale_price < product.base_price;
  
  return (
    <Box sx={{ mb: 3, p: 2, bgcolor: '#f9f9f9', borderRadius: 1 }}>
      {hasDiscount ? (
        <Box sx={{ display: 'flex', alignItems: 'baseline' }}>
          <Typography variant="h4" component="span" color="primary" fontWeight="bold">
            {Number(product.sale_price).toLocaleString()} VNĐ
          </Typography>
          <Typography
            variant="body1"
            component="span"
            sx={{ ml: 2, textDecoration: 'line-through', color: 'text.secondary' }}
          >
            {Number(product.base_price).toLocaleString()} VNĐ
          </Typography>
          <Chip
            label={`-${Math.round((1 - Number(product.sale_price) / Number(product.base_price)) * 100)}%`}
            color="error"
            size="small"
            sx={{ ml: 1 }}
          />
        </Box>
      ) : (
        <Typography variant="h4" color="primary" fontWeight="bold">
          {Number(product.base_price).toLocaleString()} VNĐ
        </Typography>
      )}
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        Đã bán: {product.total_sold || 0} | Còn lại: {product.quantity}
      </Typography>
    </Box>
  );
});

// Stock status component memoized
const StockStatus = memo(({ product }) => (
  <Box mb={3} display="flex" alignItems="center">
    <Typography variant="body1" sx={{ mr: 1 }}>Tình trạng:</Typography>
    {product.quantity > 0 ? (
      <Chip 
        label="Còn hàng" 
        color="success" 
        size="small" 
      />
    ) : (
      <Chip 
        label="Hết hàng" 
        color="error" 
        size="small" 
      />
    )}
    {product.status && product.status !== 'ACTIVE' && (
      <Chip 
        label={product.status} 
        color="default" 
        size="small" 
        sx={{ ml: 1 }}
      />
    )}
  </Box>
));

// Policies component memoized
const PurchasePolicies = memo(() => (
  <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
    <Typography variant="subtitle1" gutterBottom fontWeight="bold">
      Chính sách mua hàng
    </Typography>
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <Box display="flex" alignItems="center">
          <LocalShippingIcon color="primary" sx={{ mr: 1 }} />
          <Typography variant="body2">Giao hàng toàn quốc</Typography>
        </Box>
      </Grid>
      <Grid item xs={6}>
        <Box display="flex" alignItems="center">
          <VerifiedIcon color="primary" sx={{ mr: 1 }} />
          <Typography variant="body2">Bảo hành chính hãng</Typography>
        </Box>
      </Grid>
      <Grid item xs={6}>
        <Box display="flex" alignItems="center">
          <AssignmentReturnIcon color="primary" sx={{ mr: 1 }} />
          <Typography variant="body2">Đổi trả trong 7 ngày</Typography>
        </Box>
      </Grid>
      <Grid item xs={6}>
        <Box display="flex" alignItems="center">
          <PaymentIcon color="primary" sx={{ mr: 1 }} />
          <Typography variant="body2">Thanh toán linh hoạt</Typography>
        </Box>
      </Grid>
    </Grid>
  </Paper>
));

// Social sharing component memoized
const SocialSharing = memo(() => (
  <Box display="flex" alignItems="center" mt={2}>
    <Typography variant="body2" sx={{ mr: 2 }}>Chia sẻ:</Typography>
    <Box display="flex" gap={1}>
      <IconButton size="small" sx={{ color: '#3b5998' }}>
        <FacebookIcon />
      </IconButton>
      <IconButton size="small" sx={{ color: '#25D366' }}>
        <WhatsAppIcon />
      </IconButton>
      <IconButton size="small" sx={{ color: '#E60023' }}>
        <PinterestIcon />
      </IconButton>
      <IconButton size="small" sx={{ color: '#1DA1F2' }}>
        <TwitterIcon />
      </IconButton>
    </Box>
  </Box>
));

const ProductInfo = ({ product, isInWishlist, onAddToCart, onToggleWishlist }) => {
  if (!product) return null;

  return (
    <>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        {product.name}
      </Typography>
      
      {/* Mã sản phẩm và đánh giá */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="body2" color="text.secondary">
          Mã SP: {product.sku}
        </Typography>
        <Box display="flex" alignItems="center">
          <Rating value={product.rating || 0} readOnly precision={0.5} />
          <Typography variant="body2" sx={{ ml: 1 }}>
            ({product.review_count || 0} đánh giá)
          </Typography>
        </Box>
      </Box>
      
      <Divider sx={{ mb: 2 }} />
      
      {/* Giá sản phẩm */}
      <ProductPrice product={product} />
      
      {/* Trạng thái của sản phẩm */}
      <StockStatus product={product} />
      
      {/* Thông tin cơ bản */}
      <Box mb={3}>
        {product.brand && (
          <Typography variant="body1" sx={{ mb: 1 }}>
            <strong>Thương hiệu:</strong> {product.brand}
          </Typography>
        )}
        {product.category_path && product.category_path.length > 0 && (
          <Typography variant="body1" sx={{ mb: 1 }}>
            <strong>Danh mục:</strong> {product.category_path.join(' > ')}
          </Typography>
        )}
        {product.weight && (
          <Typography variant="body1" sx={{ mb: 1 }}>
            <strong>Trọng lượng:</strong> {product.weight} kg
          </Typography>
        )}
      </Box>

      {/* Nếu là sách, hiển thị tóm tắt nhanh */}
      {product.product_type === 'BOOK' && product.details && product.details.summary && (
        <Paper variant="outlined" sx={{ p: 2, mb: 3, bgcolor: '#fafafa' }}>
          <Typography variant="subtitle1" gutterBottom fontWeight="bold">
            Tóm tắt nội dung
          </Typography>
          <Typography variant="body2">
            {product.details.summary}
          </Typography>
        </Paper>
      )}
      
      {/* Nút mua hàng và thêm vào giỏ hàng */}
      <Box display="flex" gap={2} mb={4}>
        <Button
          variant="contained"
          size="large"
          startIcon={<ShoppingCartIcon />}
          onClick={onAddToCart}
          disabled={product.quantity <= 0}
          fullWidth
          sx={{ py: 1.5 }}
        >
          Thêm vào giỏ hàng
        </Button>
        <Button 
          variant="outlined" 
          size="large"
          startIcon={isInWishlist ? <FavoriteIcon color="error" /> : <FavoriteBorderIcon />}
          onClick={onToggleWishlist}
          fullWidth
          sx={{ py: 1.5 }}
        >
          {isInWishlist ? 'Đã yêu thích' : 'Thêm vào yêu thích'}
        </Button>
      </Box>

      {/* Chính sách mua hàng */}
      <PurchasePolicies />
      
      {/* Chia sẻ sản phẩm */}
      <SocialSharing />
    </>
  );
};

export default memo(ProductInfo); 