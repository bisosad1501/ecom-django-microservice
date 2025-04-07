import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  CircularProgress,
  Alert,
  Divider
} from '@mui/material';
import { orderService } from '../services/api';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchOrders = async () => {
      setLoading(true);
      try {
        const response = await orderService.getOrders();
        setOrders(response.data);
      } catch (error) {
        console.error('Lỗi khi lấy danh sách đơn hàng:', error);
        setError('Không thể tải danh sách đơn hàng. Vui lòng thử lại sau.');
        
        // Tạo dữ liệu giả để demo
        setOrders([
          {
            id: '1',
            order_number: 'ORD-001',
            created_at: '2023-04-01T10:30:00Z',
            status: 'Hoàn thành',
            total_amount: 1250000,
            items_count: 3
          },
          {
            id: '2',
            order_number: 'ORD-002',
            created_at: '2023-04-05T14:45:00Z',
            status: 'Đang xử lý',
            total_amount: 850000,
            items_count: 2
          },
          {
            id: '3',
            order_number: 'ORD-003',
            created_at: '2023-04-10T09:15:00Z',
            status: 'Chờ xử lý',
            total_amount: 550000,
            items_count: 1
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

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
        return 'primary';
      case 'delivered':
      case 'đã nhận hàng':
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

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatPrice = (price) => {
    return price.toLocaleString() + ' VNĐ';
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
        Đơn hàng của tôi
      </Typography>
      
      <Divider sx={{ mb: 4 }} />
      
      {error && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {orders.length > 0 ? (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Mã đơn hàng</TableCell>
                <TableCell>Ngày đặt</TableCell>
                <TableCell>Tổng tiền</TableCell>
                <TableCell>Trạng thái</TableCell>
                <TableCell>Hành động</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {orders.map((order) => (
                <TableRow key={order.id}>
                  <TableCell>
                    <Typography variant="body2">
                      {order.order_number}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {order.items_count} sản phẩm
                    </Typography>
                  </TableCell>
                  <TableCell>{formatDate(order.created_at)}</TableCell>
                  <TableCell>{formatPrice(order.total_amount)}</TableCell>
                  <TableCell>
                    <Chip 
                      label={order.status} 
                      color={getStatusColor(order.status)} 
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Button 
                      variant="contained" 
                      component={Link} 
                      to={`/orders/${order.id}`}
                      size="small"
                    >
                      Chi tiết
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ) : (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" gutterBottom>
            Bạn chưa có đơn hàng nào
          </Typography>
          <Typography variant="body1" sx={{ mb: 3 }}>
            Hãy tiếp tục khám phá cửa hàng và mua sắm ngay!
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
    </Container>
  );
};

export default Orders; 