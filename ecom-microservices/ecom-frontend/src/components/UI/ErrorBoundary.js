import React, { Component } from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

/**
 * Component ErrorBoundary để bắt và xử lý lỗi trong React
 */
export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false,
      error: null,
      errorInfo: null 
    };
  }

  static getDerivedStateFromError(error) {
    // Cập nhật state để hiển thị fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Có thể log lỗi đến dịch vụ error reporting
    console.error('Error caught by ErrorBoundary:', error, errorInfo);
    this.setState({ errorInfo });
    
    // Có thể gửi lỗi đến một service như Sentry hoặc Firebase Crashlytics
    // report(error);
  }

  handleRetry = () => {
    // Làm mới trang để khôi phục ứng dụng
    window.location.reload();
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box 
          sx={{ 
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '60vh',
            py: 4
          }}
        >
          <Paper 
            elevation={3} 
            sx={{ 
              p: 4, 
              maxWidth: 600, 
              borderRadius: 2,
              textAlign: 'center'
            }}
          >
            <ErrorOutlineIcon color="error" sx={{ fontSize: 60, mb: 2 }} />
            
            <Typography variant="h5" color="error" gutterBottom>
              Đã xảy ra lỗi không mong muốn
            </Typography>
            
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              Thật đáng tiếc, đã có sự cố xảy ra khi tải trang này. Đội ngũ kỹ thuật của chúng tôi đã được thông báo về vấn đề này.
            </Typography>

            {process.env.NODE_ENV === 'development' && this.state.error && (
              <Box 
                sx={{ 
                  mt: 2, 
                  p: 2, 
                  bgcolor: 'grey.100', 
                  borderRadius: 1,
                  textAlign: 'left',
                  overflow: 'auto',
                  maxHeight: 300
                }}
              >
                <Typography variant="body2" component="pre" sx={{ fontSize: '0.85rem', mb: 1 }}>
                  {this.state.error.toString()}
                </Typography>
                {this.state.errorInfo && (
                  <Typography variant="body2" component="pre" sx={{ fontSize: '0.75rem' }}>
                    {this.state.errorInfo.componentStack}
                  </Typography>
                )}
              </Box>
            )}

            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 2 }}>
              <Button 
                variant="contained" 
                color="primary" 
                onClick={this.handleRetry}
              >
                Tải lại trang
              </Button>
              <Button 
                variant="outlined" 
                onClick={() => window.location.href = '/'}
              >
                Về trang chủ
              </Button>
            </Box>
          </Paper>
        </Box>
      );
    }

    // Nếu không có lỗi, render children
    return this.props.children;
  }
} 