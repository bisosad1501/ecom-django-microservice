import axios from 'axios';

// Đánh dấu khi file api.js được load
console.log('API service loaded at:', new Date().toISOString());

// Xác định URL API dựa trên môi trường
const determineApiUrl = () => {
  // Trong môi trường phát triển, sử dụng API Gateway chạy trên localhost
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost'; // API Gateway port 80
  }
  
  // Khi chạy trong container, sử dụng tên service
  return process.env.REACT_APP_API_URL || 'http://api-gateway';
};

const API_URL = determineApiUrl();

console.log('Using API URL:', API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: false,
  timeout: 30000
});

// Interceptor để thêm token xác thực và debug
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Log request để debug
    console.log('Request Config:', {
      url: config.url,
      method: config.method,
      baseURL: config.baseURL,
      headers: config.headers,
      data: config.data
    });
    
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Interceptor để xử lý response và log chi tiết lỗi
api.interceptors.response.use(
  (response) => {
    console.log('Response Success:', response.status);
    return response;
  },
  (error) => {
    // Log chi tiết lỗi
    console.error('Response Error:', {
      message: error.message,
      code: error.code,
      stack: error.stack,
      response: error.response ? {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers
      } : 'No response'
    });
    
    if (error.response) {
      return Promise.reject(error.response.data);
    }
    return Promise.reject(error);
  }
);

// Các API service
export const authService = {
  login: (credentials) => {
    // Đảm bảo format chính xác cho dữ liệu đăng nhập
    const loginData = {
      username: credentials.username,
      password: credentials.password
    };
    console.log('Login credentials:', loginData);
    console.log('Login URL:', API_URL + '/api/users/login/');
    return api.post('/api/users/login/', loginData);
  },
  register: (userData) => api.post('/api/users/register/', userData),
  checkAuth: () => api.get('/api/users/check/'),
  getProfile: (userId) => api.get(`/api/users/${userId}/`),
  updateProfile: (userId, userData) => api.put(`/api/users/${userId}/`, userData),
};

export const productService = {
  getProducts: (params) => api.get('/api/products/', { params }),
  getProductById: (id) => api.get(`/api/products/${id}/`),
  getFeaturedProducts: () => api.get('/api/products/', { params: { featured: true } }),
  getNewArrivals: () => api.get('/api/products/latest_products/'),
  getBestSellers: () => api.get('/api/products/best_sellers/'),
  getCategories: () => api.get('/api/products/get_categories/'),
  getWishlist: (userId) => api.get(`/api/wishlist/${userId}/`),
  addToWishlist: (userId, productId) => api.post('/api/wishlist/add/', { user_id: userId, product_id: productId }),
  removeFromWishlist: (userId, productId) => api.delete(`/api/wishlist/remove/${productId}/?user_id=${userId}`),
  getProductReviews: (productId) => api.get(`/api/reviews/product_reviews/${productId}/`),
  getBrands: () => Promise.resolve({
    data: [
      { id: 'apple', name: 'Apple' },
      { id: 'samsung', name: 'Samsung' },
      { id: 'xiaomi', name: 'Xiaomi' },
      { id: 'oppo', name: 'OPPO' },
      { id: 'vivo', name: 'Vivo' },
      { id: 'nike', name: 'Nike' },
      { id: 'adidas', name: 'Adidas' },
      { id: 'puma', name: 'Puma' },
      { id: 'sony', name: 'Sony' },
      { id: 'lg', name: 'LG' },
      { id: 'panasonic', name: 'Panasonic' }
    ]
  }),
  searchProducts: (query) => api.get('/api/products/', { params: { search: query } }),
  getRelatedProducts: (productId) => api.get(`/api/products/${productId}/related/`),
  filterProducts: (filters) => {
    // Convert filters to API parameters
    const params = {};
    if (filters.product_type) params.product_type = filters.product_type;
    if (filters.min_price) params.min_price = filters.min_price;
    if (filters.max_price) params.max_price = filters.max_price;
    if (filters.brand) params.brand = filters.brand;
    if (filters.min_rating) params.min_rating = filters.min_rating;
    if (filters.search) params.search = filters.search;
    
    return api.get('/api/products/', { params });
  },
};

export const bookService = {
  getBooks: (params) => api.get('/api/books/', { params }),
  getBookById: (id) => api.get(`/api/books/${id}/`),
  getBooksInCategory: (category) => api.get('/api/books/', { params: { category } }),
};

export const shoeService = {
  getShoes: (params) => api.get('/api/shoes/', { params }),
  getShoeById: (id) => api.get(`/api/shoes/${id}/`),
  getShoesInCategory: (category) => api.get('/api/shoes/', { params: { category } }),
};

export const cartService = {
  getCart: (userId) => {
    if (!userId) {
      console.error('getCart missing userId');
      return Promise.reject('Missing userId');
    }
    return api.get(`/api/cart/get/${userId}/`);
  },
  addToCart: (item) => {
    console.log('Adding to cart with data:', item);
    return api.post('/api/cart/add-item/', item);
  },
  updateCart: (item) => api.post('/api/cart/update-item/', item),
  removeFromCart: (data) => api.post('/api/cart/remove-item/', data),
  clearCart: (userId) => {
    if (!userId) {
      console.error('clearCart missing userId');
      return Promise.reject('Missing userId');
    }
    return api.post('/api/cart/clear/', { user_id: userId });
  }
};

export const orderService = {
  createOrder: (orderData) => api.post('/api/orders/', orderData),
  getOrders: () => api.get('/api/orders/'),
  getOrderById: (id) => api.get(`/api/orders/${id}/`),
  cancelOrder: (id) => api.put(`/api/orders/${id}/cancel/`),
};

export const paymentService = {
  processPayment: (paymentData) => api.post('/api/payments/process/', paymentData),
  getPaymentStatus: (paymentId) => api.get(`/api/payments/${paymentId}/`),
};

export const shipmentService = {
  getShipmentMethods: () => api.get('/api/shipments/methods/'),
  getShipmentById: (id) => api.get(`/api/shipments/${id}/`),
  trackShipment: (trackingNumber) => api.get(`/api/shipments/track/${trackingNumber}/`),
};

export const reviewService = {
  getReviews: (productId) => api.get(`/api/reviews/product_reviews/${productId}/`),
  addReview: (reviewData) => api.post('/api/reviews/create_review/', reviewData),
  getUserReviews: (userId) => api.get(`/api/reviews/user_reviews/${userId}/`),
  voteReview: (reviewId, vote) => api.post(`/api/reviews/vote/${reviewId}/`, { vote }),
  reportReview: (reviewId) => api.post(`/api/reviews/report/${reviewId}/`),
  addComment: (reviewId, comment) => api.post(`/api/reviews/add_comment/${reviewId}/`, { comment }),
  updateRating: (reviewId, rating) => api.patch(`/api/reviews/update_rating/${reviewId}/`, { rating }),
};

export const recommendationService = {
  getRecommendations: (userId) => api.get(`/api/recommendations/user/${userId}/`),
  getSimilarProducts: (productId) => api.get(`/api/recommendations/similar/${productId}/`),
  getPopularProducts: () => api.get('/api/recommendations/popular/'),
};

export const wishlistService = {
  getWishlist: () => api.get('/api/wishlist/'),
  addToWishlist: (productId) => api.post('/api/wishlist/add/', { product_id: productId }),
  removeFromWishlist: (productId) => api.delete(`/api/wishlist/remove/${productId}/`),
};

export default api;