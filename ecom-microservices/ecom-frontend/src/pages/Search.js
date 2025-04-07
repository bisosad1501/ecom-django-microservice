import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Button,
  Box,
  TextField,
  InputAdornment,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Pagination,
  CircularProgress,
  Alert,
  Breadcrumbs,
  Chip,
  Divider,
  Paper,
  Rating,
  Skeleton,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import {
  Search as SearchIcon,
  Tune as FilterIcon,
  Clear as ClearIcon,
  ShoppingCart as CartIcon,
  Favorite as FavoriteIcon,
  FavoriteBorder as FavoriteBorderIcon,
} from '@mui/icons-material';
import { productService, cartService } from '../services/api';

const Search = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [searchQuery, setSearchQuery] = useState('');
  const [category, setCategory] = useState('all');
  const [sort, setSort] = useState('relevance');
  const [loading, setLoading] = useState(false);
  const [initialLoad, setInitialLoad] = useState(true);
  const [error, setError] = useState('');
  const [products, setProducts] = useState([]);
  const [totalResults, setTotalResults] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [notification, setNotification] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  // Categories for filter dropdown
  const categories = [
    { id: 'all', name: 'Tất cả danh mục' },
    { id: 'electronics', name: 'Điện tử & Điện thoại' },
    { id: 'computer', name: 'Máy tính & Laptop' },
    { id: 'books', name: 'Sách' },
    { id: 'clothes', name: 'Thời trang' },
    { id: 'shoes', name: 'Giày dép' },
    { id: 'accessories', name: 'Phụ kiện' }
  ];

  useEffect(() => {
    // Extract search parameters from URL
    const params = new URLSearchParams(location.search);
    const q = params.get('q') || '';
    const cat = params.get('category') || 'all';
    const sortBy = params.get('sort') || 'relevance';
    const page = parseInt(params.get('page') || '1', 10);
    
    // Update state with URL parameters
    setSearchQuery(q);
    setCategory(cat);
    setSort(sortBy);
    setCurrentPage(page);
    
    // If there's a search query, perform search
    if (q) {
      performSearch(q, cat, sortBy, page);
    } else {
      setInitialLoad(false);
    }
  }, [location.search]);

  const performSearch = async (query, category, sort, page) => {
    setLoading(true);
    setError('');
    
    try {
      // Call search API
      const response = await productService.searchProducts({
        query,
        category: category !== 'all' ? category : '',
        sort,
        page,
        limit: 12
      });
      
      if (response.data && response.data.results) {
        setProducts(response.data.results);
        setTotalResults(response.data.total || 0);
        setTotalPages(response.data.total_pages || Math.ceil(response.data.total / 12) || 1);
      } else {
        // Use dummy data if API fails to return results
        const dummyData = getDummySearchResults(query, category);
        setProducts(dummyData);
        setTotalResults(dummyData.length);
        setTotalPages(Math.ceil(dummyData.length / 12));
      }
    } catch (error) {
      console.error('Search error:', error);
      setError('Không thể tìm kiếm sản phẩm. Vui lòng thử lại sau.');
      
      // Use dummy data on error
      const dummyData = getDummySearchResults(query, category);
      setProducts(dummyData);
      setTotalResults(dummyData.length);
      setTotalPages(Math.ceil(dummyData.length / 12));
    } finally {
      setLoading(false);
      setInitialLoad(false);
    }
  };

  const handleSearch = (event) => {
    event.preventDefault();
    
    if (!searchQuery.trim()) {
      return;
    }
    
    // Update URL with search parameters
    const params = new URLSearchParams();
    params.set('q', searchQuery);
    if (category !== 'all') {
      params.set('category', category);
    }
    if (sort !== 'relevance') {
      params.set('sort', sort);
    }
    
    navigate(`/search?${params.toString()}`);
  };

  const handleCategoryChange = (event) => {
    const newCategory = event.target.value;
    setCategory(newCategory);
    
    // Update URL with new category
    const params = new URLSearchParams(location.search);
    if (newCategory === 'all') {
      params.delete('category');
    } else {
      params.set('category', newCategory);
    }
    
    // Reset to page 1 when changing category
    params.delete('page');
    
    navigate(`/search?${params.toString()}`);
  };

  const handleSortChange = (event) => {
    const newSort = event.target.value;
    setSort(newSort);
    
    // Update URL with new sort
    const params = new URLSearchParams(location.search);
    if (newSort === 'relevance') {
      params.delete('sort');
    } else {
      params.set('sort', newSort);
    }
    
    // Reset to page 1 when changing sort
    params.delete('page');
    
    navigate(`/search?${params.toString()}`);
  };

  const handlePageChange = (event, value) => {
    setCurrentPage(value);
    
    // Update URL with new page
    const params = new URLSearchParams(location.search);
    if (value === 1) {
      params.delete('page');
    } else {
      params.set('page', value);
    }
    
    navigate(`/search?${params.toString()}`);
  };

  const handleAddToCart = async (product) => {
    try {
      await cartService.addToCart({
        product_id: product.id,
        quantity: 1,
        product_type: product.type || 'product'
      });
      
      setNotification({
        open: true,
        message: 'Đã thêm vào giỏ hàng',
        severity: 'success'
      });
      
      // Close notification after 3 seconds
      setTimeout(() => {
        setNotification({ ...notification, open: false });
      }, 3000);
    } catch (error) {
      console.error('Error adding to cart:', error);
      setNotification({
        open: true,
        message: 'Không thể thêm vào giỏ hàng',
        severity: 'error'
      });
    }
  };

  const handleToggleWishlist = (productId) => {
    try {
      // Get wishlist from localStorage
      const wishlist = localStorage.getItem('wishlist');
      let wishlistItems = wishlist ? JSON.parse(wishlist) : [];
      
      // Check if product is already in wishlist
      const index = wishlistItems.indexOf(productId);
      
      if (index !== -1) {
        // Remove from wishlist
        wishlistItems.splice(index, 1);
        setNotification({
          open: true,
          message: 'Đã xóa khỏi danh sách yêu thích',
          severity: 'info'
        });
      } else {
        // Add to wishlist
        wishlistItems.push(productId);
        setNotification({
          open: true,
          message: 'Đã thêm vào danh sách yêu thích',
          severity: 'success'
        });
      }
      
      // Save updated wishlist
      localStorage.setItem('wishlist', JSON.stringify(wishlistItems));
      
      // Close notification after 3 seconds
      setTimeout(() => {
        setNotification({ ...notification, open: false });
      }, 3000);
    } catch (error) {
      console.error('Error updating wishlist:', error);
      setNotification({
        open: true,
        message: 'Không thể cập nhật danh sách yêu thích',
        severity: 'error'
      });
    }
  };

  const isInWishlist = (productId) => {
    try {
      const wishlist = localStorage.getItem('wishlist');
      if (!wishlist) return false;
      
      const wishlistItems = JSON.parse(wishlist);
      return wishlistItems.includes(productId);
    } catch (error) {
      return false;
    }
  };

  const getProductDetailUrl = (product) => {
    if (!product) return '/';
    
    if (product.type === 'book') return `/books/${product.id}`;
    if (product.type === 'shoe') return `/shoes/${product.id}`;
    
    return `/products/${product.id}`;
  };

  const formatPrice = (price) => {
    return price ? price.toLocaleString() + ' VNĐ' : '';
  };

  // Function to generate dummy search results
  const getDummySearchResults = (query, category) => {
    const dummyProducts = [
      {
        id: '1',
        name: 'Laptop Asus VivoBook 15',
        type: 'product',
        category: 'computer',
        price: 15990000,
        discount_price: 14500000,
        image: 'https://via.placeholder.com/300x300?text=Laptop+Asus',
        rating: 4.5
      },
      {
        id: '2',
        name: 'Điện thoại Samsung Galaxy S22',
        type: 'product',
        category: 'electronics',
        price: 21990000,
        discount_price: 19990000,
        image: 'https://via.placeholder.com/300x300?text=Samsung+Galaxy+S22',
        rating: 4.7
      },
      {
        id: '3',
        name: 'Đắc Nhân Tâm',
        type: 'book',
        category: 'books',
        author: 'Dale Carnegie',
        price: 88000,
        discount_price: 75000,
        image: 'https://via.placeholder.com/300x400?text=Dac+Nhan+Tam',
        rating: 4.8
      },
      {
        id: '4',
        name: 'Tai nghe Sony WH-1000XM4',
        type: 'product',
        category: 'electronics',
        price: 8490000,
        discount_price: 6990000,
        image: 'https://via.placeholder.com/300x300?text=Sony+WH-1000XM4',
        rating: 4.9
      },
      {
        id: '5',
        name: 'Giày Nike Air Force 1',
        type: 'shoe',
        category: 'shoes',
        price: 2650000,
        discount_price: null,
        image: 'https://via.placeholder.com/300x300?text=Nike+Air+Force+1',
        rating: 4.6
      },
      {
        id: '6',
        name: 'Áo thun Polo nam',
        type: 'product',
        category: 'clothes',
        price: 350000,
        discount_price: 290000,
        image: 'https://via.placeholder.com/300x300?text=Polo+shirt',
        rating: 4.3
      },
      {
        id: '7',
        name: 'Apple Watch Series 7',
        type: 'product',
        category: 'electronics',
        price: 11990000,
        discount_price: 10890000,
        image: 'https://via.placeholder.com/300x300?text=Apple+Watch',
        rating: 4.8
      },
      {
        id: '8',
        name: 'Sách Atomic Habits',
        type: 'book',
        category: 'books',
        author: 'James Clear',
        price: 120000,
        discount_price: 99000,
        image: 'https://via.placeholder.com/300x400?text=Atomic+Habits',
        rating: 4.9
      },
      {
        id: '9',
        name: 'Chuột không dây Logitech MX Master 3',
        type: 'product',
        category: 'computer',
        price: 2490000,
        discount_price: null,
        image: 'https://via.placeholder.com/300x300?text=Logitech+MX+Master',
        rating: 4.8
      },
      {
        id: '10',
        name: 'Giày Adidas Ultraboost 22',
        type: 'shoe',
        category: 'shoes',
        price: 4250000,
        discount_price: 3850000,
        image: 'https://via.placeholder.com/300x300?text=Adidas+Ultraboost',
        rating: 4.7
      },
      {
        id: '11',
        name: 'Ốp lưng iPhone 13 Pro',
        type: 'product',
        category: 'accessories',
        price: 350000,
        discount_price: 290000,
        image: 'https://via.placeholder.com/300x300?text=iPhone+Case',
        rating: 4.2
      },
      {
        id: '12',
        name: 'Bàn phím cơ Keychron K2',
        type: 'product',
        category: 'computer',
        price: 1890000,
        discount_price: 1690000,
        image: 'https://via.placeholder.com/300x300?text=Keychron+K2',
        rating: 4.6
      }
    ];

    // Filter by search query (case insensitive)
    const lowercaseQuery = query.toLowerCase();
    let filtered = dummyProducts.filter(product => 
      product.name.toLowerCase().includes(lowercaseQuery) || 
      (product.author && product.author.toLowerCase().includes(lowercaseQuery))
    );
    
    // Filter by category if not 'all'
    if (category && category !== 'all') {
      filtered = filtered.filter(product => product.category === category);
    }
    
    return filtered;
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 3 }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          Trang chủ
        </Link>
        <Typography color="text.primary">Tìm kiếm</Typography>
      </Breadcrumbs>
      
      {/* Search Form */}
      <Paper component="form" onSubmit={handleSearch} sx={{ p: 2, mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Tìm kiếm sản phẩm..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
                endAdornment: searchQuery && (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="clear search"
                      onClick={() => setSearchQuery('')}
                      edge="end"
                    >
                      <ClearIcon />
                    </IconButton>
                  </InputAdornment>
                )
              }}
            />
          </Grid>
          
          <Grid item xs={6} md={2}>
            <FormControl fullWidth variant="outlined">
              <InputLabel id="category-select-label">Danh mục</InputLabel>
              <Select
                labelId="category-select-label"
                id="category-select"
                value={category}
                onChange={handleCategoryChange}
                label="Danh mục"
              >
                {categories.map((cat) => (
                  <MenuItem key={cat.id} value={cat.id}>
                    {cat.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={6} md={2}>
            <FormControl fullWidth variant="outlined">
              <InputLabel id="sort-select-label">Sắp xếp</InputLabel>
              <Select
                labelId="sort-select-label"
                id="sort-select"
                value={sort}
                onChange={handleSortChange}
                label="Sắp xếp"
              >
                <MenuItem value="relevance">Liên quan</MenuItem>
                <MenuItem value="price_asc">Giá tăng dần</MenuItem>
                <MenuItem value="price_desc">Giá giảm dần</MenuItem>
                <MenuItem value="rating">Đánh giá cao</MenuItem>
                <MenuItem value="newest">Mới nhất</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={2}>
            <Button 
              type="submit" 
              variant="contained" 
              fullWidth
              disabled={!searchQuery.trim()}
            >
              Tìm kiếm
            </Button>
          </Grid>
        </Grid>
      </Paper>
      
      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {/* Search Results */}
      {initialLoad ? (
        <Box sx={{ my: 4 }}>
          <Typography variant="h5" sx={{ mb: 4 }}>
            Nhập từ khóa để tìm kiếm sản phẩm
          </Typography>
        </Box>
      ) : loading ? (
        <Grid container spacing={3}>
          {[...Array(8)].map((_, index) => (
            <Grid item xs={6} sm={4} md={3} key={index}>
              <Card>
                <Skeleton variant="rectangular" height={200} />
                <CardContent>
                  <Skeleton variant="text" height={30} />
                  <Skeleton variant="text" width="60%" />
                  <Box sx={{ mt: 1 }}>
                    <Skeleton variant="text" width="40%" />
                  </Box>
                </CardContent>
                <CardActions>
                  <Skeleton variant="rectangular" width={120} height={36} sx={{ ml: 'auto' }} />
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      ) : products.length === 0 ? (
        <Box sx={{ my: 8, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            Không tìm thấy sản phẩm nào
          </Typography>
          <Typography variant="body1">
            Vui lòng thử lại với từ khóa khác hoặc duyệt qua danh mục sản phẩm của chúng tôi
          </Typography>
          <Button 
            variant="contained" 
            component={Link} 
            to="/products"
            sx={{ mt: 3 }}
          >
            Xem tất cả sản phẩm
          </Button>
        </Box>
      ) : (
        <>
          <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography>
              {searchQuery && (
                <Box component="span">
                  Kết quả tìm kiếm cho <Chip label={searchQuery} /> {category !== 'all' && (
                    <>trong <Chip label={categories.find(cat => cat.id === category)?.name || category} /></>
                  )}
                </Box>
              )}
            </Typography>
            <Typography>
              Tìm thấy {totalResults} sản phẩm
            </Typography>
          </Box>
          
          <Grid container spacing={3}>
            {products.map((product) => (
              <Grid item xs={6} sm={4} md={3} key={product.id}>
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', position: 'relative' }}>
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
                    onClick={() => handleToggleWishlist(product.id)}
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
                      pt: product.type === 'book' ? '140%' : '100%',
                      position: 'relative',
                      cursor: 'pointer',
                      textDecoration: 'none'
                    }}
                  >
                    <Box
                      component="img"
                      src={product.image}
                      alt={product.name}
                      sx={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        objectFit: 'contain'
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
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                      <Rating value={product.rating || 0} precision={0.1} size="small" readOnly />
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
                      onClick={() => handleAddToCart(product)}
                      sx={{ ml: 'auto' }}
                    >
                      Thêm vào giỏ
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
          
          {/* Pagination */}
          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={totalPages}
                page={currentPage}
                onChange={handlePageChange}
                color="primary"
                showFirstButton
                showLastButton
              />
            </Box>
          )}
          
          {/* Notification Popup */}
          {notification.open && (
            <Box
              sx={{
                position: 'fixed',
                bottom: 20,
                right: 20,
                zIndex: 2000,
                maxWidth: 300
              }}
            >
              <Alert severity={notification.severity}>
                {notification.message}
              </Alert>
            </Box>
          )}
        </>
      )}
    </Container>
  );
};

export default Search; 