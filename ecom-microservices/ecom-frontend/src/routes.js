import React, { lazy, Suspense } from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import ErrorBoundary from './components/UI/ErrorBoundary';

// Layout
const MainLayout = lazy(() => import('./layouts/MainLayout'));
const AdminLayout = lazy(() => import('./layouts/AdminLayout'));

// Prefetch component để prefetch các routes sau khi component đã mount 
const Prefetch = ({ children }) => {
  const prefetchRoutes = React.useCallback(() => {
    // Prefetch các route phổ biến nhất
    import('./pages/Home');
    import('./pages/ProductList');
    import('./pages/ProductDetail');
    import('./pages/Cart');
    import('./pages/Login');
    import('./pages/Register');
  }, []);

  React.useEffect(() => {
    // Chỉ prefetch khi browser không bận
    if (typeof window !== 'undefined' && 'requestIdleCallback' in window) {
      window.requestIdleCallback(prefetchRoutes, { timeout: 2000 });
    } else {
      // Fallback cho browsers không hỗ trợ requestIdleCallback
      setTimeout(prefetchRoutes, 1000);
    }
  }, [prefetchRoutes]);

  return children;
};

// Tạo một HOC để xử lý loading và error cho lazy components
const withSuspense = (Component, loadingProps = {}) => {
  return (props) => (
    <ErrorBoundary>
      <Suspense fallback={<LoadingFallback {...loadingProps} />}>
        <Component {...props} />
      </Suspense>
    </ErrorBoundary>
  );
};

// Loading fallback component
const LoadingFallback = ({ minHeight = '70vh' }) => (
  <Box sx={{ 
    display: 'flex', 
    justifyContent: 'center', 
    alignItems: 'center', 
    minHeight,
    width: '100%',
  }}>
    <CircularProgress color="primary" />
  </Box>
);

// Routes với priority loading 
// High priority - load ngay lập tức
const Home = lazy(() => import('./pages/Home'));
const ProductList = lazy(() => import('./pages/ProductList'));
const ProductDetail = lazy(() => import('./pages/ProductDetail'));
const Cart = lazy(() => import('./pages/Cart'));
const Checkout = lazy(() => import('./pages/Checkout'));

// Medium priority - low priority prefetch
const Login = lazy(() => 
  import(/* webpackPrefetch: true */ './pages/Login')
);
const Register = lazy(() => 
  import(/* webpackPrefetch: true */ './pages/Register')
);

// Low priority - load on demand
const NotFound = lazy(() => import('./pages/NotFound'));
const About = lazy(() => import('./pages/About'));
const Contact = lazy(() => import('./pages/Contact'));
const Profile = lazy(() => import('./pages/Profile'));
const OrderHistory = lazy(() => import('./pages/OrderHistory'));
const OrderDetail = lazy(() => import('./pages/OrderDetail'));
const Wishlist = lazy(() => import('./pages/Wishlist'));

// Admin pages - load riêng biệt
const AdminDashboard = lazy(() => import('./pages/Admin/Dashboard'));
const AdminProducts = lazy(() => import('./pages/Admin/Products'));
const AdminOrders = lazy(() => import('./pages/Admin/Orders'));
const AdminCustomers = lazy(() => import('./pages/Admin/Customers'));

// Prefetch on hover hook
function usePrefetchOnHover(Component) {
  return (e) => {
    // Bắt đầu prefetch khi hover
    // Đối với dynamic imports, chỉ cần gọi là đã prefetch
    if (Component && Component.preload) {
      Component.preload();
    }
  };
}

const AppRoutes = () => {
  return (
    <Prefetch>
      <Routes>
        <Route path="/" element={withSuspense(MainLayout)()} errorElement={<ErrorBoundary />}>
          <Route index element={withSuspense(Home)()} />
          <Route path="products" element={withSuspense(ProductList)()} />
          <Route path="products/:id" element={withSuspense(ProductDetail)()} />
          <Route path="cart" element={withSuspense(Cart)()} />
          <Route path="checkout" element={withSuspense(Checkout)()} />
          <Route path="login" element={withSuspense(Login)()} />
          <Route path="register" element={withSuspense(Register)()} />
          <Route path="about" element={withSuspense(About)()} />
          <Route path="contact" element={withSuspense(Contact)()} />
          <Route path="profile" element={withSuspense(Profile)()} />
          <Route path="orders" element={withSuspense(OrderHistory)()} />
          <Route path="orders/:id" element={withSuspense(OrderDetail)()} />
          <Route path="wishlist" element={withSuspense(Wishlist)()} />
          <Route path="*" element={withSuspense(NotFound)()} />
        </Route>
        
        <Route path="/admin" element={withSuspense(AdminLayout)()} errorElement={<ErrorBoundary />}>
          <Route index element={withSuspense(AdminDashboard)()} />
          <Route path="products" element={withSuspense(AdminProducts)()} />
          <Route path="orders" element={withSuspense(AdminOrders)()} />
          <Route path="customers" element={withSuspense(AdminCustomers)()} />
        </Route>
      </Routes>
    </Prefetch>
  );
};

export default AppRoutes;
export { usePrefetchOnHover }; 