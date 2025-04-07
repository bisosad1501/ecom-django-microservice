import React from 'react';
import { Snackbar, Alert } from '@mui/material';

/**
 * Component quản lý hiển thị thông báo toàn cục
 * 
 * @param {Object} snackbar - Cấu hình snackbar từ useSnackbar hook
 * @param {Function} onClose - Hàm xử lý đóng snackbar
 */
const SnackbarManager = ({ snackbar, onClose }) => {
  const { open, message, severity, duration, position, action } = snackbar;
  
  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    
    if (onClose) {
      onClose();
    }
  };
  
  return (
    <Snackbar
      open={open}
      autoHideDuration={duration}
      onClose={handleClose}
      anchorOrigin={position}
    >
      <Alert 
        onClose={handleClose} 
        severity={severity} 
        elevation={6}
        variant="filled"
        sx={{ 
          width: '100%',
          alignItems: 'center'
        }}
        action={action}
      >
        {message}
      </Alert>
    </Snackbar>
  );
};

export default SnackbarManager; 