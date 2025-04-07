import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Button,
  Paper,
  Divider,
  CircularProgress,
  Alert
} from '@mui/material';
import LoginForm from '../components/Auth/LoginForm';
import { authService } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  
  // Lấy redirect path từ location state (nếu có)
  const from = location.state?.from?.pathname || '/';

  const handleSubmit = async (formData) => {
    if (!formData.username || !formData.password) {
      setError('Vui lòng nhập tên đăng nhập và mật khẩu');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      console.log('Đang gửi request đăng nhập với:', { username: formData.username, password: formData.password });
      
      // Sử dụng authService để gọi API đăng nhập
      const response = await authService.login({
        username: formData.username,
        password: formData.password
      });
      
      console.log('Login thành công:', response.data);
      
      if (response.data && response.data.tokens) {
        // Sử dụng context để xử lý đăng nhập
        await login(response.data);
        
        // Chuyển hướng tới trang trước đó hoặc trang chủ
        navigate(from, { replace: true });
      } else {
        console.error('Response không có token:', response.data);
        setError('Đăng nhập không thành công. Vui lòng thử lại.');
      }
    } catch (error) {
      console.error('Chi tiết lỗi đăng nhập:', error);
      
      if (error.response) {
        // Server trả về response với status code nằm ngoài 2xx
        if (error.response.status === 401) {
          setError('Tên đăng nhập hoặc mật khẩu không chính xác');
        } else if (error.response.data && error.response.data.detail) {
          setError(error.response.data.detail);
        } else if (error.response.data && error.response.data.message) {
          setError(error.response.data.message);
        } else {
          setError(`Lỗi ${error.response.status}: ${error.response.statusText}`);
        }
      } else if (error.request) {
        // Request được gửi nhưng không nhận được response
        console.error('Network Error - No Response:', error.request);
        setError('Không thể kết nối đến máy chủ. Vui lòng kiểm tra kết nối mạng và thử lại.');
      } else {
        // Có lỗi khi thiết lập request
        console.error('Request Setup Error:', error.message);
        setError('Có lỗi xảy ra. Vui lòng thử lại sau.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center',
        mt: 8
      }}>
        <LoginForm 
          onSubmit={handleSubmit}
          loading={loading}
          error={error}
        />
        
        <Paper elevation={2} sx={{ p: 3, mt: 3, width: '100%', maxWidth: 450 }}>
          <Typography variant="body2" sx={{ textAlign: 'center', mb: 2, color: 'text.secondary' }}>
            Nếu bạn chưa có tài khoản, vui lòng đăng ký để trải nghiệm dịch vụ
          </Typography>
          
          <Button
            fullWidth
            variant="outlined"
            sx={{ py: 1.2 }}
            onClick={() => navigate('/register')}
          >
            Đăng ký tài khoản mới
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default Login; 