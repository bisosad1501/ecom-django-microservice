import { useState, useCallback } from 'react';

/**
 * Custom hook để quản lý thông báo snackbar
 * 
 * @returns {Object} - Các phương thức và state để quản lý snackbar
 */
export const useSnackbar = () => {
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info', // 'error', 'warning', 'info', 'success'
    autoHideDuration: 6000,
    anchorOrigin: { vertical: 'bottom', horizontal: 'left' }
  });
  
  /**
   * Hiển thị thông báo snackbar
   * 
   * @param {string} message - Nội dung thông báo
   * @param {Object} options - Tùy chọn cho snackbar
   * @param {string} options.severity - Mức độ nghiêm trọng ('error', 'warning', 'info', 'success')
   * @param {number} options.autoHideDuration - Thời gian tự động ẩn (ms)
   * @param {Object} options.anchorOrigin - Vị trí hiển thị
   */
  const showSnackbar = useCallback((message, options = {}) => {
    setSnackbar({
      open: true,
      message,
      severity: options.severity || 'info',
      autoHideDuration: options.autoHideDuration || 6000,
      anchorOrigin: options.anchorOrigin || { vertical: 'bottom', horizontal: 'left' }
    });
  }, []);
  
  /**
   * Ẩn thông báo snackbar
   */
  const hideSnackbar = useCallback(() => {
    setSnackbar(prev => ({ ...prev, open: false }));
  }, []);
  
  /**
   * Hiển thị thông báo thành công
   * 
   * @param {string} message - Nội dung thông báo
   * @param {Object} options - Tùy chọn khác
   */
  const showSuccess = useCallback((message, options = {}) => {
    showSnackbar(message, { severity: 'success', ...options });
  }, [showSnackbar]);
  
  /**
   * Hiển thị thông báo lỗi
   * 
   * @param {string} message - Nội dung thông báo
   * @param {Object} options - Tùy chọn khác
   */
  const showError = useCallback((message, options = {}) => {
    showSnackbar(message, { severity: 'error', ...options });
  }, [showSnackbar]);
  
  /**
   * Hiển thị thông báo cảnh báo
   * 
   * @param {string} message - Nội dung thông báo
   * @param {Object} options - Tùy chọn khác
   */
  const showWarning = useCallback((message, options = {}) => {
    showSnackbar(message, { severity: 'warning', ...options });
  }, [showSnackbar]);
  
  /**
   * Hiển thị thông báo thông tin
   * 
   * @param {string} message - Nội dung thông báo
   * @param {Object} options - Tùy chọn khác
   */
  const showInfo = useCallback((message, options = {}) => {
    showSnackbar(message, { severity: 'info', ...options });
  }, [showSnackbar]);
  
  return {
    snackbar,
    showSnackbar,
    hideSnackbar,
    showSuccess,
    showError,
    showWarning,
    showInfo
  };
};

export default useSnackbar; 