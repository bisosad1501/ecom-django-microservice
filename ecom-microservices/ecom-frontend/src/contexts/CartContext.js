import React, { createContext, useReducer, useContext, useEffect, useCallback, useMemo } from 'react';
import { cartService } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

// Khởi tạo Context
const CartContext = createContext();

// Reducer function để xử lý các action
const cartReducer = (state, action) => {
  switch (action.type) {
    case 'SET_CART':
      return {
        ...state,
        items: action.payload,
        loading: false,
        error: null
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: true,
        error: null
      };
    case 'SET_ERROR':
      return {
        ...state,
        loading: false,
        error: action.payload
      };
    case 'ADD_ITEM':
      // Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
      const existingItemIndex = state.items.findIndex(
        item => item.product_id === action.payload.product_id
      );
      
      if (existingItemIndex >= 0) {
        // Nếu sản phẩm đã tồn tại, cập nhật số lượng
        const updatedItems = [...state.items];
        updatedItems[existingItemIndex] = {
          ...updatedItems[existingItemIndex],
          quantity: updatedItems[existingItemIndex].quantity + action.payload.quantity,
          subtotal: (updatedItems[existingItemIndex].price * (updatedItems[existingItemIndex].quantity + action.payload.quantity))
        };
        
        return {
          ...state,
          items: updatedItems,
          loading: false
        };
      } else {
        // Nếu sản phẩm chưa có, thêm mới
        return {
          ...state,
          items: [...state.items, action.payload],
          loading: false
        };
      }
    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map(item => {
          if (item.id === action.payload.itemId) {
            return {
              ...item,
              quantity: action.payload.quantity,
              subtotal: item.price * action.payload.quantity
            };
          }
          return item;
        }),
        loading: false
      };
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload),
        loading: false
      };
    case 'CLEAR_CART':
      return {
        ...state,
        items: [],
        loading: false
      };
    case 'RESET_CART':
      return {
        items: [],
        loading: false,
        error: null
      };
    default:
      return state;
  }
};

