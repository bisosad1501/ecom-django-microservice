# Chiến lược tối ưu hóa hiệu suất

Tài liệu này mô tả tất cả các chiến lược tối ưu hóa được áp dụng trong dự án ecom-frontend.

## Tóm tắt các chiến lược

1. **Code Splitting & Lazy Loading**
   - Sử dụng React.lazy và Suspense
   - Ưu tiên phân chia theo routes
   - Prefetching thông minh với requestIdleCallback

2. **Memo hóa & React Performance**
   - useMemo & useCallback tối ưu
   - React.memo cho components đắt
   - Virtualization cho danh sách lớn

3. **Tối ưu hóa Context API**
   - Tạo cấu trúc tối ưu cho Providers
   - Memo hóa context value
   - Tách nhỏ contexts để tránh re-render không cần thiết

4. **Tải và Hiển thị hình ảnh**
   - Lazy loading với Intersection Observer
   - Tối ưu để tránh Cumulative Layout Shift (CLS)
   - Progressive loading với placeholder

5. **Background Tasks**
   - Web Workers cho tác vụ nặng
   - Inline workers với Blob URLs

## Chi tiết triển khai

### 1. Code Splitting & Lazy Loading

**routes.js**
```jsx
const Home = lazy(() => import('./pages/Home'));
const ProductList = lazy(() => import('./pages/ProductList'));
```

- **Tính năng Prefetching**: Sử dụng requestIdleCallback để tải trước các routes phổ biến
- **Ưu tiên theo route**: Phân chia components theo route, tải khi cần
- **Phân loại ưu tiên**: High, Medium, Low theo tần suất sử dụng

### 2. Memo hóa & React Performance

**ProductCard.js**
```jsx
const areEqual = (prevProps, nextProps) => {
  return prevProps.id === nextProps.id && 
         prevProps.inWishlist === nextProps.inWishlist;
}

export default memo(ProductCard, areEqual);
```

- **useCallback**: Sử dụng cho event handlers và callbacks để tránh tạo functions mới mỗi lần render
- **useMemo**: Sử dụng cho calculated values phức tạp
- **Virtualization**: Áp dụng trong ProductGrid với react-virtuoso để xử lý danh sách lớn

### 3. Tối ưu hóa Context API

**CartContext.js**
```jsx
const contextValue = useMemo(() => ({
  cart: state,
  addToCart,
  updateQuantity,
  removeItem,
  clearCart,
}), [state, addToCart, updateQuantity, removeItem, clearCart]);
```

- **Re-render tối thiểu**: Sử dụng memo hóa để giảm re-render
- **Tách context theo chức năng**: Auth, Cart, Products riêng biệt
- **State hoisting**: Tách component để giảm render scope

### 4. Tải và Hiển thị hình ảnh

**useIntersectionObserver.js**
```jsx
// Sử dụng với Image component
const [ref, isInView, isLoaded, setIsLoaded, shouldLoad] = useLazyImage();
```

- **Intersection Observer API**: Chỉ tải hình ảnh khi chúng sắp hiển thị trong viewport
- **Placeholder**: Sử dụng thumbnails hoặc blur-up placeholders
- **aspect-ratio**: Luôn đặt kích thước ảnh trước để tránh layout shift

### 5. Background Tasks

**useBackgroundCallback.js**
```jsx
const { execute, result, error, loading } = useBackgroundCallback(
  (data) => complexProcessing(data), 
  { immediate: false }
);
```

- **Web Workers**: Chuyển các tác vụ nặng sang background thread
- **Thread an toàn**: Xử lý lỗi và tự động fallback khi cần
- **Async execution**: Hỗ trợ cả Promise và sync operations

## Cách sử dụng

### 1. Sử dụng React.memo đúng cách

```jsx
// Khi nào sử dụng memo:
// 1. Component render thường xuyên với props không đổi
// 2. Component có nhiều logic render phức tạp
// 3. Component là "pure component" - chỉ phụ thuộc vào props

// Khi nào không sử dụng memo:
// 1. Component đơn giản, render nhanh
// 2. Component gần như luôn nhận props khác mỗi lần re-render
```

### 2. Virtualization cho danh sách lớn

```jsx
// Cho mọi danh sách có thể mở rộng lớn hơn ~20 items
<Virtuoso
  totalCount={rows}
  itemContent={index => <RowComponent data={data[index]} />}
  components={{ Footer }}
/>
```

### 3. Lazy loading Images

```jsx
const ProductImage = ({ src, alt }) => {
  const [ref, isVisible, isLoaded, setIsLoaded, shouldLoad] = useLazyImage();
  
  return (
    <div ref={ref} className="product-image-container">
      {shouldLoad ? (
        <img
          src={src}
          alt={alt}
          className={`product-image ${isLoaded ? 'loaded' : ''}`}
          onLoad={() => setIsLoaded(true)}
        />
      ) : null}
      {!isLoaded && <div className="product-image-skeleton" />}
    </div>
  );
};
```

### 4. Sử dụng hooks cho tác vụ nặng

```jsx
const FilterComponent = ({ products }) => {
  const { execute, result, loading } = useBackgroundCallback(
    (products) => {
      // Phức tạp, CPU-intensive operations
      return products.filter(complexFiltering).map(complexMapping);
    }
  );
  
  const handleApplyFilter = () => {
    execute(products);
  };
  
  return (
    <div>
      <button onClick={handleApplyFilter} disabled={loading}>
        Apply Filters
      </button>
      {loading ? <Spinner /> : <ResultList results={result} />}
    </div>
  );
};
```

