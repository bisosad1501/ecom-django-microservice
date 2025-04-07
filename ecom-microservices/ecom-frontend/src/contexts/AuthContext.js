import React, { createContext, useReducer, useContext, useEffect, useCallback, useMemo } from 'react';
import { authService } from '../services/api';

// Khởi tạo Context
const AuthContext = createContext();

// Reducer function
const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload.user,
        loading: false,
        error: null
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        loading: false,
        error: action.payload
      };
    case 'LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        loading: false,
        error: null
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: true,
        error: null
      };
    case 'UPDATE_USER':
      return {
        ...state,
        user: { ...state.user, ...action.payload },
        loading: false
      };
    default:
      return state;
  }
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, {
    isAuthenticated: false,
    user: null,
    loading: true,
    error: null
  });

  // Kiểm tra xem người dùng đã đăng nhập chưa khi component mount
  useEffect(() => {
    const checkAuth = async () => {
      // Kiểm tra token trong localStorage
      const token = localStorage.getItem('token');
      const userJson = localStorage.getItem('user');

      if (token && userJson) {
        try {
          // Lấy thông tin user từ localStorage
          const user = JSON.parse(userJson);
          
          // Cập nhật state
          dispatch({
            type: 'LOGIN_SUCCESS',
            payload: { user }
          });
          
          // Thêm bước gọi API để xác thực token nếu cần
          // Có thể gọi authService.checkAuth() ở đây
        } catch (error) {
          console.error('Lỗi khi kiểm tra xác thực:', error);
          // Xóa token nếu không hợp lệ
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          localStorage.removeItem('userId');
          
          dispatch({ type: 'LOGOUT' });
        }
      } else {
        dispatch({ type: 'LOGOUT' });
      }
    };

    checkAuth();
  }, []);

  // Đăng nhập - memo hóa với useCallback
  const login = useCallback(async (loginData) => {
    dispatch({ type: 'SET_LOADING' });
    
    try {
      // Nếu đã có dữ liệu từ API, sử dụng nó trực tiếp
      let userData;
      let tokenData;
      
      if (loginData.tokens && loginData.user) {
        // Dữ liệu đã được truyền từ component Login
        userData = loginData.user;
        tokenData = loginData.tokens;
      } else {
        // Cần gọi API login
        const response = await authService.login({
          username: loginData.username,
          password: loginData.password
        });
        if (response.data) {
          userData = response.data.user;
          tokenData = response.data.tokens;
        } else {
          throw new Error('Không nhận được dữ liệu từ API');
        }
      }
      
      if (tokenData && tokenData.access) {
        // Lưu access token
        localStorage.setItem('token', tokenData.access);
        
        // Lưu refresh token nếu có
        if (tokenData.refresh) {
          localStorage.setItem('refreshToken', tokenData.refresh);
        }
        
        // Lưu thông tin user
        if (userData) {
          localStorage.setItem('user', JSON.stringify(userData));
          
          // Lưu userId riêng để dễ sử dụng
          if (userData.id) {
            localStorage.setItem('userId', userData.id);
          }
        }
        
        // Lưu "remember me" nếu được chọn
        if (loginData.remember) {
          localStorage.setItem('remember', 'true');
        } else {
          localStorage.removeItem('remember');
        }
        
        // Cập nhật state
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: { user: userData }
        });
        
        return { success: true };
      } else {
        dispatch({
          type: 'LOGIN_FAILURE',
          payload: 'Đăng nhập không thành công. Thiếu thông tin xác thực.'
        });
        
        return { success: false, error: 'Đăng nhập không thành công' };
      }
    } catch (error) {
      console.error('Lỗi đăng nhập:', error);
      
      let errorMessage = 'Đăng nhập không thành công. Vui lòng thử lại.';
      
      if (error.response) {
        if (error.response.status === 401) {
          errorMessage = 'Tên đăng nhập hoặc mật khẩu không chính xác';
        } else if (error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response.data && error.response.data.message) {
          errorMessage = error.response.data.message;
        }
      }
      
      dispatch({
        type: 'LOGIN_FAILURE',
        payload: errorMessage
      });
      
      return { success: false, error: errorMessage };
    }
  }, []);
  
  // Đăng ký - memo hóa với useCallback
  const register = useCallback(async (userData) => {
    dispatch({ type: 'SET_LOADING' });
    
    try {
      const response = await authService.register({
        username: userData.username,
        email: userData.email,
        password: userData.password,
        confirm_password: userData.confirm_password
      });
      
      if (response.data && response.data.tokens) {
        // Xử lý giống như login
        const token = response.data.tokens.access;
        localStorage.setItem('token', token);
        
        if (response.data.user) {
          localStorage.setItem('user', JSON.stringify(response.data.user));
          
          if (response.data.user.id) {
            localStorage.setItem('userId', response.data.user.id);
          }
        }
        
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: { user: response.data.user }
        });
        
        return { success: true };
      } else if (response.data && response.data.message) {
        // Đăng ký thành công nhưng không có token
        return { success: true };
      } else {
        dispatch({
          type: 'LOGIN_FAILURE',
          payload: 'Đăng ký không thành công. Vui lòng thử lại.'
        });
        
        return { success: false, error: 'Đăng ký không thành công' };
      }
    } catch (error) {
      console.error('Lỗi đăng ký:', error);
      
      let errorMessage = 'Đăng ký không thành công. Vui lòng thử lại.';
      
      if (error.response) {
        if (error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response.data && error.response.data.message) {
          errorMessage = error.response.data.message;
        } else if (error.response.data && error.response.data.email) {
          errorMessage = 'Email này đã được sử dụng';
        } else if (error.response.data && error.response.data.username) {
          errorMessage = 'Tên đăng nhập này đã được sử dụng';
        }
      }
      
      dispatch({
        type: 'LOGIN_FAILURE',
        payload: errorMessage
      });
      
      return { success: false, error: errorMessage };
    }
  }, []);

  // Đăng xuất - memo hóa với useCallback
  const logout = useCallback(() => {
    // Xóa token và thông tin user từ localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    localStorage.removeItem('userId');
    localStorage.removeItem('remember');
    
    // Cập nhật state
    dispatch({ type: 'LOGOUT' });
    
    return { success: true };
  }, []);

  // Cập nhật thông tin user - memo hóa với useCallback
  const updateUser = useCallback(async (userId, userData) => {
    dispatch({ type: 'SET_LOADING' });
    
    try {
      const response = await authService.updateProfile(userId, userData);
      
      if (response.data) {
        // Cập nhật thông tin trong localStorage
        const updatedUser = { ...state.user, ...response.data };
        localStorage.setItem('user', JSON.stringify(updatedUser));
        
        // Cập nhật state
        dispatch({
          type: 'UPDATE_USER',
          payload: response.data
        });
        
        return { success: true };
      } else {
        return { success: false, error: 'Cập nhật không thành công' };
      }
    } catch (error) {
      console.error('Lỗi cập nhật thông tin:', error);
      
      let errorMessage = 'Cập nhật không thành công. Vui lòng thử lại.';
      
      if (error.response && error.response.data && error.response.data.message) {
        errorMessage = error.response.data.message;
      }
      
      return { success: false, error: errorMessage };
    }
  }, [state.user]);

  // Demo login (không gọi API) - memo hóa với useCallback
  const demoLogin = useCallback(() => {
    // Tạo dữ liệu người dùng demo
    const demoUser = {
      id: '331b9209-2526-46c4-9de2-901b50961b9e',
      full_name: 'Nguyễn Văn A',
      email: 'demo@example.com',
      phone: '0987654321',
      address: '123 Đường Lê Lợi',
      city: 'TP. Hồ Chí Minh',
      country: 'Việt Nam',
      postal_code: '70000',
      created_at: new Date().toISOString()
    };
    
    // Lưu thông tin giả lập
    localStorage.setItem('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJleHAiOjE5MDY4OTU0Mzd9.ujwPcJqA8hANuulGkVWTVe2XH4aZM9tllLZ6w1gP62c');
    localStorage.setItem('user', JSON.stringify(demoUser));
    localStorage.setItem('userId', demoUser.id);
    
    // Cập nhật state
    dispatch({
      type: 'LOGIN_SUCCESS',
      payload: { user: demoUser }
    });
    
    return { success: true };
  }, []);

  // Memo hóa các giá trị context để tránh re-render không cần thiết
  const contextValue = useMemo(() => ({
    // State
    isAuthenticated: state.isAuthenticated,
    user: state.user,
    loading: state.loading,
    error: state.error,
    // Methods
    login,
    register,
    logout,
    updateUser,
    demoLogin
  }), [
    state.isAuthenticated,
    state.user,
    state.loading,
    state.error,
    login,
    register,
    logout,
    updateUser,
    demoLogin
  ]);

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook để sử dụng AuthContext
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth phải được sử dụng trong AuthProvider');
  }
  return context;
}; 