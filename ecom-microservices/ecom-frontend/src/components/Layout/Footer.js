import React from 'react';
import { Box, Container, Grid, Typography, Link, Divider } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  return (
    <Box component="footer" className="footer">
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Về chúng tôi
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Ecom là nền tảng thương mại điện tử hàng đầu, cung cấp đa dạng sản phẩm
              với chất lượng cao và dịch vụ khách hàng xuất sắc.
            </Typography>
          </Grid>
          
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Liên kết
            </Typography>
            <Link component={RouterLink} to="/" color="inherit" display="block" gutterBottom>
              Trang chủ
            </Link>
            <Link component={RouterLink} to="/products" color="inherit" display="block" gutterBottom>
              Sản phẩm
            </Link>
            <Link component={RouterLink} to="/cart" color="inherit" display="block" gutterBottom>
              Giỏ hàng
            </Link>
            <Link component={RouterLink} to="/profile" color="inherit" display="block" gutterBottom>
              Tài khoản
            </Link>
          </Grid>
          
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Liên hệ
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Email: contact@ecom.com
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Điện thoại: (84) 123 456 789
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Địa chỉ: 123 Đường ABC, Quận XYZ, TP. Hồ Chí Minh
            </Typography>
          </Grid>
        </Grid>
        
        <Divider sx={{ my: 3 }} />
        
        <Typography variant="body2" color="text.secondary" align="center">
          © {new Date().getFullYear()} Ecom. Tất cả quyền được bảo lưu.
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer; 