## Công cụ đo lường hiệu suất

1. **Lighthouse**: Đánh giá toàn diện
2. **Chrome DevTools Performance tab**: Phân tích runtime
3. **React DevTools Profiler**: Đo lường render
4. **Web Vitals API**: Đo lường Core Web Vitals trong thực tế

## Kết luận

Hiệu suất web nên được xem là một tính năng quan trọng, không phải một công việc tối ưu sau này. Các chiến lược được triển khai trong dự án này cân bằng giữa developer experience và user experience, với ưu tiên cho trải nghiệm người dùng.

Luôn đo lường trước khi tối ưu và tập trung vào những gì người dùng thực sự cảm nhận được.

## Ví dụ tối ưu hóa trang chi tiết sản phẩm

Trang ProductDetail là một ví dụ điển hình về cách áp dụng các chiến lược tối ưu hóa hiệu suất. Dưới đây là cách chúng tôi đã cải thiện hiệu suất cho trang này:

### 1. Chia nhỏ component theo chức năng

```jsx
// Thay vì một component lớn, chúng tôi tách thành các component nhỏ hơn:
const ProductImages = lazy(() => import('../components/Product/ProductImages'));
const ProductInfo = lazy(() => import('../components/Product/ProductInfo'));
const ProductDescription = lazy(() => import('../components/Product/ProductDescription'));
const ProductReviews = lazy(() => import('../components/Product/ProductReviews'));
const ProductDetails = lazy(() => import('../components/Product/ProductDetails'));
```

### 2. Lazy loading theo khu vực hiển thị

```jsx
// Trong component ProductDetail.js
<Grid item xs={12} md={6}>
  <Suspense fallback={<Box sx={{ height: 500, display: 'flex', justifyContent: 'center', alignItems: 'center' }}><CircularProgress /></Box>}>
    <ProductImages product={product} />
  </Suspense>
</Grid>
```

### 3. Memo hóa để tránh re-render không cần thiết

```jsx
// Memoize component nhỏ trong ProductInfo.js
const ProductPrice = memo(({ product }) => {
  const hasDiscount = product.sale_price && product.sale_price < product.base_price;
  
  return (
    <Box sx={{ mb: 3, p: 2, bgcolor: '#f9f9f9', borderRadius: 1 }}>
      {/* Nội dung hiển thị giá */}
    </Box>
  );
});
```

### 4. Sử dụng Intersection Observer cho hình ảnh

```jsx
// Trong ProductImages.js
const [imageRef, isVisible] = useIntersectionObserver({
  threshold: 0.1,
  triggerOnce: true
});

// Chỉ tải ảnh khi isVisible === true
<CardMedia
  component="img"
  height="500"
  image={isVisible ? mainImage : ''}
  alt={product.name}
  sx={{ 
    objectFit: 'contain', 
    p: 2,
    display: imageLoaded ? 'block' : 'none'
  }}
  onLoad={handleImageLoad}
  loading="lazy"
/>
```

### 5. Xử lý phân trang trong đánh giá sản phẩm

```jsx
// Trong ProductReviews.js
const [page, setPage] = useState(1);
const reviewsPerPage = 5;

// Chỉ hiển thị một phần reviews thay vì tất cả
const currentReviews = reviews.slice(
  (page - 1) * reviewsPerPage,
  page * reviewsPerPage
);
```

### 6. Lazy load ảnh trong đánh giá

```jsx
// Trong ReviewItem component
const [reviewImagesRef, reviewImagesVisible] = useIntersectionObserver({
  threshold: 0.1,
  triggerOnce: true
});

// Chỉ hiển thị ảnh khi phần đánh giá hiển thị trong viewport
{reviewImagesVisible && review.images.map((image, index) => (
  <Box
    key={index}
    component="img"
    src={image}
    alt={`Ảnh đánh giá ${index + 1}`}
    sx={{ width: 80, height: 80, borderRadius: 1 }}
    loading="lazy"
  />
))}
```

### Kết quả đạt được

- **Giảm thời gian tải ban đầu**: Bằng cách tải theo nhu cầu, trang hiển thị nhanh hơn
- **Tối ưu hóa CLS**: Sử dụng skeleton và đặt kích thước trước cho hình ảnh
- **Ưu tiên nội dung quan trọng**: Hiển thị thông tin sản phẩm trước, lazy load phần ít quan trọng hơn
- **Cấu trúc code tốt hơn**: Dễ bảo trì và mở rộng nhờ chia nhỏ component

## Công cụ đo lường hiệu suất

1. **Lighthouse**: Đánh giá toàn diện
2. **Chrome DevTools Performance tab**: Phân tích runtime
3. **React DevTools Profiler**: Đo lường render
4. **Web Vitals API**: Đo lường Core Web Vitals trong thực tế

## Kết luận

Hiệu suất web nên được xem là một tính năng quan trọng, không phải một công việc tối ưu sau này. Các chiến lược được triển khai trong dự án này cân bằng giữa developer experience và user experience, với ưu tiên cho trải nghiệm người dùng.

Luôn đo lường trước khi tối ưu và tập trung vào những gì người dùng thực sự cảm nhận được. 