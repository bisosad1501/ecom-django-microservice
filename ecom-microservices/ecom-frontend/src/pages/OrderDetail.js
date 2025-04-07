import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Divider,
  Chip,
  CircularProgress,
  Button,
  Card,
  CardContent,
  CardMedia,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert
} from '@mui/material';
import { 
  LocalShipping as ShippingIcon, 
  Payment as PaymentIcon,
  Schedule as ScheduleIcon,
  Check as CheckIcon
} from '@mui/icons-material';
import { orderService, paymentService, shipmentService } from '../services/api';

const OrderDetail = () => {
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [shipmentData, setShipmentData] = useState(null);
  const [paymentData, setPaymentData] = useState(null);

  useEffect(() => {
    const fetchOrderDetails = async () => {
      setLoading(true);
      try {
        // Lấy thông tin đơn hàng
        const orderResponse = await orderService.getOrderById(id);
        setOrder(orderResponse.data);
        
        // Lấy thông tin vận chuyển nếu có
        if (orderResponse.data.shipment_id) {
          try {
            const shipmentResponse = await shipmentService.getShipmentById(orderResponse.data.shipment_id);
            setShipmentData(shipmentResponse.data);
          } catch (error) {
            console.error('Lỗi khi lấy thông tin vận chuyển:', error);
          }
        }
        
        // Lấy thông tin thanh toán nếu có
        if (orderResponse.data.payment_id) {
          try {
            const paymentResponse = await paymentService.getPaymentStatus(orderResponse.data.payment_id);
            setPaymentData(paymentResponse.data);
          } catch (error) {
            console.error('Lỗi khi lấy thông tin thanh toán:', error);
          }
        }
      } catch (error) {
        console.error('Lỗi khi lấy chi tiết đơn hàng:', error);
        setError('Không thể tải thông tin đơn hàng. Vui lòng thử lại sau.');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchOrderDetails();
    }
  }, [id]);

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending':
      case 'chờ xử lý':
        return 'warning';
      case 'processing':
      case 'đang xử lý':
        return 'info';
      case 'shipped':
      case 'đã giao hàng':
        return 'success';
      case 'cancelled':
      case 'đã hủy':
        return 'error';
      case 'completed':
      case 'hoàn thành':
        return 'success';
      default:
        return 'default';
    }
  };

  const getPaymentStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'paid':
      case 'đã thanh toán':
        return 'success';
      case 'pending':
      case 'chờ thanh toán':
        return 'warning';
      case 'failed':
      case 'thất bại':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatPrice = (price) => {
    if (price === undefined || price === null) return 'N/A';
    return price.toLocaleString() + ' VNĐ';
  };

  // Tạo đơn hàng giả nếu không có dữ liệu từ API
  const dummyOrder = {
    id: id,
    order_number: `ORD-${id}`,
    status: 'Chờ xử lý',
    created_at: new Date().toISOString(),
    total_amount: 1250000,
    shipping_address: {
      full_name: 'Nguyễn Văn A',
      phone: '0987654321',
      address: '123 Đường Lê Lợi, Quận 1',
      city: 'TP. Hồ Chí Minh',
      country: 'Việt Nam',
      postal_code: '70000'
    },
    items: [
      {
        id: 1,
        product_id: '101',
        product_name: 'Laptop Asus VivoBook',
        quantity: 1,
        price: 950000,
        image: 'https://via.placeholder.com/150'
      },
      {
        id: 2,
        product_id: '203',
        product_name: 'Chuột không dây Logitech',
        quantity: 2,
        price: 150000,
        image: 'https://via.placeholder.com/150'
      }
    ],
    payment_method: 'Thanh toán khi nhận hàng (COD)',
    shipping_method: 'Giao hàng tiêu chuẩn',
    shipping_fee: 30000,
    subtotal: 1220000,
    notes: ''
  };

  // Sử dụng đơn hàng từ API hoặc đơn hàng giả
  const orderData = order || dummyOrder;

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
        Chi tiết đơn hàng
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            Đơn hàng #{orderData.order_number}
          </Typography>
          <Chip 
            label={orderData.status} 
            color={getStatusColor(orderData.status)}
            icon={<CheckIcon />}
          />
        </Box>
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="body2" color="text.secondary">
            <ScheduleIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 1 }} />
            Ngày đặt hàng: {formatDate(orderData.created_at)}
          </Typography>
        </Box>

        <Divider sx={{ my: 2 }} />
        
        <Grid container spacing={3}>
          {/* Thông tin địa chỉ giao hàng */}
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom>
              Thông tin giao hàng
            </Typography>
            <Box sx={{ bgcolor: 'background.default', p: 2, borderRadius: 1 }}>
              <Typography variant="body1">
                {orderData.shipping_address.full_name}
              </Typography>
              <Typography variant="body2">
                {orderData.shipping_address.phone}
              </Typography>
              <Typography variant="body2">
                {orderData.shipping_address.address}
              </Typography>
              <Typography variant="body2">
                {orderData.shipping_address.city}, {orderData.shipping_address.country} {orderData.shipping_address.postal_code}
              </Typography>
            </Box>
          </Grid>
          
          {/* Thông tin vận chuyển và thanh toán */}
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom>
              Phương thức thanh toán & vận chuyển
            </Typography>
            <Box sx={{ bgcolor: 'background.default', p: 2, borderRadius: 1 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <PaymentIcon fontSize="small" sx={{ mr: 1 }} />
                <Typography variant="body2">
                  {orderData.payment_method}
                </Typography>
                {paymentData && (
                  <Chip 
                    label={paymentData.status} 
                    color={getPaymentStatusColor(paymentData.status)}
                    size="small"
                    sx={{ ml: 1 }}
                  />
                )}
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <ShippingIcon fontSize="small" sx={{ mr: 1 }} />
                <Typography variant="body2">
                  {orderData.shipping_method}
                </Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>
      </Paper>
      
      {/* Sản phẩm trong đơn hàng */}
      <Typography variant="h6" sx={{ mb: 2 }}>
        Sản phẩm
      </Typography>
      
      <TableContainer component={Paper} sx={{ mb: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Sản phẩm</TableCell>
              <TableCell align="right">Giá</TableCell>
              <TableCell align="center">Số lượng</TableCell>
              <TableCell align="right">Tổng</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {orderData.items.map((item) => (
              <TableRow key={item.id}>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box 
                      component="img" 
                      src={item.image} 
                      alt={item.product_name}
                      sx={{ width: 50, height: 50, objectFit: 'cover', mr: 2 }}
                    />
                    <Typography variant="body2">
                      {item.product_name}
                    </Typography>
                  </Box>
                </TableCell>
                <TableCell align="right">{formatPrice(item.price)}</TableCell>
                <TableCell align="center">{item.quantity}</TableCell>
                <TableCell align="right">{formatPrice(item.price * item.quantity)}</TableCell>
              </TableRow>
            ))}
            
            {/* Tổng hóa đơn */}
            <TableRow>
              <TableCell colSpan={2} />
              <TableCell align="right">
                <Typography variant="body2">Tạm tính</Typography>
              </TableCell>
              <TableCell align="right">
                {formatPrice(orderData.subtotal)}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell colSpan={2} />
              <TableCell align="right">
                <Typography variant="body2">Phí vận chuyển</Typography>
              </TableCell>
              <TableCell align="right">
                {formatPrice(orderData.shipping_fee)}
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell colSpan={2} />
              <TableCell align="right">
                <Typography variant="subtitle1">Tổng cộng</Typography>
              </TableCell>
              <TableCell align="right">
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                  {formatPrice(orderData.total_amount)}
                </Typography>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
      
      {/* Thông tin vận chuyển nếu có */}
      {shipmentData && (
        <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Thông tin vận chuyển
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <ShippingIcon sx={{ mr: 1 }} />
            <Typography variant="body1">
              Mã vận đơn: {shipmentData.tracking_number}
            </Typography>
          </Box>
          <Typography variant="body2">
            Dự kiến giao hàng: {formatDate(shipmentData.estimated_delivery_date)}
          </Typography>
        </Paper>
      )}
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button 
          variant="outlined" 
          component={Link} 
          to="/orders"
        >
          Quay lại danh sách đơn hàng
        </Button>
        
        {orderData.status.toLowerCase() === 'pending' || orderData.status.toLowerCase() === 'chờ xử lý' ? (
          <Button 
            variant="contained" 
            color="error"
            onClick={() => orderService.cancelOrder(id)}
          >
            Hủy đơn hàng
          </Button>
        ) : null}
      </Box>
    </Container>
  );
};

export default OrderDetail; 