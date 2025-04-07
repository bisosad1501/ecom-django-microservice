import { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { productService } from '../services/api';

/**
 * Custom hook để quản lý danh sách sản phẩm và các trạng thái liên quan
 * 
 * @param {Object} initialFilters - Filters ban đầu
 * @returns {Object} - Trạng thái và các hàm xử lý
 */
export const useProducts = (initialFilters = {}) => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // State
  const [loading, setLoading] = useState(true);
  const [products, setProducts] = useState([]);
  const [totalPages, setTotalPages] = useState(1);
  const [page, setPage] = useState(1);
  const [sort, setSort] = useState('newest');
  const [filters, setFilters] = useState({
    category: '',
    price: [0, 50000000],
    brand: [],
    rating: 0,
    ...initialFilters
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState('');
  const [productType, setProductType] = useState('');
  
  // State cho categories và brands
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [categoriesLoading, setCategoriesLoading] = useState(false);
  const [brandsLoading, setBrandsLoading] = useState(false);
  
  // Tham chiếu cho cache
  const cache = useRef({
    products: new Map(),
    categories: null,
    brands: null,
    lastFetch: {
      products: null,
      categories: null,
      brands: null
    }
  });
  
  // Kiểm tra cache có hết hạn chưa (5 phút)
  const isCacheExpired = useCallback((cacheType) => {
    const lastFetch = cache.current.lastFetch[cacheType];
    if (!lastFetch) return true;
    
    const now = Date.now();
    const fiveMinutes = 5 * 60 * 1000;
    return now - lastFetch > fiveMinutes;
  }, []);
  
  // Tạo cache key từ tham số
  const getCacheKey = useCallback((page, sort, filters) => {
    return `${page}-${sort}-${JSON.stringify(filters)}`;
  }, []);
  
  // Format sản phẩm từ API response
  const formatProduct = useCallback((product) => {
    return {
      id: product._id || product.id,
      name: product.name || 'Sản phẩm không tên',
      description: product.description || '',
      price: product.price || product.base_price || 0,
      sale_price: product.sale_price || product.price || 0,
      primary_image: product.primary_image || product.image || '/images/product-placeholder.jpg',
      images: product.images || [],
      rating: product.rating || 0,
      product_type: product.product_type || productType,
      brand: product.brand || '',
      category: product.category || ''
    };
  }, [productType]);
  
  // Hàm lấy sản phẩm từ API
  const fetchProducts = useCallback(async (currentPage, currentSort, currentFilters) => {
    setLoading(true);
    setError('');
    
    // Tạo cache key
    const cacheKey = getCacheKey(currentPage, currentSort, currentFilters);
    
    // Kiểm tra cache
    if (cache.current.products.has(cacheKey) && !isCacheExpired('products')) {
      const cachedData = cache.current.products.get(cacheKey);
      setProducts(cachedData.products);
      setTotalPages(cachedData.totalPages);
      setLoading(false);
      return;
    }
    
    try {
      // Chuẩn bị tham số cho API
      const params = {
        page: currentPage,
        limit: 12,
        sort: currentSort,
        category: currentFilters.category,
        min_price: currentFilters.price?.[0] || 0,
        max_price: currentFilters.price?.[1] || 50000000,
        brands: Array.isArray(currentFilters.brand) 
          ? currentFilters.brand.join(',') 
          : currentFilters.brand,
        rating: currentFilters.rating || 0,
        search: currentFilters.search || searchQuery
      };
      
      // Thêm product_type nếu có
      if (currentFilters.product_type) {
        params.product_type = currentFilters.product_type;
      }
      
      const response = await productService.getProducts(params);
      
      // Xử lý cả hai trường hợp API trả về: mảng phẳng hoặc đối tượng có phân trang
      let formattedProducts = [];
      let totalPages = 1;
      
      if (response.data) {
        if (Array.isArray(response.data)) {
          // Trường hợp API trả về mảng phẳng
          formattedProducts = response.data.map(formatProduct);
          totalPages = 1;
        } else if (response.data.results) {
          // Trường hợp API trả về đối tượng có phân trang
          formattedProducts = response.data.results.map(formatProduct);
          totalPages = response.data.total_pages || Math.ceil(response.data.count / 12) || 1;
        }
      }
      
      // Cập nhật cache
      cache.current.products.set(cacheKey, {
        products: formattedProducts,
        totalPages
      });
      cache.current.lastFetch.products = Date.now();
      
      // Cập nhật state
      setProducts(formattedProducts);
      setTotalPages(totalPages);
    } catch (error) {
      console.error('Error fetching products:', error);
      setError('Không thể tải danh sách sản phẩm. Vui lòng thử lại sau.');
      setProducts([]);
      setTotalPages(1);
    } finally {
      setLoading(false);
    }
  }, [getCacheKey, isCacheExpired, formatProduct, searchQuery]);
  
  // Hàm lấy danh mục từ API
  const fetchCategories = useCallback(async () => {
    // Kiểm tra cache
    if (cache.current.categories && !isCacheExpired('categories')) {
      setCategories(cache.current.categories);
      return;
    }
    
    setCategoriesLoading(true);
    try {
      const response = await productService.getCategories();
      if (response.data) {
        setCategories(response.data);
        
        // Cập nhật cache
        cache.current.categories = response.data;
        cache.current.lastFetch.categories = Date.now();
      }
    } catch (error) {
      console.error('Error fetching categories:', error);
      setCategories([]);
    } finally {
      setCategoriesLoading(false);
    }
  }, [isCacheExpired]);
  
  // Hàm lấy thương hiệu từ API
  const fetchBrands = useCallback(async () => {
    // Kiểm tra cache
    if (cache.current.brands && !isCacheExpired('brands')) {
      setBrands(cache.current.brands);
      return;
    }
    
    setBrandsLoading(true);
    try {
      const response = await productService.getBrands();
      if (response.data) {
        setBrands(response.data);
        
        // Cập nhật cache
        cache.current.brands = response.data;
        cache.current.lastFetch.brands = Date.now();
      }
    } catch (error) {
      console.error('Error fetching brands:', error);
      setBrands([]);
    } finally {
      setBrandsLoading(false);
    }
  }, [isCacheExpired]);

  // Xử lý thay đổi URL
  const updateUrlFromState = useCallback((newPage, newSort, newFilters, newSearch, newType) => {
    const searchParams = new URLSearchParams();
    
    // Thêm các tham số vào URL
    if (newPage && newPage !== 1) searchParams.set('page', newPage.toString());
    if (newSort && newSort !== 'newest') searchParams.set('sort', newSort);
    if (newFilters.category) searchParams.set('category', newFilters.category);
    if (newSearch) searchParams.set('search', newSearch);
    
    // Thêm price range nếu khác mặc định
    if (newFilters.price && (newFilters.price[0] !== 0 || newFilters.price[1] !== 50000000)) {
      searchParams.set('price', `${newFilters.price[0]}-${newFilters.price[1]}`);
    }
    
    // Thêm brands nếu có
    if (newFilters.brand && newFilters.brand.length > 0) {
      searchParams.set('brands', Array.isArray(newFilters.brand) 
        ? newFilters.brand.join(',') 
        : newFilters.brand);
    }
    
    // Thêm rating nếu có
    if (newFilters.rating && newFilters.rating > 0) {
      searchParams.set('rating', newFilters.rating.toString());
    }
    
    // Thêm product_type nếu có
    if (newType) {
      searchParams.set('type', newType);
    }
    
    navigate(`${location.pathname}?${searchParams.toString()}`);
  }, [location.pathname, navigate]);

  // Xử lý tham số từ URL khi component mount hoặc URL thay đổi
  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    
    const currentPage = searchParams.get('page') ? parseInt(searchParams.get('page')) : 1;
    const currentSort = searchParams.get('sort') || 'newest';
    const currentCategory = searchParams.get('category') || '';
    const currentSearch = searchParams.get('search') || '';
    
    // Price range format: min-max
    const priceParam = searchParams.get('price');
    const currentPrice = priceParam 
      ? priceParam.split('-').map(p => parseInt(p)) 
      : [0, 50000000];
    
    // Brands format: comma separated values
    const brandsParam = searchParams.get('brands');
    const currentBrands = brandsParam ? brandsParam.split(',') : [];
    
    const currentRating = searchParams.get('rating') 
      ? parseInt(searchParams.get('rating')) 
      : 0;
    
    const currentType = searchParams.get('type') || '';
    
    // Cập nhật state từ URL
    setPage(currentPage);
    setSort(currentSort);
    setSearchQuery(currentSearch);
    setProductType(currentType);
    setFilters({
      category: currentCategory,
      price: currentPrice,
      brand: currentBrands,
      rating: currentRating,
      search: currentSearch,
      product_type: currentType
    });
    
    // Fetch products dựa vào URL parameters
    fetchProducts(currentPage, currentSort, {
      category: currentCategory,
      price: currentPrice,
      brand: currentBrands,
      rating: currentRating,
      search: currentSearch,
      product_type: currentType
    });
  }, [location.search, fetchProducts]);

  // Xử lý thay đổi filter
  const handleFilterChange = useCallback((name, value) => {
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  }, []);

  // Xử lý thay đổi sort
  const handleSortChange = useCallback((event) => {
    const newSort = event.target.value;
    setSort(newSort);
    
    // Sẽ không cập nhật URL ngay, cần gọi applyFilters để áp dụng
  }, []);

  // Xử lý thay đổi loại sản phẩm
  const handleProductTypeChange = useCallback((event) => {
    const newType = event.target.value;
    setProductType(newType);
    
    // Cập nhật URL và reset về trang 1
    updateUrlFromState(1, sort, {
      ...filters,
      product_type: newType
    }, searchQuery, newType);
  }, [filters, sort, searchQuery, updateUrlFromState]);

  // Xử lý tìm kiếm
  const handleSearch = useCallback((query) => {
    setSearchQuery(query);
    
    // Cập nhật URL và reset về trang 1
    updateUrlFromState(1, sort, {
      ...filters,
      search: query
    }, query, productType);
  }, [filters, sort, productType, updateUrlFromState]);

  // Áp dụng filters
  const applyFilters = useCallback(() => {
    // Cập nhật URL với filters
    updateUrlFromState(page, sort, filters, searchQuery, productType);
  }, [page, sort, filters, searchQuery, productType, updateUrlFromState]);

  // Reset filters
  const resetFilters = useCallback(() => {
    const defaultFilters = {
      category: '',
      price: [0, 50000000],
      brand: [],
      rating: 0
    };
    
    setFilters(defaultFilters);
    setProductType('');
    setSort('newest');
    setSearchQuery('');
    setPage(1);
    
    // Reset URL
    navigate(location.pathname);
  }, [navigate, location.pathname]);

  // Xử lý thay đổi trang
  const handlePageChange = useCallback((newPage) => {
    setPage(newPage);
    
    // Cập nhật URL
    updateUrlFromState(newPage, sort, filters, searchQuery, productType);
    
    // Scroll to top
    window.scrollTo(0, 0);
  }, [sort, filters, searchQuery, productType, updateUrlFromState]);

  // Memoize các giá trị trả về
  const memoizedValues = useMemo(() => ({
    loading,
    products,
    totalPages,
    page,
    sort,
    filters,
    searchQuery,
    error,
    productType,
    categories,
    brands,
    categoriesLoading,
    brandsLoading,
    handleFilterChange,
    handleSortChange,
    handleProductTypeChange,
    handleSearch,
    applyFilters,
    resetFilters,
    handlePageChange,
    fetchProducts,
    fetchCategories,
    fetchBrands
  }), [
    loading, products, totalPages, page, sort, filters, 
    searchQuery, error, productType, categories, brands,
    categoriesLoading, brandsLoading, 
    handleFilterChange, handleSortChange, handleProductTypeChange,
    handleSearch, applyFilters, resetFilters, handlePageChange,
    fetchProducts, fetchCategories, fetchBrands
  ]);

  return memoizedValues;
}; 