import React, { useState, useEffect, useCallback, useMemo, Suspense, lazy } from 'react';
import { Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Button,
  IconButton,
  Skeleton,
  Chip,
  Rating,
  Tabs,
  Tab,
  Alert,
  Snackbar,
  Divider,
  useTheme,
  useMediaQuery
} from '@mui/material';
import { 
  Favorite as FavoriteIcon, 
  FavoriteBorder as FavoriteBorderIcon,
  ShoppingCart as CartIcon,
  ChevronRight as ArrowRightIcon,
  FilterList as FilterIcon
} from '@mui/icons-material';
import { Carousel } from 'react-responsive-carousel';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import { productService, cartService } from '../services/api';
import { useSnackbar } from '../hooks/useSnackbar';
import { useIntersectionObserver } from '../hooks/useIntersectionObserver';
import { useWishlist } from '../hooks/useWishlist';
import { useCart } from '../contexts/CartContext';

// Lazy load các component ít quan trọng hơn
const CategorySection = lazy(() => import('../components/Home/CategorySection'));

// Component ProductCard đã được tách riêng và memo hóa
const ProductCard = React.memo(({ 
  product, 
  onAddToCart, 
  onToggleWishlist, 
  isInWishlist,
  getProductDetailUrl, 
  formatPrice 
}) => {
  return (
    <Card 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column', 
        position: 'relative',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': {
          transform: 'translateY(-5px)',
          boxShadow: 6
        }
      }}
    >
      {product.discount_price && (
        <Chip
          label={`-${Math.round((1 - product.discount_price / product.price) * 100)}%`}
          color="error"
          size="small"
          sx={{ position: 'absolute', top: 10, left: 10, zIndex: 1 }}
        />
      )}
      <IconButton
        sx={{ position: 'absolute', top: 10, right: 10, zIndex: 1 }}
        onClick={() => onToggleWishlist(product.id)}
      >
        {isInWishlist(product.id) ? (
          <FavoriteIcon color="error" />
        ) : (
          <FavoriteBorderIcon />
        )}
      </IconButton>
      <CardMedia
        component={Link}
        to={getProductDetailUrl(product)}
        sx={{
          pt: '100%',
          position: 'relative',
          cursor: 'pointer',
          textDecoration: 'none'
        }}
      >
        <Box
          component="img"
          src={product.image}
          alt={product.name}
          loading="lazy"
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            padding: 1
          }}
        />
      </CardMedia>
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography
          variant="subtitle1"
          component={Link}
          to={getProductDetailUrl(product)}
          sx={{
            textDecoration: 'none',
            color: 'inherit',
            display: 'block',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            fontWeight: 500,
            '&:hover': { color: 'primary.main' }
          }}
        >
          {product.name}
        </Typography>
        {product.author && (
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              mt: 0.5,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap'
            }}
          >
            {product.author}
          </Typography>
        )}
        {product.brand && (
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              mt: 0.5,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap'
            }}
          >
            {product.brand}
          </Typography>
        )}
        <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
          <Rating value={product.rating || 0} precision={0.1} size="small" readOnly />
          {product.rating > 0 && (
            <Typography variant="body2" color="text.secondary" sx={{ ml: 0.5 }}>
              ({product.rating})
            </Typography>
          )}
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
          {product.discount_price ? (
            <>
              <Typography variant="subtitle1" color="primary" fontWeight="bold">
                {formatPrice(product.discount_price)}
              </Typography>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ ml: 1, textDecoration: 'line-through' }}
              >
                {formatPrice(product.price)}
              </Typography>
            </>
          ) : (
            <Typography variant="subtitle1" color="primary" fontWeight="bold">
              {formatPrice(product.price)}
            </Typography>
          )}
        </Box>
      </CardContent>
      <CardActions>
        <Button
          size="small"
          startIcon={<CartIcon />}
          onClick={() => onAddToCart(product)}
          sx={{ ml: 'auto' }}
        >
          Thêm vào giỏ
        </Button>
      </CardActions>
    </Card>
  );
});

// Component cho Skeleton cards
const SkeletonCard = React.memo(() => (
  <Card sx={{ height: '100%' }}>
    <Skeleton variant="rectangular" height={200} animation="wave" />
    <CardContent>
      <Skeleton variant="text" animation="wave" />
      <Skeleton variant="text" width="60%" animation="wave" />
      <Skeleton variant="text" width="40%" animation="wave" />
    </CardContent>
    <CardActions>
      <Skeleton variant="rectangular" width={120} height={36} sx={{ ml: 'auto' }} animation="wave" />
    </CardActions>
  </Card>
));

