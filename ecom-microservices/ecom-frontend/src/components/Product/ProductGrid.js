import React, { useCallback, useMemo } from 'react';
import { Typography, Box, CircularProgress, Pagination } from '@mui/material';
import { Virtuoso } from 'react-virtuoso';
import { useTheme, useMediaQuery } from '@mui/material';
import ProductCard from '../UI/ProductCard';
import './ProductGrid.css';

// Component row trong virtualization
const ProductGridRow = React.memo(({ products, startIndex, endIndex, onAddToCart, onToggleWishlist, wishlistItems }) => {
  // Chỉ render sản phẩm trong row này
  return products.slice(startIndex, endIndex).map((product, idx) => (
    <Box className="product-grid-item" key={product.id || `product-${startIndex + idx}`}>
      <ProductCard
        product={product}
        onAddToCart={() => onAddToCart(product)}
        onToggleWishlist={() => onToggleWishlist(product.id)}
        inWishlist={wishlistItems.some(item => item.id === product.id)}
      />
    </Box>
  ));
});

const ProductGrid = ({
  products = [],
  loading = false,
  error = '',
  onAddToCart,
  onToggleWishlist,
  wishlistItems = [],
  page = 1,
  totalPages = 1,
  onPageChange,
  emptyMessage = 'Không tìm thấy sản phẩm.',
  itemsPerRow = 4
}) => {
  const theme = useTheme();
  
  // Responsive columns
  const isExtraSmall = useMediaQuery(theme.breakpoints.down('sm'));
  const isSmall = useMediaQuery(theme.breakpoints.between('sm', 'md'));
  const isMedium = useMediaQuery(theme.breakpoints.between('md', 'lg'));
  
  // Xác định số cột dựa trên kích thước màn hình
  const columnsPerRow = useMemo(() => {
    if (isExtraSmall) return 1;
    if (isSmall) return 2;
    if (isMedium) return 3;
    return itemsPerRow;
  }, [isExtraSmall, isSmall, isMedium, itemsPerRow]);
  
  // Số rows cần hiển thị
  const totalRows = useMemo(() => {
    return Math.ceil(products.length / columnsPerRow);
  }, [products.length, columnsPerRow]);
  
  // Kiểm tra sản phẩm có trong wishlist không
  const isInWishlist = useCallback((productId) => {
    return wishlistItems.some(item => item.id === productId);
  }, [wishlistItems]);
  
  // Handle pagination
  const handlePageChange = useCallback((event, value) => {
    if (onPageChange) {
      onPageChange(value);
    }
    // Scroll to top khi chuyển trang
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [onPageChange]);

  // Row renderer cho virtualization
  const rowRenderer = useCallback(index => {
    const startIndex = index * columnsPerRow;
    const endIndex = Math.min(startIndex + columnsPerRow, products.length);
    
    return (
      <div className="product-grid-row">
        <ProductGridRow 
          products={products}
          startIndex={startIndex}
          endIndex={endIndex}
          onAddToCart={onAddToCart}
          onToggleWishlist={onToggleWishlist}
          wishlistItems={wishlistItems}
        />
      </div>
    );
  }, [products, columnsPerRow, onAddToCart, onToggleWishlist, wishlistItems]);

  if (loading) {
    return (
      <Box className="product-grid-loading">
        <CircularProgress />
        <Typography variant="body1" sx={{ mt: 2 }}>
          Đang tải sản phẩm...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box className="product-grid-error">
        <Typography variant="body1" color="error">
          {error}
        </Typography>
      </Box>
    );
  }

  if (!products.length) {
    return (
      <Box className="product-grid-empty">
        <Typography variant="body1">
          {emptyMessage}
        </Typography>
      </Box>
    );
  }

  // Sử dụng react-virtuoso cho danh sách sản phẩm lớn
  return (
    <Box className="product-grid-container">
      {products.length > 20 ? (
        <Box className="product-grid-virtualized">
          <Virtuoso
            totalCount={totalRows}
            itemContent={rowRenderer}
            style={{ height: '100%', minHeight: '800px' }}
            increaseViewportBy={{ top: 300, bottom: 300 }}
            components={{
              Footer: () => (
                totalPages > 1 ? (
                  <Box className="product-grid-pagination">
                    <Pagination
                      count={totalPages}
                      page={page}
                      onChange={handlePageChange}
                      color="primary"
                      siblingCount={1}
                      size="large"
                    />
                  </Box>
                ) : null
              )
            }}
          />
        </Box>
      ) : (
        // Cách hiển thị thông thường cho số lượng nhỏ sản phẩm
        <>
          <Box className="product-grid">
            {products.map((product) => (
              <Box className="product-grid-item" key={product.id}>
                <ProductCard
                  product={product}
                  onAddToCart={() => onAddToCart(product)}
                  onToggleWishlist={() => onToggleWishlist(product.id)}
                  inWishlist={isInWishlist(product.id)}
                />
              </Box>
            ))}
          </Box>

          {totalPages > 1 && (
            <Box className="product-grid-pagination">
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="primary"
                siblingCount={1}
                size="large"
              />
            </Box>
          )}
        </>
      )}
    </Box>
  );
};

export default React.memo(ProductGrid); 