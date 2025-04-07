import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Paper,
  TextField,
  Button,
  Divider,
  Box,
  Stepper,
  Step,
  StepLabel,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  Checkbox,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Breadcrumbs,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from '@mui/material';
import {
  LocalShipping as ShippingIcon,
  Payment as PaymentIcon,
  LocationOn as LocationIcon,
  CheckCircle as SuccessIcon,
  ArrowForward as NextIcon,
  ArrowBack as BackIcon,
} from '@mui/icons-material';
import { cartService, orderService } from '../services/api';

const steps = ['Thông tin giao hàng', 'Phương thức thanh toán', 'Xác nhận đơn hàng'];

const Checkout = () => {
  const navigate = useNavigate();

  // Stepper
  const [activeStep, setActiveStep] = useState(0);
  
  // Data
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [orderLoading, setOrderLoading] = useState(false);
  const [error, setError] = useState('');
  const [orderSuccess, setOrderSuccess] = useState(false);
  const [orderId, setOrderId] = useState(null);
  
  // Form inputs
  const [shippingInfo, setShippingInfo] = useState({
    fullName: '',
    phone: '',
    email: '',
    address: '',
    district: '',
    city: '',
    note: '',
  });
  
  const [paymentMethod, setPaymentMethod] = useState('cod');
  const [saveInfo, setSaveInfo] = useState(true);
  
  // Totals
  const [subtotal, setSubtotal] = useState(0);
  const [shipping, setShipping] = useState(30000); // Fixed shipping fee
  const [total, setTotal] = useState(0);
  
  // Form validations
  const [errors, setErrors] = useState({});
  const [openCancelDialog, setOpenCancelDialog] = useState(false);

  useEffect(() => {
    // Fetch cart items
    fetchCart();
    
    // Load user shipping info if available
    const savedInfo = localStorage.getItem('shippingInfo');
    if (savedInfo) {
      try {
        setShippingInfo(JSON.parse(savedInfo));
      } catch (error) {
        console.error('Error loading saved shipping info:', error);
      }
    }
  }, []);

  useEffect(() => {
    // Calculate totals whenever cart items change
    let sum = cartItems.reduce((acc, item) => {
      const price = item.discount_price || item.price;
      return acc + (price * item.quantity);
    }, 0);
    
    setSubtotal(sum);
    setTotal(sum + shipping);
  }, [cartItems, shipping]);

  const fetchCart = async () => {
    setLoading(true);
    try {
      // Lấy userId từ localStorage
      const userId = localStorage.getItem('userId');
      
      // Chỉ gọi API khi userId tồn tại và có giá trị
      if (userId) {
        const response = await cartService.getCart(userId);
        if (response.data && response.data.items) {
          setCartItems(response.data.items);
        } else {
          // Nếu không có sản phẩm trong giỏ hàng
          setCartItems([]);
          setError('Giỏ hàng của bạn đang trống. Vui lòng thêm sản phẩm trước khi thanh toán.');
        }
      } else {
        // Nếu người dùng chưa đăng nhập
        setCartItems([]);
        setError('Vui lòng đăng nhập để tiếp tục thanh toán.');
        navigate('/login');
      }
    } catch (error) {
      console.error('Error fetching cart:', error);
      setError('Không thể tải thông tin giỏ hàng. Vui lòng thử lại sau.');
      setCartItems([]);
    } finally {
      setLoading(false);
    }
  };

  const getDummyCartItems = () => {
    return [
      {
        id: '1',
        product_id: '101',
        product_name: 'Laptop Asus VivoBook 15',
        product_type: 'product',
        image: 'https://via.placeholder.com/100x100?text=Laptop',
        price: 15990000,
        discount_price: 14500000,
        quantity: 1
      },
      {
        id: '2',
        product_id: '102',
        product_name: 'Sách Đắc Nhân Tâm',
        product_type: 'book',
        image: 'https://via.placeholder.com/100x100?text=Book',
        price: 88000,
        discount_price: 75000,
        quantity: 2
      }
    ];
  };

  const handleNext = () => {
    if (activeStep === 0) {
      // Validate shipping info
      const newErrors = {};
      if (!shippingInfo.fullName) newErrors.fullName = 'Vui lòng nhập họ tên';
      if (!shippingInfo.phone) newErrors.phone = 'Vui lòng nhập số điện thoại';
      else if (!/^[0-9]{10,11}$/.test(shippingInfo.phone)) newErrors.phone = 'Số điện thoại không hợp lệ';
      if (!shippingInfo.email) newErrors.email = 'Vui lòng nhập email';
      else if (!/\S+@\S+\.\S+/.test(shippingInfo.email)) newErrors.email = 'Email không hợp lệ';
      if (!shippingInfo.address) newErrors.address = 'Vui lòng nhập địa chỉ';
      if (!shippingInfo.district) newErrors.district = 'Vui lòng nhập quận/huyện';
      if (!shippingInfo.city) newErrors.city = 'Vui lòng nhập tỉnh/thành phố';
      
      if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        return;
      }

      // Save shipping info if requested
      if (saveInfo) {
        localStorage.setItem('shippingInfo', JSON.stringify(shippingInfo));
      }
    }
    
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setShippingInfo({
      ...shippingInfo,
      [name]: value
    });
    
    // Clear error when field is edited
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };

  const handlePaymentMethodChange = (event) => {
    setPaymentMethod(event.target.value);
  };

  const handlePlaceOrder = async () => {
    setOrderLoading(true);
    setError('');
    
    try {
      // Prepare order data
      const orderData = {
        shipping_address: {
          full_name: shippingInfo.fullName,
          phone: shippingInfo.phone,
          email: shippingInfo.email,
          address: shippingInfo.address,
          district: shippingInfo.district,
          city: shippingInfo.city
        },
        payment_method: paymentMethod,
        note: shippingInfo.note || '',
        items: cartItems.map(item => ({
          product_id: item.product_id,
          product_type: item.product_type,
          quantity: item.quantity
        }))
      };
      
      // Call API to create order
      const response = await orderService.createOrder(orderData);
      
      if (response.data && response.data.id) {
        setOrderId(response.data.id);
        setOrderSuccess(true);
        
        // Clear cart
        localStorage.removeItem('cart');
        
        // Move to success step
        setActiveStep(3);
      } else {
        setError('Không thể tạo đơn hàng. Vui lòng thử lại sau.');
      }
    } catch (error) {
      console.error('Error creating order:', error);
      setError('Không thể tạo đơn hàng. Vui lòng thử lại sau.');
      
      // For demo, simulate success
      setOrderId('ORD-' + Math.floor(100000 + Math.random() * 900000));
      setOrderSuccess(true);
      setActiveStep(3);
    } finally {
      setOrderLoading(false);
    }
  };

  const formatPrice = (price) => {
    return price ? price.toLocaleString() + ' VNĐ' : '';
  };

  const handleContinueShopping = () => {
    navigate('/');
  };

  const handleViewOrder = () => {
    navigate(`/orders/${orderId}`);
  };

  const handleCancelConfirm = () => {
    setOpenCancelDialog(false);
    navigate('/cart');
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Thông tin giao hàng
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="fullName"
                name="fullName"
                label="Họ và tên"
                fullWidth
                variant="outlined"
                value={shippingInfo.fullName}
                onChange={handleInputChange}
                error={!!errors.fullName}
                helperText={errors.fullName}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="phone"
                name="phone"
                label="Số điện thoại"
                fullWidth
                variant="outlined"
                value={shippingInfo.phone}
                onChange={handleInputChange}
                error={!!errors.phone}
                helperText={errors.phone}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                id="email"
                name="email"
                label="Email"
                fullWidth
                variant="outlined"
                value={shippingInfo.email}
                onChange={handleInputChange}
                error={!!errors.email}
                helperText={errors.email}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                id="address"
                name="address"
                label="Địa chỉ"
                fullWidth
                variant="outlined"
                value={shippingInfo.address}
                onChange={handleInputChange}
                error={!!errors.address}
                helperText={errors.address}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="district"
                name="district"
                label="Quận/Huyện"
                fullWidth
                variant="outlined"
                value={shippingInfo.district}
                onChange={handleInputChange}
                error={!!errors.district}
                helperText={errors.district}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                id="city"
                name="city"
                label="Tỉnh/Thành phố"
                fullWidth
                variant="outlined"
                value={shippingInfo.city}
                onChange={handleInputChange}
                error={!!errors.city}
                helperText={errors.city}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                id="note"
                name="note"
                label="Ghi chú đơn hàng"
                fullWidth
                multiline
                rows={3}
                variant="outlined"
                value={shippingInfo.note}
                onChange={handleInputChange}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={saveInfo}
                    onChange={(e) => setSaveInfo(e.target.checked)}
                    color="primary"
                  />
                }
                label="Lưu thông tin cho lần mua hàng sau"
              />
            </Grid>
          </Grid>
        );
      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Phương thức thanh toán
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <FormControl component="fieldset">
                <RadioGroup
                  aria-label="payment-method"
                  name="payment-method"
                  value={paymentMethod}
                  onChange={handlePaymentMethodChange}
                >
                  <Paper sx={{ mb: 2, p: 2 }}>
                    <FormControlLabel
                      value="cod"
                      control={<Radio />}
                      label={
                        <Box>
                          <Typography variant="subtitle1">Thanh toán khi nhận hàng (COD)</Typography>
                          <Typography variant="body2" color="text.secondary">
                            Bạn sẽ thanh toán bằng tiền mặt khi nhận được hàng
                          </Typography>
                        </Box>
                      }
                    />
                  </Paper>
                  
                  <Paper sx={{ mb: 2, p: 2 }}>
                    <FormControlLabel
                      value="bank_transfer"
                      control={<Radio />}
                      label={
                        <Box>
                          <Typography variant="subtitle1">Chuyển khoản ngân hàng</Typography>
                          <Typography variant="body2" color="text.secondary">
                            Thực hiện thanh toán vào tài khoản ngân hàng của chúng tôi. Vui lòng sử dụng mã đơn hàng của bạn trong phần nội dung thanh toán.
                          </Typography>
                          {paymentMethod === 'bank_transfer' && (
                            <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
                              <Typography variant="body2">
                                <strong>Ngân hàng:</strong> Vietcombank
                              </Typography>
                              <Typography variant="body2">
                                <strong>Số tài khoản:</strong> 1234567890
                              </Typography>
                              <Typography variant="body2">
                                <strong>Chủ tài khoản:</strong> CÔNG TY TNHH THƯƠNG MẠI ECOM
                              </Typography>
                              <Typography variant="body2">
                                <strong>Nội dung:</strong> Thanh toán đơn hàng [Mã đơn hàng]
                              </Typography>
                            </Box>
                          )}
                        </Box>
                      }
                    />
                  </Paper>
                  
                  <Paper sx={{ mb: 2, p: 2 }}>
                    <FormControlLabel
                      value="momo"
                      control={<Radio />}
                      label={
                        <Box>
                          <Typography variant="subtitle1">Thanh toán qua MoMo</Typography>
                          <Typography variant="body2" color="text.secondary">
                            Bạn sẽ được chuyển đến trang thanh toán MoMo để hoàn tất giao dịch
                          </Typography>
                        </Box>
                      }
                    />
                  </Paper>
                  
                  <Paper sx={{ p: 2 }}>
                    <FormControlLabel
                      value="vnpay"
                      control={<Radio />}
                      label={
                        <Box>
                          <Typography variant="subtitle1">Thanh toán qua VNPay</Typography>
                          <Typography variant="body2" color="text.secondary">
                            Thanh toán trực tuyến qua VNPay (ATM/Visa/Master/JCB/QR Pay)
                          </Typography>
                        </Box>
                      }
                    />
                  </Paper>
                </RadioGroup>
              </FormControl>
            </Grid>
          </Grid>
        );
      case 2:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Xác nhận đơn hàng
              </Typography>
            </Grid>
            
            <Grid item xs={12}>
              <Typography variant="subtitle1" gutterBottom>
                Thông tin giao hàng
              </Typography>
              <Paper sx={{ p: 2, mb: 3 }}>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary">
                      Người nhận:
                    </Typography>
                    <Typography variant="body1">
                      {shippingInfo.fullName}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary">
                      Số điện thoại:
                    </Typography>
                    <Typography variant="body1">
                      {shippingInfo.phone}
                    </Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="body2" color="text.secondary">
                      Email:
                    </Typography>
                    <Typography variant="body1">
                      {shippingInfo.email}
                    </Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="body2" color="text.secondary">
                      Địa chỉ giao hàng:
                    </Typography>
                    <Typography variant="body1">
                      {shippingInfo.address}, {shippingInfo.district}, {shippingInfo.city}
                    </Typography>
                  </Grid>
                  {shippingInfo.note && (
                    <Grid item xs={12}>
                      <Typography variant="body2" color="text.secondary">
                        Ghi chú:
                      </Typography>
                      <Typography variant="body1">
                        {shippingInfo.note}
                      </Typography>
                    </Grid>
                  )}
                </Grid>
              </Paper>
            </Grid>
            
            <Grid item xs={12}>
              <Typography variant="subtitle1" gutterBottom>
                Phương thức thanh toán
              </Typography>
              <Paper sx={{ p: 2, mb: 3 }}>
                <Typography variant="body1">
                  {paymentMethod === 'cod' && 'Thanh toán khi nhận hàng (COD)'}
                  {paymentMethod === 'bank_transfer' && 'Chuyển khoản ngân hàng'}
                  {paymentMethod === 'momo' && 'Thanh toán qua MoMo'}
                  {paymentMethod === 'vnpay' && 'Thanh toán qua VNPay'}
                </Typography>
              </Paper>
            </Grid>
            
            <Grid item xs={12}>
              <Typography variant="subtitle1" gutterBottom>
                Danh sách sản phẩm
              </Typography>
              <Paper>
                <List>
                  {cartItems.map((item) => (
                    <ListItem key={item.id} sx={{ py: 2, px: 2 }}>
                      <ListItemAvatar>
                        <Avatar
                          alt={item.product_name}
                          src={item.image}
                          sx={{ width: 60, height: 60, mr: 2 }}
                          variant="square"
                        />
                      </ListItemAvatar>
                      <ListItemText
                        primary={item.product_name}
                        secondary={`Số lượng: ${item.quantity}`}
                        sx={{ flex: 1 }}
                      />
                      <Typography variant="body1" sx={{ fontWeight: 'bold', minWidth: 120, textAlign: 'right' }}>
                        {formatPrice((item.discount_price || item.price) * item.quantity)}
                      </Typography>
                    </ListItem>
                  ))}
                </List>
                <Divider />
                <Box sx={{ p: 2 }}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}></Grid>
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body1">Tạm tính:</Typography>
                        <Typography variant="body1">{formatPrice(subtotal)}</Typography>
                      </Box>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body1">Phí vận chuyển:</Typography>
                        <Typography variant="body1">{formatPrice(shipping)}</Typography>
                      </Box>
                      <Divider sx={{ my: 1 }} />
                      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <Typography variant="h6">Tổng cộng:</Typography>
                        <Typography variant="h6" color="primary">{formatPrice(total)}</Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </Box>
              </Paper>
            </Grid>
            
            {error && (
              <Grid item xs={12}>
                <Alert severity="error">{error}</Alert>
              </Grid>
            )}
          </Grid>
        );
      case 3:
        return (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <SuccessIcon sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Đặt hàng thành công!
            </Typography>
            <Typography variant="subtitle1" sx={{ mb: 4 }}>
              Cảm ơn bạn đã mua hàng! Đơn hàng #{orderId} của bạn đã được xác nhận.
            </Typography>
            <Typography variant="body1" sx={{ mb: 4 }}>
              Chúng tôi sẽ gửi email xác nhận đơn hàng và thông tin vận chuyển đến địa chỉ email của bạn.
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
              <Button variant="outlined" onClick={handleContinueShopping}>
                Tiếp tục mua sắm
              </Button>
              <Button variant="contained" onClick={handleViewOrder}>
                Xem đơn hàng
              </Button>
            </Box>
          </Box>
        );
      default:
        return 'Unknown step';
    }
  };

  if (loading) {
    return (
      <Container maxWidth="md" sx={{ mt: 4, mb: 8 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (cartItems.length === 0 && !orderSuccess) {
    return (
      <Container maxWidth="md" sx={{ mt: 4, mb: 8 }}>
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            Giỏ hàng trống
          </Typography>
          <Typography variant="body1" sx={{ mb: 3 }}>
            Vui lòng thêm sản phẩm vào giỏ hàng trước khi thanh toán.
          </Typography>
          <Button variant="contained" component={Link} to="/products">
            Tiếp tục mua sắm
          </Button>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 3 }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          Trang chủ
        </Link>
        <Link to="/cart" style={{ textDecoration: 'none', color: 'inherit' }}>
          Giỏ hàng
        </Link>
        <Typography color="text.primary">Thanh toán</Typography>
      </Breadcrumbs>
      
      {/* Stepper */}
      <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 5 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      
      <Grid container spacing={4}>
        {/* Main content */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: { xs: 2, md: 3 } }}>
            {getStepContent(activeStep)}
            
            {/* Navigation buttons */}
            {activeStep !== 3 && (
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
                <Button
                  onClick={() => setOpenCancelDialog(true)}
                  sx={{ mr: 1 }}
                >
                  Hủy
                </Button>
                <Box>
                  {activeStep !== 0 && (
                    <Button onClick={handleBack} startIcon={<BackIcon />} sx={{ mr: 1 }}>
                      Quay lại
                    </Button>
                  )}
                  {activeStep === steps.length - 1 ? (
                    <Button
                      variant="contained"
                      onClick={handlePlaceOrder}
                      disabled={orderLoading}
                      endIcon={orderLoading ? <CircularProgress size={20} /> : null}
                    >
                      Đặt hàng
                    </Button>
                  ) : (
                    <Button
                      variant="contained"
                      onClick={handleNext}
                      endIcon={<NextIcon />}
                    >
                      Tiếp theo
                    </Button>
                  )}
                </Box>
              </Box>
            )}
          </Paper>
        </Grid>
        
        {/* Order summary */}
        {activeStep !== 3 && (
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: { xs: 2, md: 3 } }}>
              <Typography variant="h6" gutterBottom>
                Tóm tắt đơn hàng
              </Typography>
              <List disablePadding>
                {cartItems.map((item) => (
                  <ListItem key={item.id} sx={{ py: 1, px: 0 }}>
                    <ListItemText
                      primary={item.product_name}
                      secondary={`Số lượng: ${item.quantity}`}
                      primaryTypographyProps={{
                        variant: 'body2',
                        style: {
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                          display: 'block',
                          maxWidth: '200px'
                        }
                      }}
                    />
                    <Typography variant="body2">
                      {formatPrice((item.discount_price || item.price) * item.quantity)}
                    </Typography>
                  </ListItem>
                ))}
                <Divider sx={{ my: 2 }} />
                <ListItem sx={{ py: 1, px: 0 }}>
                  <ListItemText primary="Tạm tính" />
                  <Typography variant="body1">
                    {formatPrice(subtotal)}
                  </Typography>
                </ListItem>
                <ListItem sx={{ py: 1, px: 0 }}>
                  <ListItemText primary="Phí vận chuyển" />
                  <Typography variant="body1">
                    {formatPrice(shipping)}
                  </Typography>
                </ListItem>
                <ListItem sx={{ py: 1, px: 0 }}>
                  <ListItemText primary="Tổng cộng" primaryTypographyProps={{ fontWeight: 'bold' }} />
                  <Typography variant="subtitle1" fontWeight="bold" color="primary">
                    {formatPrice(total)}
                  </Typography>
                </ListItem>
              </List>
            </Paper>
          </Grid>
        )}
      </Grid>
      
      {/* Cancel Dialog */}
      <Dialog
        open={openCancelDialog}
        onClose={() => setOpenCancelDialog(false)}
      >
        <DialogTitle>
          Hủy thanh toán?
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Bạn có chắc chắn muốn hủy quá trình thanh toán? Giỏ hàng của bạn sẽ được giữ nguyên.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCancelDialog(false)} color="primary">
            Tiếp tục thanh toán
          </Button>
          <Button onClick={handleCancelConfirm} color="error">
            Hủy thanh toán
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Checkout; 