// Component cho carousel
const FeaturedCarousel = React.memo(({ 
  featuredProducts, 
  formatPrice, 
  getProductDetailUrl 
}) => (
  <Box sx={{ mb: 4 }}>
    <Carousel
      showThumbs={false}
      infiniteLoop
      autoPlay
      interval={5000}
      showStatus={false}
    >
      {featuredProducts.map((product) => (
        <Box key={product.id} sx={{ position: 'relative' }}>
          <Box
            component="img"
            src={product.image}
            alt={product.name}
            sx={{
              width: '100%',
              height: { xs: '200px', sm: '300px', md: '400px' },
              objectFit: 'cover'
            }}
          />
          <Box
            sx={{
              position: 'absolute',
              bottom: 0,
              left: 0,
              right: 0,
              p: { xs: 2, md: 4 },
              background: 'rgba(0,0,0,0.7)',
              color: 'white',
              textAlign: 'left'
            }}
          >
            <Typography variant="h4" component="h2" gutterBottom>
              {product.name}
            </Typography>
            <Typography variant="body1" sx={{ mb: 2, display: { xs: 'none', sm: 'block' } }}>
              {product.description}
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              {product.discount_price ? (
                <>
                  <Typography variant="h6" color="error">
                    {formatPrice(product.discount_price)}
                  </Typography>
                  <Typography variant="body1" sx={{ textDecoration: 'line-through' }}>
                    {formatPrice(product.price)}
                  </Typography>
                </>
              ) : (
                <Typography variant="h6">
                  {formatPrice(product.price)}
                </Typography>
              )}
              <Button
                variant="contained"
                component={Link}
                to={getProductDetailUrl(product)}
                sx={{ ml: 'auto' }}
              >
                Xem chi tiết
              </Button>
            </Box>
          </Box>
        </Box>
      ))}
    </Carousel>
  </Box>
));

// Component cho danh sách sản phẩm
const ProductGrid = React.memo(({ 
  products, 
  loading, 
  renderProductCard, 
  renderSkeletonCard,
  itemsPerRow = { 
    xs: '50%',   // 2 sản phẩm trên 1 hàng với màn hình nhỏ
    sm: '33.333%', // 3 sản phẩm trên 1 hàng với màn hình trung bình
    md: '25%',     // 4 sản phẩm trên 1 hàng với màn hình lớn
    lg: '20%'      // 5 sản phẩm trên 1 hàng với màn hình rất lớn
  },
  count = 8 
}) => (
  <Grid container spacing={3}>
    {loading
      ? Array.from(new Array(count)).map((_, index) => (
          <Grid item key={index} sx={{ width: itemsPerRow }}>
            {renderSkeletonCard(index)}
          </Grid>
        ))
      : products.map((product) => (
          <Grid item key={product.id} sx={{ width: itemsPerRow }}>
            {renderProductCard(product)}
          </Grid>
        ))}
  </Grid>
));

