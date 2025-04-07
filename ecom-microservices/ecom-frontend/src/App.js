import React, { Suspense, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import Header from './components/Layout/Header';
import { Container, CircularProgress, Box, Typography } from '@mui/material';
import { ErrorBoundary } from './components/UI/ErrorBoundary';

// Lazy loading trang với prefetch
const Home = React.lazy(() => import('./pages/Home'));
const Login = React.lazy(() => import('./pages/Login'));
const Register = React.lazy(() => import('./pages/Register'));
const ProductDetail = React.lazy(() => import('./pages/ProductDetail'));
const ProductList = React.lazy(() => import('./pages/ProductList'));
const BookList = React.lazy(() => import('./pages/BookList'));
const ShoeList = React.lazy(() => import('./pages/ShoeList'));
const Cart = React.lazy(() => import('./pages/Cart'));
const Checkout = React.lazy(() => import('./pages/Checkout'));
const Profile = React.lazy(() => import('./pages/Profile'));
const Orders = React.lazy(() => import('./pages/Orders'));
const OrderDetail = React.lazy(() => import('./pages/OrderDetail'));
const Wishlist = React.lazy(() => import('./pages/Wishlist'));
const Search = React.lazy(() => import('./pages/Search'));

// Prefetch các routes phổ biến
const prefetchRoutes = () => {
  // Prefetch các trang người dùng thường xem
  const prefetchPromises = [
    import('./pages/Home'),
    import('./pages/ProductList'),
    import('./pages/Cart')
  ];
  
  // Thực hiện prefetch một cách không chặn
  Promise.all(prefetchPromises).catch(err => 
    console.log('Prefetch không ảnh hưởng đến ứng dụng:', err)
  );
};

// Loading component cải tiến
const Loading = () => (
  <Box 
    sx={{ 
      display: 'flex', 
      flexDirection: 'column',
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '60vh' 
    }}
  >
    <CircularProgress color="primary" size={50} thickness={4} />
    <Typography variant="body1" sx={{ mt: 2 }}>
      Đang tải nội dung...
    </Typography>
  </Box>
);

// Component lắng nghe route change để prefetch data
const RoutePrefetcher = () => {
  const location = useLocation();
  
  useEffect(() => {
    // Detect route có thể prefetch khi user vào một trang
    if (location.pathname === '/products') {
      // Prefetch chi tiết sản phẩm phổ biến 
      import('./pages/ProductDetail');
    } else if (location.pathname === '/cart') {
      // Prefetch checkout khi vào giỏ hàng
      import('./pages/Checkout');
    }
  }, [location.pathname]);
  
  return null;
};

function App() {
  // Prefetch routes khi app load xong
  useEffect(() => {
    // Sử dụng requestIdleCallback nếu browser hỗ trợ, nếu không dùng setTimeout
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(prefetchRoutes, { timeout: 2000 });
    } else {
      setTimeout(prefetchRoutes, 2000);
    }
  }, []);
  
  return (
    <>
      <CssBaseline />
      <Router>
        <Header />
        <ErrorBoundary>
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Suspense fallback={<Loading />}>
              <RoutePrefetcher />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/products" element={<ProductList />} />
                <Route path="/products/:id" element={<ProductDetail />} />
                <Route path="/books" element={<BookList />} />
                <Route path="/books/:id" element={<Navigate to="/products/:id" replace />} />
                <Route path="/shoes" element={<ShoeList />} />
                <Route path="/shoes/:id" element={<Navigate to="/products/:id" replace />} />
                <Route path="/cart" element={<Cart />} />
                <Route path="/checkout" element={<Checkout />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/orders" element={<Orders />} />
                <Route path="/orders/:id" element={<OrderDetail />} />
                <Route path="/wishlist" element={<Wishlist />} />
                <Route path="/search" element={<Search />} />
              </Routes>
            </Suspense>
          </Container>
        </ErrorBoundary>
      </Router>
    </>
  );
}

export default App;
