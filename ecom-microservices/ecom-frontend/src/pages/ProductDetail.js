import React, { useState, useEffect, useCallback, useMemo, lazy, Suspense } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Box,
  Paper,
  Button,
  IconButton,
  Card,
  CardMedia,
  Breadcrumbs,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Tabs,
  Tab,
  Rating,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
  CircularProgress,
  Snackbar,
  Alert
} from '@mui/material';
import {
  ShoppingCart as ShoppingCartIcon,
  Favorite as FavoriteIcon,
  ThumbUp as ThumbUpIcon,
  Facebook as FacebookIcon,
  Twitter as TwitterIcon,
  Pinterest as PinterestIcon,
  WhatsApp as WhatsAppIcon,
  LocalShipping as LocalShippingIcon,
  AssignmentReturn as AssignmentReturnIcon,
  Payment as PaymentIcon,
  Verified as VerifiedIcon
} from '@mui/icons-material';
import { productService } from '../services/api';
import { useCart } from '../contexts/CartContext';
import { useWishlist } from '../hooks/useWishlist';
import { useSnackbar } from '../hooks/useSnackbar';

// Lazy load các component con
const ProductImages = lazy(() => import('../components/Product/ProductImages'));
const ProductInfo = lazy(() => import('../components/Product/ProductInfo'));
const ProductDescription = lazy(() => import('../components/Product/ProductDescription'));
const ProductReviews = lazy(() => import('../components/Product/ProductReviews'));
const ProductDetails = lazy(() => import('../components/Product/ProductDetails'));

// Component hỗ trợ cho tab panel
const CustomTabPanel = React.memo(({ children, value, index, ...other }) => {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`product-tabpanel-${index}`}
      aria-labelledby={`product-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
});

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { isInWishlist, toggleWishlistItem } = useWishlist();
  const { showSnackbar } = useSnackbar();
  
  // States
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reviews, setReviews] = useState([]);
  const [tabValue, setTabValue] = useState(0);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  // Handlers
  const handleCloseSnackbar = useCallback(() => {
    setSnackbar(prev => ({ ...prev, open: false }));
  }, []);

  const handleTabChange = useCallback((event, newValue) => {
    setTabValue(newValue);
  }, []);

  const handleAddToCart = useCallback(async () => {
    if (!product) return;
    
    try {
      await addToCart({
        product_id: product._id,
        quantity: 1,
        product_type: product.product_type
      });
      
      setSnackbar({
        open: true,
        message: 'Đã thêm sản phẩm vào giỏ hàng',
        severity: 'success'
      });
    } catch (error) {
      console.error('Error adding to cart:', error);
      setSnackbar({
        open: true,
        message: 'Không thể thêm vào giỏ hàng. Vui lòng thử lại.',
        severity: 'error'
      });
    }
  }, [product, addToCart]);

  const handleToggleWishlist = useCallback(async () => {
    if (!product) return;
    
    try {
      const result = await toggleWishlistItem(product);
      setSnackbar({
        open: true,
        message: result.message,
        severity: result.success ? 'success' : 'error'
      });
    } catch (error) {
      console.error('Error toggling wishlist:', error);
      setSnackbar({
        open: true,
        message: 'Không thể thực hiện thao tác với danh sách yêu thích',
        severity: 'error'
      });
    }
  }, [product, toggleWishlistItem]);

  // Fetch product and reviews
  useEffect(() => {
    const fetchProductData = async () => {
      setLoading(true);
      setError('');
      
      try {
        // Fetch product details và log kết quả để debug
        console.log('Đang fetch sản phẩm với ID:', id);
        const productResponse = await productService.getProductById(id);
        console.log('Kết quả từ API:', productResponse);
        
        if (productResponse.data) {
          setProduct(productResponse.data);
          console.log('Loại sản phẩm:', productResponse.data.product_type);
          
          // Fetch product reviews
          try {
            const reviewsResponse = await productService.getProductReviews(id);
            setReviews(reviewsResponse.data || []);
          } catch (reviewErr) {
            console.error('Lỗi khi lấy đánh giá:', reviewErr);
            // Không hiển thị lỗi đánh giá cho người dùng, chỉ log
            setReviews([]);
          }
        } else {
          throw new Error('Không có dữ liệu sản phẩm');
        }
      } catch (err) {
        console.error('Lỗi chi tiết khi tải sản phẩm:', err);
        // Hiển thị thông báo lỗi thân thiện hơn cho người dùng
        if (err.response && err.response.status === 404) {
          setError('Không tìm thấy sản phẩm. Sản phẩm có thể đã bị xóa hoặc không tồn tại.');
        } else {
          setError('Không thể tải thông tin sản phẩm. Vui lòng thử lại sau.');
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchProductData();
  }, [id]);

  // Memoized values and components
  const isProductInWishlist = useMemo(() => {
    if (!product) return false;
    return isInWishlist(product._id);
  }, [product, isInWishlist]);

  // Các component nhỏ hơn đã được chuyển sang file riêng

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!product) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <Typography>Không tìm thấy sản phẩm</Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Breadcrumb */}
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 3 }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          Trang chủ
        </Link>
        {product.category_path && product.category_path.length > 0 && (
          <Link 
            to={`/products?category=${product.category_path[0].toLowerCase()}&type=${product.product_type}`} 
            style={{ textDecoration: 'none', color: 'inherit' }}
          >
            {product.category_path[0]}
          </Link>
        )}
        <Typography color="text.primary">{product.name}</Typography>
      </Breadcrumbs>
      
      <Grid container spacing={4}>
        {/* Hình ảnh sản phẩm */}
        <Grid item xs={12} md={6}>
          <Suspense fallback={<Box sx={{ height: 500, display: 'flex', justifyContent: 'center', alignItems: 'center' }}><CircularProgress /></Box>}>
            <ProductImages product={product} />
          </Suspense>
        </Grid>
        
        {/* Thông tin sản phẩm */}
        <Grid item xs={12} md={6}>
          <Suspense fallback={<Box sx={{ height: 500, display: 'flex', justifyContent: 'center', alignItems: 'center' }}><CircularProgress /></Box>}>
            <ProductInfo 
              product={product} 
              isInWishlist={isProductInWishlist}
              onAddToCart={handleAddToCart}
              onToggleWishlist={handleToggleWishlist}
            />
          </Suspense>
        </Grid>
      </Grid>
      
      <Box mt={6}>
        <Paper sx={{ p: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange} sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tab label="Chi tiết sản phẩm" id="tab-0" />
            <Tab label="Thông số kỹ thuật" id="tab-1" />
            <Tab label="Đánh giá" id="tab-2" />
          </Tabs>
          
          <CustomTabPanel value={tabValue} index={0}>
            <Suspense fallback={<CircularProgress />}>
              <ProductDescription product={product} />
            </Suspense>
          </CustomTabPanel>
          
          <CustomTabPanel value={tabValue} index={1}>
            <Suspense fallback={<CircularProgress />}>
              <ProductDetails product={product} />
            </Suspense>
          </CustomTabPanel>
          
          <CustomTabPanel value={tabValue} index={2}>
            <Suspense fallback={<CircularProgress />}>
              <ProductReviews reviews={reviews} />
            </Suspense>
          </CustomTabPanel>
        </Paper>
      </Box>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default React.memo(ProductDetail); 