import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  Breadcrumbs,
  CircularProgress,
  Alert,
  IconButton,
  Drawer,
  useMediaQuery,
  Button,
  useTheme,
  Snackbar
} from '@mui/material';
import {
  FilterList as FilterIcon,
  Search as SearchIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import { productService, cartService } from '../services/api';

// Import các component mới
import ProductFilter from '../components/Product/ProductFilter';
import ProductGrid from '../components/Product/ProductGrid';
import SearchBar from '../components/Forms/SearchBar';

// Import hooks và services
import { useProducts } from '../hooks/useProducts';
import { useWishlist } from '../hooks/useWishlist';
import { useCart } from '../contexts/CartContext';
import { useSnackbar } from '../hooks/useSnackbar';

const PRODUCT_TYPES = [
  { value: 'BOOK', label: 'Sách' },
  { value: 'SHOE', label: 'Giày' },
  { value: 'ELECTRONIC', label: 'Điện tử' },
  { value: 'CLOTHING', label: 'Quần áo' },
  { value: 'HOME_APPLIANCE', label: 'Đồ gia dụng' },
  { value: 'FURNITURE', label: 'Nội thất' },
  { value: 'BEAUTY', label: 'Mỹ phẩm' },
  { value: 'FOOD', label: 'Thực phẩm' },
  { value: 'SPORTS', label: 'Đồ thể thao' },
  { value: 'TOYS', label: 'Đồ chơi' }
];

const ProductList = () => {
  // Hooks
  const theme = useTheme();
  const location = useLocation();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // Custom hooks
  const { 
    snackbar, 
    showSnackbar, 
    hideSnackbar 
  } = useSnackbar();
  
  const { 
    isInWishlist, 
    toggleWishlistItem,
    wishlist 
  } = useWishlist();
  
  const { addToCart } = useCart();
  
  // Local state
  const [drawerOpen, setDrawerOpen] = useState(false);
  
  // Sử dụng custom hook useProducts
  const {
    products,
    loading,
    error,
    totalPages,
    page,
    sort,
    filters,
    searchQuery,
    productType,
    categories,
    brands,
    handleFilterChange,
    handleSortChange,
    handleProductTypeChange,
    handleSearch,
    applyFilters,
    resetFilters,
    handlePageChange,
    fetchProducts,
    fetchCategories,
    fetchBrands
  } = useProducts();

  // Lấy danh mục và thương hiệu khi component mount
  useEffect(() => {
    fetchCategories();
    fetchBrands();
  }, [fetchCategories, fetchBrands]);

  // Xử lý event handlers
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
        product_id: product._id || product.id,
        quantity: 1,
        product_type: product.product_type || productType
      });
      
      showSnackbar('Đã thêm sản phẩm vào giỏ hàng', {
        severity: 'success'
      });
    } catch (error) {
      console.error('Error adding to cart:', error);
      showSnackbar('Không thể thêm sản phẩm vào giỏ hàng. Vui lòng thử lại.', {
        severity: 'error'
      });
    }
  }, [addToCart, productType, showSnackbar]);

  const handleToggleWishlist = useCallback(async (productId) => {
    try {
      const userId = localStorage.getItem('userId');
      if (!userId) {
        showSnackbar('Vui lòng đăng nhập để quản lý danh sách yêu thích', {
          severity: 'warning'
        });
        return;
      }
      
      // Tìm thông tin sản phẩm
      const product = products.find(p => (p._id || p.id) === productId);
      if (!product) return;
      
      // Sử dụng hook toggleWishlistItem để xử lý
      const result = await toggleWishlistItem(product);
      
      showSnackbar(result.message, {
        severity: result.success ? 'success' : 'error'
      });
    } catch (error) {
      console.error('Error toggling wishlist:', error);
      showSnackbar('Không thể cập nhật danh sách yêu thích. Vui lòng thử lại.', {
        severity: 'error'
      });
    }
  }, [products, showSnackbar, toggleWishlistItem]);

  // Các hàm tính toán phức tạp
  const getPageTitle = useMemo(() => {
    if (!productType) return 'Tất cả sản phẩm';
    
    const typeObj = PRODUCT_TYPES.find(type => type.value === productType);
    return typeObj ? typeObj.label : 'Sản phẩm';
  }, [productType]);

  // Toggle drawer
  const toggleDrawer = useCallback((open) => () => {
    setDrawerOpen(open);
  }, []);

  // Render
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 3 }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          Trang chủ
        </Link>
        <Link to="/products" style={{ textDecoration: 'none', color: 'inherit' }}>
          Sản phẩm
        </Link>
        <Typography color="text.primary">{getPageTitle}</Typography>
      </Breadcrumbs>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {/* Search Bar */}
      <Box sx={{ mb: 3 }}>
        <SearchBar
          initialValue={searchQuery}
          onSearch={handleSearch}
          fullWidth
        />
      </Box>
      
      {/* Mobile Filter Button */}
      {isMobile && (
        <Button
          variant="outlined"
          startIcon={<FilterIcon />}
          onClick={toggleDrawer(true)}
          fullWidth
          sx={{ mb: 3 }}
        >
          Lọc và sắp xếp
        </Button>
      )}
      
      {/* Main Content */}
      <Box sx={{ display: 'flex', flexDirection: 'row', gap: 3 }}>
        {/* Filters - Desktop */}
        {!isMobile && (
          <Box 
            sx={{ 
              width: '25%', 
              minWidth: '250px',
              position: 'sticky',
              top: '20px',
              alignSelf: 'flex-start',
              height: 'fit-content'
            }}
          >
            <ProductFilter
              categories={categories}
              brands={brands}
              filters={filters}
              onFilterChange={handleFilterChange}
              onApplyFilters={applyFilters}
              onResetFilters={resetFilters}
              productType={productType}
              onProductTypeChange={handleProductTypeChange}
              sort={sort}
              onSortChange={handleSortChange}
            />
          </Box>
        )}
        
        {/* Products */}
        <Box sx={{ flexGrow: 1 }}>
          <ProductGrid
            products={products}
            loading={loading}
            error={error}
            onAddToCart={handleAddToCart}
            onToggleWishlist={handleToggleWishlist}
            wishlistItems={wishlist || []}
            page={page}
            totalPages={totalPages}
            onPageChange={handlePageChange}
            useVirtualization={products.length > 20}
          />
        </Box>
      </Box>
      
      {/* Filters - Mobile Drawer */}
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer(false)}
        sx={{ 
          '& .MuiDrawer-paper': { 
            width: { xs: '80%', sm: 320 },
            boxSizing: 'border-box',
            pt: 1
          } 
        }}
      >
        <Box sx={{ 
          width: '100%', 
          p: 2,
          height: '100%',
          overflow: 'auto' 
        }}>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            mb: 2 
          }}>
            <Typography variant="h6">Bộ lọc</Typography>
            <IconButton onClick={toggleDrawer(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
          <ProductFilter
            categories={categories}
            brands={brands}
            filters={filters}
            onFilterChange={handleFilterChange}
            onApplyFilters={(f) => {
              applyFilters(f);
              setDrawerOpen(false);
            }}
            onResetFilters={() => {
              resetFilters();
              setDrawerOpen(false);
            }}
            productType={productType}
            onProductTypeChange={handleProductTypeChange}
            sort={sort}
            onSortChange={handleSortChange}
            isMobile={true}
          />
        </Box>
      </Drawer>
      
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
    </Container>
  );
};

export default React.memo(ProductList); 