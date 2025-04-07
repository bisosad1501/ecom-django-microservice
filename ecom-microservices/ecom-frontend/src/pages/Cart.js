import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  Button,
  Divider,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Snackbar
} from '@mui/material';
import {
  ShoppingBag as ShoppingBagIcon
} from '@mui/icons-material';
import { cartService } from '../services/api';
// Import component CartItem mới
import CartItem from '../components/Cart/CartItem';

const Cart = () => {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    setLoading(true);
    try {
      // Lấy userId từ localStorage
      const userId = localStorage.getItem('userId');
      
      // Chỉ gọi API khi userId tồn tại và có giá trị
      if (userId) {
        const response = await cartService.getCart(userId);
        // Kiểm tra dữ liệu trả về từ API
        if (response.data && response.data.items) {
          // Map CartItems từ API response để hỗ trợ trường price
          const mappedItems = response.data.items.map(item => ({
            ...item,
            price: item.sale_price, // Dùng sale_price từ API để gán vào price cho tương thích với code hiện tại
            imageUrl: item.image,
            name: item.product_name
          }));
          setCartItems(mappedItems);
        } else {
          setCartItems([]);
        }
      } else {
        console.log('Không có userId, không thể lấy giỏ hàng');
        setCartItems([]);
      }
    } catch (error) {
      console.error('Lỗi khi lấy giỏ hàng:', error);
      setError('Không thể tải giỏ hàng. Vui lòng đăng nhập và thử lại.');
      setCartItems([]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateQuantity = async (itemId, newQuantity) => {
    if (newQuantity < 1) return;
    
    try {
      // Lấy userId từ localStorage
      const userId = localStorage.getItem('userId');
      
      if (!userId) {
        setSnackbar({
          open: true,
          message: 'Vui lòng đăng nhập để cập nhật giỏ hàng',
          severity: 'warning'
        });
        return;
      }
      
      // Cập nhật UI trước
      const updatedItems = cartItems.map(item => {
        if (item.id === itemId) {
          return {
            ...item,
            quantity: newQuantity,
            subtotal: item.price * newQuantity
          };
        }
        return item;
      });
      
      setCartItems(updatedItems);
      
      // Tìm thông tin product_id của item cần cập nhật
      const item = cartItems.find(item => item.id === itemId);
      
      // Gọi API cập nhật
      await cartService.updateCart({
        user_id: userId,
        product_id: item.product_id,
        quantity: newQuantity
      });
      
    } catch (error) {
      console.error('Lỗi khi cập nhật số lượng:', error);
      setSnackbar({
        open: true,
        message: 'Không thể cập nhật số lượng. Vui lòng thử lại.',
        severity: 'error'
      });
      
      // Reload cart to get correct data
      fetchCart();
    }
  };

  const handleRemoveItem = async (itemId) => {
    try {
      // Lấy userId từ localStorage
      const userId = localStorage.getItem('userId');
      
      if (!userId) {
        setSnackbar({
          open: true,
          message: 'Vui lòng đăng nhập để xóa sản phẩm',
          severity: 'warning'
        });
        return;
      }
      
      // Tìm thông tin product_id của item cần xóa
      const item = cartItems.find(item => item.id === itemId);
      
      // Cập nhật UI trước
      setCartItems(cartItems.filter(item => item.id !== itemId));
      
      // Gọi API xóa với thông tin đúng định dạng
      await cartService.removeFromCart({
        user_id: userId,
        product_id: item.product_id
      });
      
      setSnackbar({
        open: true,
        message: 'Đã xóa sản phẩm khỏi giỏ hàng',
        severity: 'success'
      });
    } catch (error) {
      console.error('Lỗi khi xóa sản phẩm:', error);
      setSnackbar({
        open: true,
        message: 'Không thể xóa sản phẩm. Vui lòng thử lại.',
        severity: 'error'
      });
      
      // Reload cart to get correct data
      fetchCart();
    }
  };

  const handleClearCart = async () => {
    try {
      // Cập nhật UI trước
      setCartItems([]);
      
      // Gọi API xóa tất cả
      await cartService.clearCart();
      
      setSnackbar({
        open: true,
        message: 'Đã xóa tất cả sản phẩm khỏi giỏ hàng',
        severity: 'success'
      });
    } catch (error) {
      console.error('Lỗi khi xóa giỏ hàng:', error);
      setSnackbar({
        open: true,
        message: 'Không thể xóa giỏ hàng. Vui lòng thử lại.',
        severity: 'error'
      });
      
      // Reload cart to get correct data
      fetchCart();
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const getProductLink = (item) => {
    // Điều chỉnh link dựa trên loại sản phẩm
    if (item.product_type === 'BOOK') return `/book/${item.product_id}`;
    if (item.product_type === 'SHOE') return `/shoe/${item.product_id}`;
    return `/products/${item.product_id}`;
  };

  const calculateTotal = () => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  };
  
  const calculateShipping = () => {
    const subtotal = calculateTotal();
    // Miễn phí vận chuyển nếu đơn hàng trên 500,000 VNĐ
    return subtotal > 500000 ? 0 : 30000;
  };

  const handleCheckout = () => {
    navigate('/checkout');
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
        Giỏ hàng
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {cartItems.length > 0 ? (
        <Grid container spacing={4}>
          {/* Danh sách sản phẩm */}
          <Grid item xs={12} md={8}>
            <Box>
              {cartItems.map((item) => (
                <CartItem
                  key={item.id}
                  item={{
                    ...item,
                    id: item.id,
                    name: item.product_name,
                    imageUrl: item.image,
                    price: item.price,
                    quantity: item.quantity,
                    // Thêm các thuộc tính khác nếu component CartItem cần
                    originalPrice: item.original_price || undefined,
                    discount: item.discount || 0,
                    attributes: item.attributes || undefined
                  }}
                  onUpdateQuantity={handleUpdateQuantity}
                  onRemove={handleRemoveItem}
                />
              ))}
            </Box>
            
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
              <Button
                component={Link}
                to="/"
                variant="outlined"
              >
                Tiếp tục mua sắm
              </Button>
              <Button
                variant="outlined" 
                color="error"
                onClick={handleClearCart}
              >
                Xóa giỏ hàng
              </Button>
            </Box>
          </Grid>
          
          {/* Tóm tắt đơn hàng */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Tóm tắt đơn hàng
                </Typography>
                <Box sx={{ my: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body1">Tạm tính ({cartItems.length} sản phẩm)</Typography>
                    <Typography variant="body1">{calculateTotal().toLocaleString('vi-VN')} ₫</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body1">Phí vận chuyển</Typography>
                    <Typography variant="body1">
                      {calculateShipping() === 0 ? 'Miễn phí' : `${calculateShipping().toLocaleString('vi-VN')} ₫`}
                    </Typography>
                  </Box>
                </Box>
                <Divider sx={{ my: 2 }} />
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6">Tổng cộng</Typography>
                  <Typography variant="h6" color="primary">
                    {(calculateTotal() + calculateShipping()).toLocaleString('vi-VN')} ₫
                  </Typography>
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  size="large"
                  startIcon={<ShoppingBagIcon />}
                  onClick={handleCheckout}
                >
                  Thanh toán
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      ) : (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" gutterBottom>
            Giỏ hàng của bạn đang trống
          </Typography>
          <Typography variant="body1" sx={{ mb: 3 }}>
            Hãy thêm sản phẩm vào giỏ hàng để tiến hành mua sắm
          </Typography>
          <Button 
            variant="contained" 
            component={Link} 
            to="/"
          >
            Tiếp tục mua sắm
          </Button>
        </Paper>
      )}
      
      {/* Snackbar notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Cart; 