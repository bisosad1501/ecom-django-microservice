import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
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
  CircularProgress,
  IconButton,
  Divider,
  Alert
} from '@mui/material';
import { Delete as DeleteIcon, ShoppingCart as ShoppingCartIcon } from '@mui/icons-material';
import { productService, cartService } from '../services/api';

const Wishlist = () => {
  const [loading, setLoading] = useState(true);
  const [wishlistItems, setWishlistItems] = useState([]);
  const [error, setError] = useState('');
  const [addToCartSuccess, setAddToCartSuccess] = useState(false);

  useEffect(() => {
    // Trong triển khai thực tế, sẽ lấy dữ liệu từ API
    // Nhưng hiện tại, sử dụng localStorage để lưu trữ tạm
    const fetchWishlist = async () => {
      setLoading(true);
      try {
        const storedWishlist = localStorage.getItem('wishlist');
        const wishlistIds = storedWishlist ? JSON.parse(storedWishlist) : [];
        
        if (wishlistIds.length > 0) {
          // Lấy thông tin sản phẩm từ các ID
          const productPromises = wishlistIds.map(id => productService.getProductById(id));
          const responses = await Promise.all(productPromises);
          const products = responses.map(response => response.data);
          setWishlistItems(products);
        } else {
          setWishlistItems([]);
        }
      } catch (error) {
        console.error('Lỗi khi lấy danh sách yêu thích:', error);
        setError('Không thể tải danh sách yêu thích. Vui lòng thử lại sau.');
      } finally {
        setLoading(false);
      }
    };

    fetchWishlist();
  }, []);

  const removeFromWishlist = (productId) => {
    try {
      const storedWishlist = localStorage.getItem('wishlist');
      const wishlistIds = storedWishlist ? JSON.parse(storedWishlist) : [];
      
      const updatedWishlist = wishlistIds.filter(id => id !== productId);
      localStorage.setItem('wishlist', JSON.stringify(updatedWishlist));
      
      // Cập nhật UI
      setWishlistItems(wishlistItems.filter(item => item.id !== productId));
    } catch (error) {
      console.error('Lỗi khi xóa khỏi danh sách yêu thích:', error);
      setError('Không thể xóa sản phẩm khỏi danh sách yêu thích.');
    }
  };

  const addToCart = async (product) => {
    try {
      await cartService.addToCart({
        product_id: product.id,
        quantity: 1
      });
      
      setAddToCartSuccess(true);
      setTimeout(() => setAddToCartSuccess(false), 3000);
    } catch (error) {
      console.error('Lỗi khi thêm vào giỏ hàng:', error);
      setError('Không thể thêm sản phẩm vào giỏ hàng.');
      setTimeout(() => setError(''), 3000);
    }
  };

  // Hàm trợ giúp để lấy hình ảnh an toàn
  const getImageUrl = (product) => {
    if (!product) return 'https://via.placeholder.com/300';
    
    if (product.image_url) return product.image_url;
    if (product.image) return product.image;
    if (product.cover_image) return product.cover_image;
    
    return 'https://via.placeholder.com/300';
  };

  // Hàm trợ giúp để lấy giá an toàn
  const getPrice = (product) => {
    if (!product) return '';
    
    const price = product.price || product.sale_price || 0;
    return price.toLocaleString() + ' VNĐ';
  };

  // Hàm trợ giúp để lấy tên sản phẩm
  const getProductName = (product) => {
    if (!product) return '';
    
    return product.name || product.title || 'Sản phẩm';
  };

  // Hàm xác định URL chi tiết dựa vào loại sản phẩm
  const getDetailUrl = (product) => {
    if (!product) return '/';
    
    // Xác định loại sản phẩm dựa vào thuộc tính
    if (product.author || product.isbn) return `/books/${product.id}`;
    if (product.size || product.brand) return `/shoes/${product.id}`;
    
    return `/products/${product.id}`;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', my: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Danh sách yêu thích
      </Typography>
      
      <Divider sx={{ mb: 4 }} />
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {addToCartSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Đã thêm sản phẩm vào giỏ hàng thành công!
        </Alert>
      )}
      
      {wishlistItems.length > 0 ? (
        <Grid container spacing={3}>
          {wishlistItems.map((product) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={product.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={getImageUrl(product)}
                  alt={getProductName(product)}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h6" component="div" noWrap>
                    {getProductName(product)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {getPrice(product)}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    component={Link} 
                    to={getDetailUrl(product)}
                  >
                    Chi tiết
                  </Button>
                  <IconButton 
                    color="primary" 
                    onClick={() => addToCart(product)}
                    aria-label="add to cart"
                  >
                    <ShoppingCartIcon />
                  </IconButton>
                  <IconButton 
                    color="error"
                    onClick={() => removeFromWishlist(product.id)}
                    aria-label="remove from wishlist"
                  >
                    <DeleteIcon />
                  </IconButton>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      ) : (
        <Box sx={{ textAlign: 'center', my: 8 }}>
          <Typography variant="h6" gutterBottom>
            Danh sách yêu thích của bạn đang trống
          </Typography>
          <Typography variant="body1" sx={{ mb: 3 }}>
            Hãy khám phá cửa hàng và thêm những sản phẩm bạn yêu thích
          </Typography>
          <Button 
            variant="contained" 
            component={Link} 
            to="/"
          >
            Tiếp tục mua sắm
          </Button>
        </Box>
      )}
    </Container>
  );
};

export default Wishlist; 