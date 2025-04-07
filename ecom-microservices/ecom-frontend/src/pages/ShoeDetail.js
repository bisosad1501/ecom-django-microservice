import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Grid,
  Button,
  Divider,
  Rating,
  Card,
  CardContent,
  CardMedia,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Chip,
  Breadcrumbs,
  Paper,
  Snackbar,
  List,
  ListItem
} from '@mui/material';
import {
  FavoriteBorder as FavoriteBorderIcon,
  Favorite as FavoriteIcon,
  ShoppingCart as ShoppingCartIcon,
  Star as StarIcon,
  Add as AddIcon,
  Remove as RemoveIcon
} from '@mui/icons-material';
import { productService, reviewService } from '../services/api';

const ShoeDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [selectedSize, setSelectedSize] = useState('');
  const [tabValue, setTabValue] = useState(0);
  const [reviews, setReviews] = useState([]);
  const [similarProducts, setSimilarProducts] = useState([]);
  const [inWishlist, setInWishlist] = useState(false);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });
  
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Lấy thông tin sản phẩm
        const productData = await productService.getProductById(id);
        if (productData && productData.data) {
          setProduct(productData.data);
          // Đặt kích thước mặc định là kích thước đầu tiên có sẵn
          if (productData.data.sizes && productData.data.sizes.length > 0) {
            setSelectedSize(productData.data.sizes[0]);
          }
        } else {
          // Sử dụng dữ liệu mẫu nếu API không trả về dữ liệu
          setDummyProduct();
        }
        
        // Lấy đánh giá
        const reviewsData = await reviewService.getReviewsByProductId(id);
        if (reviewsData && reviewsData.data) {
          setReviews(reviewsData.data);
        } else {
          // Sử dụng dữ liệu mẫu cho đánh giá
          setDummyReviews();
        }
        
        // Lấy sản phẩm tương tự
        const similarData = await productService.getSimilarProducts(id);
        if (similarData && similarData.data) {
          setSimilarProducts(similarData.data);
        } else {
          // Sử dụng dữ liệu mẫu cho sản phẩm tương tự
          setDummySimilarProducts();
        }
        
        // Kiểm tra xem sản phẩm có trong danh sách yêu thích không
        try {
          const wishlistData = await productService.getWishlist(localStorage.getItem('userId'));
          if (wishlistData && wishlistData.data) {
            const isInList = wishlistData.data.items.some(item => item.product_id === id);
            setInWishlist(isInList);
          }
        } catch (error) {
          console.error('Lỗi khi kiểm tra danh sách yêu thích:', error);
        }
      } catch (error) {
        console.error('Lỗi khi lấy thông tin sản phẩm:', error);
        setError('Không thể tải thông tin sản phẩm. Vui lòng thử lại sau.');
        // Sử dụng dữ liệu mẫu trong trường hợp lỗi
        setDummyProduct();
        setDummyReviews();
        setDummySimilarProducts();
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [id]);
  
  const setDummyProduct = () => {
    setProduct({
      id: id,
      name: 'Giày Nike Air Force 1',
      brand: 'Nike',
      category: 'Sneakers',
      description: 'Nike Air Force 1 là một trong những mẫu giày biểu tượng nhất của Nike, được ra mắt lần đầu vào năm 1982. Giày có thiết kế cổ điển với phần mũi giày rộng, đế cao su dày và dây buộc chắc chắn. Phiên bản này được làm từ chất liệu da cao cấp với logo Swoosh đặc trưng và công nghệ đệm Air để tạo cảm giác thoải mái khi mang.',
      price: 2650000,
      discount_price: 2250000,
      colors: ['Trắng', 'Đen', 'Đỏ'],
      sizes: ['38', '39', '40', '41', '42', '43'],
      material: 'Leather',
      images: [
        'https://via.placeholder.com/600x400?text=Nike+Air+Force+1',
        'https://via.placeholder.com/600x400?text=Nike+Air+Force+1+Side',
        'https://via.placeholder.com/600x400?text=Nike+Air+Force+1+Back'
      ],
      sku: 'NIKE-AF1-001',
      in_stock: true,
      stock_quantity: 15,
      rating: 4.5,
      review_count: 128
    });
  };
  
  const setDummyReviews = () => {
    setReviews([
      {
        id: '1',
        user_name: 'Nguyễn Văn A',
        rating: 5,
        title: 'Sản phẩm tuyệt vời',
        content: 'Tôi rất thích đôi giày này. Chất lượng tốt, form đẹp và rất thoải mái khi đi.',
        created_at: '2023-10-15T10:20:30Z'
      },
      {
        id: '2',
        user_name: 'Trần Thị B',
        rating: 4,
        title: 'Giày đẹp, đúng size',
        content: 'Đôi giày đẹp như hình, đúng với mô tả. Tuy nhiên màu trắng hơi dễ bám bẩn.',
        created_at: '2023-09-22T14:15:10Z'
      },
      {
        id: '3',
        user_name: 'Lê Văn C',
        rating: 3,
        title: 'Ổn',
        content: 'Đôi giày khá tốt với mức giá này. Ship hàng nhanh.',
        created_at: '2023-08-05T09:30:45Z'
      }
    ]);
  };
  
  const setDummySimilarProducts = () => {
    setSimilarProducts([
      {
        id: '101',
        name: 'Nike Air Max 90',
        price: 3150000,
        discount_price: 2850000,
        image: 'https://via.placeholder.com/300x200?text=Nike+Air+Max+90',
        rating: 4.3
      },
      {
        id: '102',
        name: 'Nike Dunk Low',
        price: 2450000,
        discount_price: null,
        image: 'https://via.placeholder.com/300x200?text=Nike+Dunk+Low',
        rating: 4.7
      },
      {
        id: '103',
        name: 'Nike Jordan 1 Low',
        price: 2950000,
        discount_price: 2550000,
        image: 'https://via.placeholder.com/300x200?text=Nike+Jordan+1',
        rating: 4.8
      },
      {
        id: '104',
        name: 'Nike Revolution 6',
        price: 1650000,
        discount_price: 1350000,
        image: 'https://via.placeholder.com/300x200?text=Nike+Revolution',
        rating: 4.2
      }
    ]);
  };
  
  const handleChangeQuantity = (newQuantity) => {
    if (newQuantity >= 1 && newQuantity <= (product?.stock_quantity || 10)) {
      setQuantity(newQuantity);
    }
  };
  
  const handleSizeChange = (event) => {
    setSelectedSize(event.target.value);
  };
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  const handleAddToCart = async () => {
    if (!selectedSize) {
      setSnackbar({
        open: true,
        message: 'Vui lòng chọn kích thước',
        severity: 'error'
      });
      return;
    }
    
    try {
      await productService.addToCart({
        product_id: id,
        quantity: quantity,
        size: selectedSize
      });
      
      setSnackbar({
        open: true,
        message: 'Đã thêm vào giỏ hàng',
        severity: 'success'
      });
    } catch (error) {
      console.error('Lỗi khi thêm vào giỏ hàng:', error);
      setSnackbar({
        open: true,
        message: 'Không thể thêm vào giỏ hàng. Vui lòng thử lại sau.',
        severity: 'error'
      });
    }
  };
  
  const handleToggleWishlist = async () => {
    try {
      const userId = localStorage.getItem('userId');
      if (!userId) {
        setSnackbar({
          open: true,
          message: 'Vui lòng đăng nhập để sử dụng tính năng này',
          severity: 'warning'
        });
        return;
      }
      
      if (inWishlist) {
        await productService.removeFromWishlist(userId, id);
      } else {
        await productService.addToWishlist(userId, id);
      }
      
      setInWishlist(!inWishlist);
      setSnackbar({
        open: true,
        message: inWishlist ? 'Đã xóa khỏi danh sách yêu thích' : 'Đã thêm vào danh sách yêu thích',
        severity: 'success'
      });
    } catch (error) {
      console.error('Lỗi khi cập nhật danh sách yêu thích:', error);
      setSnackbar({
        open: true,
        message: 'Không thể cập nhật danh sách yêu thích. Vui lòng thử lại.',
        severity: 'error'
      });
    }
  };
  
  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };
  
  const calculateAverageRating = (reviews) => {
    if (!reviews || reviews.length === 0) return 0;
    const sum = reviews.reduce((total, review) => total + review.rating, 0);
    return sum / reviews.length;
  };
  
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('vi-VN', options);
  };
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '70vh' }}>
        <CircularProgress />
      </Box>
    );
  }
  
  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }
  
  if (!product) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
        <Alert severity="error">Không tìm thấy thông tin sản phẩm</Alert>
      </Container>
    );
  }
  
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 3 }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          Trang chủ
        </Link>
        <Link to="/shoes" style={{ textDecoration: 'none', color: 'inherit' }}>
          Giày
        </Link>
        <Link to={`/brand/${product.brand?.toLowerCase()}`} style={{ textDecoration: 'none', color: 'inherit' }}>
          {product.brand}
        </Link>
        <Typography color="text.primary">{product.name}</Typography>
      </Breadcrumbs>
      
      {/* Thông tin sản phẩm */}
      <Grid container spacing={4}>
        {/* Hình ảnh sản phẩm */}
        <Grid item xs={12} md={6}>
          <Box>
            <Box
              component="img"
              src={product.images?.[0] || 'https://via.placeholder.com/600x400?text=No+Image'}
              alt={product.name}
              sx={{
                width: '100%',
                height: 'auto',
                objectFit: 'contain',
                borderRadius: 1,
                mb: 2
              }}
            />
            <Grid container spacing={1}>
              {product.images?.slice(1).map((image, index) => (
                <Grid item xs={4} key={index}>
                  <Box
                    component="img"
                    src={image}
                    alt={`${product.name} ${index + 2}`}
                    sx={{
                      width: '100%',
                      height: 100,
                      objectFit: 'cover',
                      borderRadius: 1,
                      cursor: 'pointer'
                    }}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        </Grid>
        
        {/* Thông tin chi tiết */}
        <Grid item xs={12} md={6}>
          <Box>
            <Typography variant="h4" component="h1" gutterBottom>
              {product.name}
            </Typography>
            
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Rating value={product.rating || 0} precision={0.5} readOnly />
              <Typography variant="body2" sx={{ ml: 1 }}>
                ({product.review_count || 0} đánh giá)
              </Typography>
              <Typography variant="body2" sx={{ ml: 2 }}>
                Mã sản phẩm: {product.sku}
              </Typography>
            </Box>
            
            <Box sx={{ mb: 3 }}>
              {product.discount_price ? (
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Typography variant="h5" component="span" color="primary" fontWeight="bold">
                    {product.discount_price.toLocaleString()} VNĐ
                  </Typography>
                  <Typography
                    variant="body1"
                    component="span"
                    sx={{ ml: 2, textDecoration: 'line-through', color: 'text.secondary' }}
                  >
                    {product.price.toLocaleString()} VNĐ
                  </Typography>
                  <Chip
                    label={`-${Math.round((1 - product.discount_price / product.price) * 100)}%`}
                    color="error"
                    size="small"
                    sx={{ ml: 1 }}
                  />
                </Box>
              ) : (
                <Typography variant="h5" component="span" color="primary" fontWeight="bold">
                  {product.price.toLocaleString()} VNĐ
                </Typography>
              )}
            </Box>
            
            <Typography variant="body1" paragraph>
              {product.description}
            </Typography>
            
            <Divider sx={{ my: 2 }} />
            
            {/* Màu sắc */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Màu sắc:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1 }}>
                {product.colors?.map((color, index) => (
                  <Chip key={index} label={color} variant="outlined" />
                ))}
              </Box>
            </Box>
            
            {/* Kích thước */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Kích thước:
              </Typography>
              <FormControl fullWidth sx={{ maxWidth: 200 }}>
                <InputLabel id="size-select-label">Chọn kích thước</InputLabel>
                <Select
                  labelId="size-select-label"
                  id="size-select"
                  value={selectedSize}
                  label="Chọn kích thước"
                  onChange={handleSizeChange}
                >
                  {product.sizes?.map((size, index) => (
                    <MenuItem key={index} value={size}>{size}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
            
            {/* Số lượng */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Số lượng:
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <IconButton
                  onClick={() => handleChangeQuantity(quantity - 1)}
                  disabled={quantity <= 1}
                >
                  <RemoveIcon />
                </IconButton>
                <TextField
                  value={quantity}
                  onChange={(e) => {
                    const val = parseInt(e.target.value);
                    if (!isNaN(val) && val >= 1) {
                      handleChangeQuantity(val);
                    }
                  }}
                  inputProps={{ 
                    min: 1, 
                    max: product.stock_quantity,
                    style: { textAlign: 'center' } 
                  }}
                  variant="outlined"
                  size="small"
                  sx={{ width: 60 }}
                />
                <IconButton
                  onClick={() => handleChangeQuantity(quantity + 1)}
                  disabled={quantity >= product.stock_quantity}
                >
                  <AddIcon />
                </IconButton>
                <Typography variant="body2" sx={{ ml: 1 }}>
                  {product.in_stock ? `${product.stock_quantity} sản phẩm có sẵn` : 'Hết hàng'}
                </Typography>
              </Box>
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            {/* Nút thêm vào giỏ hàng */}
            <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
              <Button
                variant="contained"
                size="large"
                startIcon={<ShoppingCartIcon />}
                onClick={handleAddToCart}
                disabled={!product.in_stock}
                sx={{ minWidth: 200 }}
              >
                Thêm vào giỏ hàng
              </Button>
              <IconButton
                color={inWishlist ? 'error' : 'default'}
                onClick={handleToggleWishlist}
                sx={{ border: 1, borderColor: 'divider' }}
              >
                {inWishlist ? <FavoriteIcon /> : <FavoriteBorderIcon />}
              </IconButton>
            </Box>
            
            {/* Thông tin thêm */}
            <Box>
              <Typography variant="body2">
                • Chất liệu: {product.material}
              </Typography>
              <Typography variant="body2">
                • Thương hiệu: {product.brand}
              </Typography>
              <Typography variant="body2">
                • Danh mục: {product.category}
              </Typography>
            </Box>
          </Box>
        </Grid>
      </Grid>
      
      {/* Tabs */}
      <Box sx={{ mt: 6, mb: 4 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="product tabs">
            <Tab label="Mô tả" id="tab-0" />
            <Tab label={`Đánh giá (${reviews.length})`} id="tab-1" />
          </Tabs>
        </Box>
        <Box sx={{ py: 3 }}>
          {tabValue === 0 && (
            <Typography variant="body1">
              {product.description}
            </Typography>
          )}
          {tabValue === 1 && (
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
                <Box sx={{ textAlign: 'center', mr: 4 }}>
                  <Typography variant="h2" color="primary">
                    {calculateAverageRating(reviews).toFixed(1)}
                  </Typography>
                  <Rating value={calculateAverageRating(reviews)} precision={0.5} readOnly size="large" />
                  <Typography variant="body2">
                    ({reviews.length} đánh giá)
                  </Typography>
                </Box>
                <Divider orientation="vertical" flexItem sx={{ mx: 2 }} />
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Chia sẻ đánh giá về sản phẩm này
                  </Typography>
                  <Button variant="outlined">Viết đánh giá</Button>
                </Box>
              </Box>
              
              {reviews.length > 0 ? (
                <List>
                  {reviews.map((review) => (
                    <ListItem key={review.id} sx={{ px: 0, display: 'block' }}>
                      <Paper sx={{ p: 2, mb: 2 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="subtitle1" fontWeight="bold">
                            {review.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {formatDate(review.created_at)}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Rating value={review.rating} readOnly size="small" />
                          <Typography variant="body2" sx={{ ml: 1 }}>
                            bởi {review.user_name}
                          </Typography>
                        </Box>
                        <Typography variant="body1">
                          {review.content}
                        </Typography>
                      </Paper>
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body1" sx={{ textAlign: 'center', py: 4 }}>
                  Chưa có đánh giá nào cho sản phẩm này.
                </Typography>
              )}
            </Box>
          )}
        </Box>
      </Box>
      
      {/* Sản phẩm tương tự */}
      <Box sx={{ mt: 6, mb: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Sản phẩm tương tự
        </Typography>
        <Grid container spacing={3}>
          {similarProducts.map((item) => (
            <Grid item xs={12} sm={6} md={3} key={item.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={item.image}
                  alt={item.name}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="subtitle1" component="h3" gutterBottom noWrap>
                    {item.name}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Rating value={item.rating} readOnly size="small" />
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body1" color="primary" fontWeight="bold">
                      {item.discount_price ? item.discount_price.toLocaleString() : item.price.toLocaleString()} VNĐ
                    </Typography>
                    {item.discount_price && (
                      <Typography
                        variant="body2"
                        sx={{ ml: 1, textDecoration: 'line-through', color: 'text.secondary' }}
                      >
                        {item.price.toLocaleString()} VNĐ
                      </Typography>
                    )}
                  </Box>
                </CardContent>
                <Box sx={{ p: 2, pt: 0 }}>
                  <Button 
                    variant="outlined" 
                    fullWidth
                    component={Link}
                    to={`/shoes/${item.id}`}
                  >
                    Xem chi tiết
                  </Button>
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
      
      {/* Snackbar notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ShoeDetail; 