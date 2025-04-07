import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  TextField,
  Button,
  Avatar,
  Divider,
  Tabs,
  Tab,
  Alert,
  CircularProgress
} from '@mui/material';
import { 
  Person as PersonIcon,
  Edit as EditIcon,
  Save as SaveIcon,
  Cancel as CancelIcon 
} from '@mui/icons-material';
import { authService } from '../services/api';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [editMode, setEditMode] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    country: '',
    postalCode: ''
  });

  useEffect(() => {
    const fetchUserProfile = async () => {
      setLoading(true);
      try {
        // Thử lấy thông tin người dùng từ localStorage trước
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          const userData = JSON.parse(storedUser);
          setUser(userData);
          
          // Khởi tạo formData từ thông tin người dùng
          setFormData({
            fullName: userData.full_name || userData.name || '',
            email: userData.email || '',
            phone: userData.phone || '',
            address: userData.address || '',
            city: userData.city || '',
            country: userData.country || '',
            postalCode: userData.postal_code || ''
          });
        } else {
          // Nếu không có trong localStorage, tạo dữ liệu giả
          const dummyUser = {
            id: '1',
            full_name: 'Nguyễn Văn A',
            email: 'nguyenvana@example.com',
            phone: '0987654321',
            address: '123 Đường Lê Lợi',
            city: 'TP. Hồ Chí Minh',
            country: 'Việt Nam',
            postal_code: '70000',
            created_at: '2023-01-15T10:30:00Z'
          };
          
          setUser(dummyUser);
          setFormData({
            fullName: dummyUser.full_name,
            email: dummyUser.email,
            phone: dummyUser.phone,
            address: dummyUser.address,
            city: dummyUser.city,
            country: dummyUser.country,
            postalCode: dummyUser.postal_code
          });
        }
      } catch (error) {
        console.error('Lỗi khi lấy thông tin người dùng:', error);
        setError('Không thể tải thông tin tài khoản. Vui lòng thử lại sau.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleEditToggle = () => {
    if (editMode) {
      // Nếu đang trong chế độ chỉnh sửa, reset form data
      setFormData({
        fullName: user.full_name || user.name || '',
        email: user.email || '',
        phone: user.phone || '',
        address: user.address || '',
        city: user.city || '',
        country: user.country || '',
        postalCode: user.postal_code || ''
      });
    }
    setEditMode(!editMode);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      // Trong triển khai thực tế, sẽ gửi dữ liệu cập nhật lên server
      // Nhưng hiện tại, chỉ cập nhật dữ liệu local
      const updatedUser = {
        ...user,
        full_name: formData.fullName,
        email: formData.email,
        phone: formData.phone,
        address: formData.address,
        city: formData.city,
        country: formData.country,
        postal_code: formData.postalCode
      };
      
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      setSuccess('Cập nhật thông tin tài khoản thành công!');
      setEditMode(false);
    } catch (error) {
      console.error('Lỗi khi cập nhật thông tin người dùng:', error);
      setError('Không thể cập nhật thông tin tài khoản. Vui lòng thử lại sau.');
    } finally {
      setLoading(false);
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

  if (loading && !user) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', my: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Tài khoản của tôi
      </Typography>
      
      <Divider sx={{ mb: 4 }} />
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          {success}
        </Alert>
      )}
      
      <Grid container spacing={4}>
        {/* Sidebar */}
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Avatar 
              sx={{ 
                width: 100, 
                height: 100, 
                mx: 'auto', 
                mb: 2,
                bgcolor: 'primary.main'
              }}
            >
              <PersonIcon sx={{ fontSize: 60 }} />
            </Avatar>
            
            <Typography variant="h6" gutterBottom>
              {user.full_name || user.name}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {user.email}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Thành viên từ: {formatDate(user.created_at)}
            </Typography>
            
            <Divider sx={{ my: 2 }} />
            
            <Button 
              component={Link}
              to="/orders"
              variant="outlined"
              fullWidth
              sx={{ mb: 1 }}
            >
              Đơn hàng của tôi
            </Button>
            <Button 
              component={Link}
              to="/wishlist"
              variant="outlined"
              fullWidth
            >
              Danh sách yêu thích
            </Button>
          </Paper>
        </Grid>
        
        {/* Main content */}
        <Grid item xs={12} md={9}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={tabValue} onChange={handleTabChange}>
                <Tab label="Thông tin cá nhân" />
                <Tab label="Địa chỉ" />
                <Tab label="Bảo mật" />
              </Tabs>
            </Box>
            
            {/* Thông tin cá nhân */}
            {tabValue === 0 && (
              <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
                      {editMode ? (
                        <>
                          <Button
                            type="submit"
                            variant="contained"
                            startIcon={<SaveIcon />}
                            sx={{ mr: 1 }}
                            disabled={loading}
                          >
                            {loading ? <CircularProgress size={24} /> : 'Lưu'}
                          </Button>
                          <Button
                            variant="outlined"
                            startIcon={<CancelIcon />}
                            onClick={handleEditToggle}
                            disabled={loading}
                          >
                            Hủy
                          </Button>
                        </>
                      ) : (
                        <Button
                          variant="outlined"
                          startIcon={<EditIcon />}
                          onClick={handleEditToggle}
                        >
                          Chỉnh sửa
                        </Button>
                      )}
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Họ và tên"
                      name="fullName"
                      value={formData.fullName}
                      onChange={handleChange}
                      disabled={!editMode}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      disabled={!editMode}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Số điện thoại"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      disabled={!editMode}
                    />
                  </Grid>
                </Grid>
              </Box>
            )}
            
            {/* Địa chỉ */}
            {tabValue === 1 && (
              <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
                      {editMode ? (
                        <>
                          <Button
                            type="submit"
                            variant="contained"
                            startIcon={<SaveIcon />}
                            sx={{ mr: 1 }}
                            disabled={loading}
                          >
                            {loading ? <CircularProgress size={24} /> : 'Lưu'}
                          </Button>
                          <Button
                            variant="outlined"
                            startIcon={<CancelIcon />}
                            onClick={handleEditToggle}
                            disabled={loading}
                          >
                            Hủy
                          </Button>
                        </>
                      ) : (
                        <Button
                          variant="outlined"
                          startIcon={<EditIcon />}
                          onClick={handleEditToggle}
                        >
                          Chỉnh sửa
                        </Button>
                      )}
                    </Box>
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Địa chỉ"
                      name="address"
                      value={formData.address}
                      onChange={handleChange}
                      disabled={!editMode}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Thành phố"
                      name="city"
                      value={formData.city}
                      onChange={handleChange}
                      disabled={!editMode}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Quốc gia"
                      name="country"
                      value={formData.country}
                      onChange={handleChange}
                      disabled={!editMode}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Mã bưu điện"
                      name="postalCode"
                      value={formData.postalCode}
                      onChange={handleChange}
                      disabled={!editMode}
                    />
                  </Grid>
                </Grid>
              </Box>
            )}
            
            {/* Bảo mật */}
            {tabValue === 2 && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Thay đổi mật khẩu
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Mật khẩu hiện tại"
                      type="password"
                      name="currentPassword"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Mật khẩu mới"
                      type="password"
                      name="newPassword"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Xác nhận mật khẩu mới"
                      type="password"
                      name="confirmPassword"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Button
                      variant="contained"
                      color="primary"
                    >
                      Cập nhật mật khẩu
                    </Button>
                  </Grid>
                </Grid>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Profile; 