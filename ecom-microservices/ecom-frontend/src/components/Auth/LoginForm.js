import React, { useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  TextField,
  Button,
  Typography,
  Link,
  FormControlLabel,
  Checkbox,
  Alert,
  InputAdornment,
  IconButton,
  Paper
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import './AuthForms.css';

const LoginForm = ({ 
  onSubmit, 
  loading = false, 
  error = '' 
}) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    remember: false
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  
  const handleChange = (e) => {
    const { name, value, checked } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'remember' ? checked : value
    });
    
    // Clear validation error when typing
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };
  
  const toggleShowPassword = () => {
    setShowPassword(!showPassword);
  };
  
  const validate = () => {
    const newErrors = {};
    
    if (!formData.username) {
      newErrors.username = 'Vui lòng nhập tên đăng nhập';
    }
    
    if (!formData.password) {
      newErrors.password = 'Vui lòng nhập mật khẩu';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validate()) {
      onSubmit(formData);
    }
  };
  
  return (
    <Paper className="auth-form-container" elevation={3}>
      <Typography variant="h5" component="h1" className="auth-form-title">
        Đăng nhập
      </Typography>
      
      {error && (
        <Alert severity="error" className="auth-form-alert">
          {error}
        </Alert>
      )}
      
      <Box component="form" onSubmit={handleSubmit} className="auth-form">
        <TextField
          label="Tên đăng nhập"
          variant="outlined"
          fullWidth
          margin="normal"
          name="username"
          value={formData.username}
          onChange={handleChange}
          error={!!errors.username}
          helperText={errors.username}
          disabled={loading}
          required
        />
        
        <TextField
          label="Mật khẩu"
          variant="outlined"
          fullWidth
          margin="normal"
          name="password"
          type={showPassword ? 'text' : 'password'}
          value={formData.password}
          onChange={handleChange}
          error={!!errors.password}
          helperText={errors.password}
          disabled={loading}
          required
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={toggleShowPassword}
                  edge="end"
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
        
        <Box className="auth-form-options">
          <FormControlLabel
            control={
              <Checkbox
                name="remember"
                checked={formData.remember}
                onChange={handleChange}
                color="primary"
                disabled={loading}
              />
            }
            label="Ghi nhớ đăng nhập"
          />
          
          <Link component={RouterLink} to="/forgot-password" className="auth-form-link">
            Quên mật khẩu?
          </Link>
        </Box>
        
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          size="large"
          disabled={loading}
          className="auth-form-button"
        >
          {loading ? 'Đang xử lý...' : 'Đăng nhập'}
        </Button>
        
        <Typography variant="body2" align="center" className="auth-form-footer">
          Chưa có tài khoản?{' '}
          <Link component={RouterLink} to="/register" className="auth-form-link">
            Đăng ký ngay
          </Link>
        </Typography>
      </Box>
    </Paper>
  );
};

export default LoginForm; 