// Component chính trang Home
const Home = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));
  
  // Sử dụng hook tùy chỉnh
  const { 
    snackbar, 
    showSnackbar, 
    hideSnackbar 
  } = useSnackbar();
  
  const { 
    isInWishlist, 
    toggleWishlistItem 
  } = useWishlist();
  
  const { addToCart } = useCart();
  
  // State
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [newArrivals, setNewArrivals] = useState([]);
  const [bestSellers, setBestSellers] = useState([]);
  const [categories, setCategories] = useState([]);
  const [allProducts, setAllProducts] = useState([]);
  const [productsPage, setProductsPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [productsLoading, setProductsLoading] = useState(false);
  const [bookCategory, setBookCategory] = useState(0);

  // Format API response
  const mapApiProductToUIFormat = useCallback((apiProduct) => {
    return {
      id: apiProduct._id || apiProduct.id,
      name: apiProduct.name,
      image: apiProduct.primary_image || '/images/product-placeholder.jpg',
      description: apiProduct.description || '',
      price: apiProduct.base_price,
      discount_price: apiProduct.sale_price,
      rating: apiProduct.rating,
      type: apiProduct.product_type?.toLowerCase() || 'product',
      brand: apiProduct.brand,
    };
  }, []);

  // Tải dữ liệu trang chủ
  useEffect(() => {
    const fetchHomeData = async () => {
      setLoading(true);
      try {
        // Fetch featured products
        const featuredResponse = await productService.getFeaturedProducts();
        if (featuredResponse.data) {
          const products = featuredResponse.data.results || featuredResponse.data;
          setFeaturedProducts(products.map(mapApiProductToUIFormat));
        }

        // Fetch new arrivals
        const newArrivalsResponse = await productService.getNewArrivals();
        if (newArrivalsResponse.data) {
          // Kiểm tra cấu trúc dữ liệu và lấy mảng kết quả
          const products = newArrivalsResponse.data.results || newArrivalsResponse.data;
          setNewArrivals(products.map(mapApiProductToUIFormat));
        }

        // Fetch best sellers
        const bestSellersResponse = await productService.getBestSellers();
        if (bestSellersResponse.data) {
          // Kiểm tra cấu trúc dữ liệu và lấy mảng kết quả
          const products = bestSellersResponse.data.results || bestSellersResponse.data;
          setBestSellers(products.map(mapApiProductToUIFormat));
        }

        // Fetch categories
        const categoriesResponse = await productService.getCategories();
        if (categoriesResponse.data) {
          setCategories(categoriesResponse.data);
        }
        
        // Fetch all products
        fetchAllProducts(1);
      } catch (error) {
        console.error('Error fetching home data:', error);
        setError('Không thể tải dữ liệu. Vui lòng thử lại sau.');
        
        // Initialize with empty arrays instead of dummy data
        setFeaturedProducts([]);
        setNewArrivals([]);
        setBestSellers([]);
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchHomeData();
  }, [mapApiProductToUIFormat]);

  // Tải tất cả sản phẩm từ API
  const fetchAllProducts = useCallback(async (page = 1, limit = 8) => {
    setProductsLoading(true);
    try {
      const response = await productService.getProducts({ page, limit });
      if (response.data) {
        const { results, count, next, previous } = response.data;
        
        // Tính tổng số trang
        const totalPages = Math.ceil(count / limit) || 1;
        setTotalPages(totalPages);
        setProductsPage(page);
        
        // Format sản phẩm
        const formattedProducts = (results || response.data).map(mapApiProductToUIFormat);
        setAllProducts(formattedProducts);
      }
    } catch (error) {
      console.error('Error fetching products:', error);
      setError('Không thể tải danh sách sản phẩm.');
    } finally {
      setProductsLoading(false);
    }
  }, [mapApiProductToUIFormat]);

  const handlePageChange = useCallback((page) => {
    fetchAllProducts(page);
    window.scrollTo({
      top: document.getElementById('all-products-section').offsetTop - 100,
      behavior: 'smooth'
    });
  }, [fetchAllProducts]);

  const handleAddToCart = useCallback(async (product) => {
    try {
      // Lấy user_id từ localStorage
      const userId = localStorage.getItem('userId');
      
      if (!userId) {
        showSnackbar('Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng', {
          severity: 'warning'
        });
        return;
      }
      
      await addToCart({
        product_id: product.id,
        quantity: 1,
        product_type: product.type || 'product'
      });
      
      showSnackbar('Đã thêm vào giỏ hàng', {
        severity: 'success'
      });
    } catch (error) {
      console.error('Lỗi khi thêm vào giỏ hàng:', error);
      showSnackbar('Không thể thêm vào giỏ hàng. Vui lòng thử lại.', {
        severity: 'error'
      });
    }
  }, [addToCart, showSnackbar]);

  const handleToggleWishlist = useCallback((productId) => {
    const product = allProducts.find(p => p.id === productId) || 
                    featuredProducts.find(p => p.id === productId) || 
                    newArrivals.find(p => p.id === productId) || 
                    bestSellers.find(p => p.id === productId);
    
    if (!product) return;
    
    toggleWishlistItem(product).then(result => {
      showSnackbar(result.message, {
        severity: result.success ? 'success' : 'error'
      });
    });
  }, [allProducts, featuredProducts, newArrivals, bestSellers, toggleWishlistItem, showSnackbar]);

  const handleBookCategoryChange = useCallback((event, newValue) => {
    setBookCategory(newValue);
  }, []);

  // Helpers
  const getProductDetailUrl = useCallback((product) => {
    if (!product) return '/';
    return `/products/${product.id}`;
  }, []);

  const formatPrice = useCallback((price) => {
    return price ? price.toLocaleString() + ' VNĐ' : '';
  }, []);

  // Render helpers
  const renderProductCard = useCallback((product) => (
    <ProductCard
      product={product}
      onAddToCart={handleAddToCart}
      onToggleWishlist={handleToggleWishlist}
      isInWishlist={isInWishlist}
      getProductDetailUrl={getProductDetailUrl}
      formatPrice={formatPrice}
    />
  ), [handleAddToCart, handleToggleWishlist, isInWishlist, getProductDetailUrl, formatPrice]);

  const renderSkeletonCard = useCallback(() => <SkeletonCard />, []);

  // IntersectionObserver for lazy loading sections
  const [newArrivalsRef, newArrivalsVisible] = useIntersectionObserver({
    threshold: 0.1,
    rootMargin: '100px',
    triggerOnce: true
  });

  const [bestSellersRef, bestSellersVisible] = useIntersectionObserver({
    threshold: 0.1,
    rootMargin: '100px',
    triggerOnce: true
  });

  return (
    <Box sx={{ 
      background: theme.palette.mode === 'dark' 
        ? 'linear-gradient(45deg, #1a1a1a 0%, #2d2d2d 100%)' 
        : 'linear-gradient(45deg, #f5f5f5 0%, #ffffff 100%)'
    }}>
      {/* Banner Carousel */}
      <FeaturedCarousel 
        featuredProducts={featuredProducts}
        formatPrice={formatPrice}
        getProductDetailUrl={getProductDetailUrl}
      />

      <Container maxWidth="xl">
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Categories */}
        <Suspense fallback={
          <Box sx={{ mb: 6 }}>
            <Skeleton variant="text" width="30%" height={40} />
            <Grid container spacing={2}>
              {Array.from(new Array(6)).map((_, index) => (
                <Grid item xs={6} sm={4} md={4} lg={2} key={index}>
                  <Card sx={{ height: '100%' }}>
                    <Skeleton variant="rectangular" height={140} animation="wave" />
                    <CardContent>
                      <Skeleton variant="text" animation="wave" />
                      <Skeleton variant="text" width="60%" animation="wave" />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        }>
          <CategorySection categories={categories} loading={loading} />
        </Suspense>

        {/* All Products Section */}
        <Box id="all-products-section" sx={{ mb: 6 }}>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            mb: 3,
            borderBottom: `1px solid ${theme.palette.divider}`,
            pb: 1 
          }}>
            <Typography variant="h5" component="h2" fontWeight="bold">
              Tất cả sản phẩm
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Button
                startIcon={<FilterIcon />}
                component={Link}
                to="/products"
              >
                Lọc sản phẩm
              </Button>
              <Button
                endIcon={<ArrowRightIcon />}
                component={Link}
                to="/products"
              >
                Xem tất cả
              </Button>
            </Box>
          </Box>
          
          <ProductGrid
            products={allProducts}
            loading={productsLoading}
            renderProductCard={renderProductCard}
            renderSkeletonCard={renderSkeletonCard}
            count={8}
          />
          
          {/* Pagination */}
          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Box 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: 1,
                  flexWrap: 'wrap',
                  justifyContent: 'center'
                }}
              >
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <Button
                    key={page}
                    variant={productsPage === page ? 'contained' : 'outlined'}
                    onClick={() => handlePageChange(page)}
                    sx={{ minWidth: 40 }}
                  >
                    {page}
                  </Button>
                ))}
              </Box>
            </Box>
          )}
        </Box>

        {/* New Arrivals */}
        <Box ref={newArrivalsRef} sx={{ mb: 6 }}>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            mb: 3,
            borderBottom: `1px solid ${theme.palette.divider}`,
            pb: 1 
          }}>
            <Typography variant="h5" component="h2" fontWeight="bold">
              Sản phẩm mới
            </Typography>
            <Button
              endIcon={<ArrowRightIcon />}
              component={Link}
              to="/products/new"
            >
              Xem tất cả
            </Button>
          </Box>
          
          {newArrivalsVisible && (
            <ProductGrid
              products={newArrivals}
              loading={loading}
              renderProductCard={renderProductCard}
              renderSkeletonCard={renderSkeletonCard}
              count={4}
            />
          )}
        </Box>

        {/* Best Sellers */}
        <Box ref={bestSellersRef} sx={{ mb: 6 }}>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            mb: 3,
            borderBottom: `1px solid ${theme.palette.divider}`,
            pb: 1 
          }}>
            <Typography variant="h5" component="h2" fontWeight="bold">
              Sản phẩm bán chạy
            </Typography>
            <Button
              endIcon={<ArrowRightIcon />}
              component={Link}
              to="/products/bestsellers"
            >
              Xem tất cả
            </Button>
          </Box>
          
          {bestSellersVisible && (
            <ProductGrid
              products={bestSellers}
              loading={loading}
              renderProductCard={renderProductCard}
              renderSkeletonCard={renderSkeletonCard}
              count={4}
            />
          )}
        </Box>
      </Container>

      {/* Snackbar notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={hideSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={hideSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Home; 