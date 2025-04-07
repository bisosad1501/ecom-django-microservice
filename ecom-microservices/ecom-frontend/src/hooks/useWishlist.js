import { useState, useEffect, useCallback } from 'react';
import { productService } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

/**
 * Custom hook để quản lý danh sách yêu thích
 * 
 * @returns {Object} - Các phương thức và state để quản lý wishlist
 */
export const useWishlist = () => {
  const { isAuthenticated, user } = useAuth();
  const [wishlist, setWishlist] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Lấy danh sách yêu thích từ server
  const fetchWishlist = useCallback(async () => {
    if (!isAuthenticated || !user) {
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await productService.getWishlist(user.id);
      
      if (response.data && response.data.items) {
        setWishlist(response.data.items);
      } else {
        setWishlist([]);
      }
    } catch (err) {
      console.error('Lỗi khi lấy danh sách yêu thích:', err);
      setError('Không thể tải danh sách yêu thích. Vui lòng thử lại sau.');
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, user]);
  
  // Thêm sản phẩm vào danh sách yêu thích
  const addToWishlist = useCallback(async (product) => {
    if (!isAuthenticated || !user) {
      return { success: false, message: 'Vui lòng đăng nhập để thêm vào danh sách yêu thích' };
    }
    
    setLoading(true);
    
    try {
      const productId = product._id || product.id;
      await productService.addToWishlist(user.id, productId);
      
      // Thêm vào state
      const newItem = {
        id: productId,
        product_id: productId,
        product_name: product.name,
        image: product.primary_image || product.image,
        price: product.price || product.sale_price
      };
      
      setWishlist(prev => [...prev, newItem]);
      
      return { success: true, message: 'Đã thêm sản phẩm vào danh sách yêu thích' };
    } catch (err) {
      console.error('Lỗi khi thêm vào danh sách yêu thích:', err);
      return { 
        success: false, 
        message: 'Không thể thêm vào danh sách yêu thích. Vui lòng thử lại sau.' 
      };
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, user]);
  
  // Xóa sản phẩm khỏi danh sách yêu thích
  const removeFromWishlist = useCallback(async (productId) => {
    if (!isAuthenticated || !user) {
      return { success: false, message: 'Vui lòng đăng nhập để thực hiện thao tác này' };
    }
    
    setLoading(true);
    
    try {
      await productService.removeFromWishlist(user.id, productId);
      
      // Cập nhật state
      setWishlist(prev => prev.filter(item => 
        item.id !== productId && item.product_id !== productId
      ));
      
      return { success: true, message: 'Đã xóa sản phẩm khỏi danh sách yêu thích' };
    } catch (err) {
      console.error('Lỗi khi xóa khỏi danh sách yêu thích:', err);
      return { 
        success: false, 
        message: 'Không thể xóa khỏi danh sách yêu thích. Vui lòng thử lại sau.' 
      };
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, user]);
  
  // Kiểm tra sản phẩm có trong danh sách yêu thích không
  const isInWishlist = useCallback((productId) => {
    return wishlist.some(item => 
      item.id === productId || item.product_id === productId
    );
  }, [wishlist]);
  
  // Toggle sản phẩm trong danh sách yêu thích
  const toggleWishlistItem = useCallback(async (product) => {
    const productId = product._id || product.id;
    
    if (isInWishlist(productId)) {
      return removeFromWishlist(productId);
    } else {
      return addToWishlist(product);
    }
  }, [isInWishlist, removeFromWishlist, addToWishlist]);
  
  // Lấy danh sách khi component mount hoặc người dùng thay đổi
  useEffect(() => {
    fetchWishlist();
  }, [fetchWishlist]);
  
  return {
    wishlist,
    loading,
    error,
    isInWishlist,
    addToWishlist,
    removeFromWishlist,
    toggleWishlistItem,
    fetchWishlist
  };
}; 