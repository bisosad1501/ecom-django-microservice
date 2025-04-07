import React from 'react';
import { Button, CircularProgress } from '@mui/material';
import './CustomButton.css';

const CustomButton = ({
  children,
  loading = false,
  variant = 'contained',
  color = 'primary', 
  fullWidth = false,
  startIcon,
  endIcon,
  onClick,
  disabled = false,
  type = 'button',
  size = 'medium',
  className = '',
  ...props
}) => {
  return (
    <Button
      variant={variant}
      color={color}
      fullWidth={fullWidth}
      startIcon={!loading && startIcon}
      endIcon={!loading && endIcon}
      onClick={onClick}
      disabled={disabled || loading}
      type={type}
      size={size}
      className={`custom-button ${className}`}
      {...props}
    >
      {loading ? (
        <>
          <CircularProgress size={24} color="inherit" className="button-loader" />
          <span className="button-text-hidden">{children}</span>
        </>
      ) : (
        children
      )}
    </Button>
  );
};

export default CustomButton; 