// Provider component
export const CartProvider = ({ children }) => {
  const { isAuthenticated, user } = useAuth();
  const [state, dispatch] = useReducer(cartReducer, {
    items: [],
    loading: false,
    error: null
  });

  // Tính tổng giá trị giỏ hàng - memo hóa với useMemo
  const calculateTotal = useMemo(() => {
    return state.items.reduce((total, item) => total + (item.price * item.quantity), 0);
  }, [state.items]);

  // Tính phí vận chuyển - memo hóa với useMemo
  const calculateShipping = useMemo(() => {
    // Miễn phí vận chuyển nếu đơn hàng trên 500,000 VNĐ
    return calculateTotal > 500000 ? 0 : 30000;
  }, [calculateTotal]);

  // Lấy giỏ hàng từ server - memo hóa với useCallback
  const fetchCart = useCallback(async () => {
    if (!isAuthenticated || !user || !user.id) {
      dispatch({ type: 'RESET_CART' });
      return;
    }

    dispatch({ type: 'SET_LOADING' });
    try {
      const response = await cartService.getCart(user.id);
      if (response.data && response.data.items) {
        // Map CartItems từ API response
        const mappedItems = response.data.items.map(item => ({
          ...item,
          price: item.sale_price,
          imageUrl: item.image,
          name: item.product_name
        }));
        dispatch({ type: 'SET_CART', payload: mappedItems });
      } else {
        dispatch({ type: 'SET_CART', payload: [] });
      }
    } catch (error) {
      console.error('Lỗi khi lấy giỏ hàng:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Không thể tải giỏ hàng' });
    }
  }, [isAuthenticated, user]);

  // Thêm sản phẩm vào giỏ hàng - memo hóa với useCallback
  const addToCart = useCallback(async (product, quantity = 1) => {
    if (!isAuthenticated || !user || !user.id) {
      console.log('Người dùng chưa đăng nhập, không thể thêm vào giỏ hàng');
      return null;
    }

    dispatch({ type: 'SET_LOADING' });
    try {
      // Call API to add to cart
      await cartService.addToCart({
        user_id: user.id,
        product_id: product._id || product.id,
        quantity
      });

      // Add to local state
      const cartItem = {
        id: Math.random().toString(36).substr(2, 9), // Tạm thời tạo ID
        product_id: product._id || product.id,
        product_name: product.name,
        image: product.primary_image || product.image,
        price: product.sale_price || product.price,
        quantity,
        subtotal: (product.sale_price || product.price) * quantity
      };

      dispatch({ type: 'ADD_ITEM', payload: cartItem });
      return true;
    } catch (error) {
      console.error('Lỗi khi thêm vào giỏ hàng:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Không thể thêm vào giỏ hàng' });
      return false;
    }
  }, [isAuthenticated, user]);

  // Cập nhật số lượng - memo hóa với useCallback
  const updateQuantity = useCallback(async (itemId, newQuantity) => {
    if (newQuantity < 1) return false;

    if (!isAuthenticated || !user || !user.id) {
      console.log('Người dùng chưa đăng nhập, không thể cập nhật giỏ hàng');
      return false;
    }

    // Tìm thông tin sản phẩm để lấy product_id
    const item = state.items.find(item => item.id === itemId);
    if (!item) return false;

    try {
      // Cập nhật local state trước
      dispatch({ 
        type: 'UPDATE_QUANTITY', 
        payload: { itemId, quantity: newQuantity } 
      });

      // Call API to update cart
      await cartService.updateCart({
        user_id: user.id,
        product_id: item.product_id,
        quantity: newQuantity
      });

      return true;
    } catch (error) {
      console.error('Lỗi khi cập nhật số lượng:', error);
      // Reload cart to sync with server
      fetchCart();
      return false;
    }
  }, [state.items, fetchCart, isAuthenticated, user]);

  // Xóa sản phẩm khỏi giỏ hàng - memo hóa với useCallback
  const removeItem = useCallback(async (itemId) => {
    if (!isAuthenticated || !user || !user.id) {
      console.log('Người dùng chưa đăng nhập, không thể xóa khỏi giỏ hàng');
      return false;
    }

    // Tìm thông tin sản phẩm để lấy product_id
    const item = state.items.find(item => item.id === itemId);
    if (!item) return false;

    try {
      // Cập nhật local state trước
      dispatch({ type: 'REMOVE_ITEM', payload: itemId });

      // Call API to remove from cart
      await cartService.removeFromCart({
        user_id: user.id,
        product_id: item.product_id
      });

      return true;
    } catch (error) {
      console.error('Lỗi khi xóa sản phẩm:', error);
      // Reload cart to sync with server
      fetchCart();
      return false;
    }
  }, [state.items, fetchCart, isAuthenticated, user]);

  // Xóa toàn bộ giỏ hàng - memo hóa với useCallback
  const clearCart = useCallback(async () => {
    if (!isAuthenticated || !user || !user.id) {
      console.log('Người dùng chưa đăng nhập, không thể xóa giỏ hàng');
      dispatch({ type: 'RESET_CART' });
      return false;
    }

    try {
      // Update local state first
      dispatch({ type: 'CLEAR_CART' });

      // Call API to clear cart
      await cartService.clearCart(user.id);
      return true;
    } catch (error) {
      console.error('Lỗi khi xóa giỏ hàng:', error);
      // Reload cart to sync with server
      fetchCart();
      return false;
    }
  }, [fetchCart, isAuthenticated, user]);

  // Reset giỏ hàng (không gọi API, chỉ xóa state)
  const resetCart = useCallback(() => {
    dispatch({ type: 'RESET_CART' });
  }, []);

  // Load cart khi đăng nhập hoặc thay đổi user
  useEffect(() => {
    if (isAuthenticated && user) {
      fetchCart();
    } else {
      resetCart();
    }
  }, [isAuthenticated, user, fetchCart, resetCart]);

  // Memo hóa context value
  const contextValue = useMemo(() => ({
    cart: state,
    addToCart,
    updateQuantity,
    removeItem,
    clearCart,
    resetCart,
    fetchCart,
    calculateTotal,
    calculateShipping
  }), [
    state,
    addToCart,
    updateQuantity,
    removeItem,
    clearCart,
    resetCart,
    fetchCart,
    calculateTotal,
    calculateShipping
  ]);

  return (
    <CartContext.Provider value={contextValue}>
      {children}
    </CartContext.Provider>
  );
};

// Custom hook để sử dụng CartContext
export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart phải được sử dụng trong CartProvider');
  }
  return context;
}; 