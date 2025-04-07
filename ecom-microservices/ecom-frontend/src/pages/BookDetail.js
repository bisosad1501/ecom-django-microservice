import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  Box,
  Button,
  TextField,
  Rating,
  Divider,
  Breadcrumbs,
  Paper,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  Snackbar,
  Card,
  CardMedia,
  CardContent,
  Chip
} from '@mui/material';
import {
  ShoppingCart as CartIcon,
  Favorite as FavoriteIcon,
  FavoriteBorder as FavoriteBorderIcon
} from '@mui/icons-material';
import { bookService, cartService, reviewService, recommendationService } from '../services/api';

const BookDetail = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [tabValue, setTabValue] = useState(0);
  const [reviews, setReviews] = useState([]);
  const [similarBooks, setSimilarBooks] = useState([]);
  const [inWishlist, setInWishlist] = useState(false);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  useEffect(() => {
    const fetchBookDetails = async () => {
      setLoading(true);
      try {
        // Fetch book details
        const bookResponse = await bookService.getBookById(id);
        setBook(bookResponse.data);
        
        // Fetch reviews
        try {
          const reviewsResponse = await reviewService.getReviews(id);
          setReviews(reviewsResponse.data.results || reviewsResponse.data || []);
        } catch (error) {
          console.error('Lỗi khi lấy đánh giá:', error);
        }
        
        // Fetch similar books
        try {
          const similarResponse = await recommendationService.getSimilarProducts(id);
          setSimilarBooks(similarResponse.data.results || similarResponse.data || []);
        } catch (error) {
          console.error('Lỗi khi lấy sách tương tự:', error);
          // Fallback - fetch some books
          const booksResponse = await bookService.getBooks({ limit: 4 });
          setSimilarBooks(booksResponse.data.results || booksResponse.data || []);
        }
        
        // Check if book is in wishlist
        const wishlist = localStorage.getItem('wishlist');
        if (wishlist) {
          const wishlistItems = JSON.parse(wishlist);
          setInWishlist(wishlistItems.includes(id));
        }
      } catch (error) {
        console.error('Lỗi khi lấy thông tin sách:', error);
        setError('Không thể tải thông tin sách. Vui lòng thử lại sau.');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchBookDetails();
    }
  }, [id]);

  const handleQuantityChange = (e) => {
    const value = parseInt(e.target.value);
    if (value > 0) {
      setQuantity(value);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleAddToCart = async () => {
    try {
      await cartService.addToCart({
        product_id: id,
        quantity: quantity,
        product_type: 'book'
      });
      
      setSnackbar({
        open: true,
        message: 'Đã thêm sách vào giỏ hàng',
        severity: 'success'
      });
    } catch (error) {
      console.error('Lỗi khi thêm vào giỏ hàng:', error);
      setSnackbar({
        open: true,
        message: 'Không thể thêm vào giỏ hàng. Vui lòng thử lại sau.',
        severity: 'error'
      });
    }
  };

  const handleToggleWishlist = () => {
    try {
      const wishlist = localStorage.getItem('wishlist');
      let wishlistItems = wishlist ? JSON.parse(wishlist) : [];
      
      if (inWishlist) {
        // Remove from wishlist
        wishlistItems = wishlistItems.filter(item => item !== id);
        setSnackbar({
          open: true,
          message: 'Đã xóa khỏi danh sách yêu thích',
          severity: 'info'
        });
      } else {
        // Add to wishlist
        if (!wishlistItems.includes(id)) {
          wishlistItems.push(id);
        }
        setSnackbar({
          open: true,
          message: 'Đã thêm vào danh sách yêu thích',
          severity: 'success'
        });
      }
      
      localStorage.setItem('wishlist', JSON.stringify(wishlistItems));
      setInWishlist(!inWishlist);
    } catch (error) {
      console.error('Lỗi khi cập nhật danh sách yêu thích:', error);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const calculateAverageRating = (reviews) => {
    if (!reviews || reviews.length === 0) return 0;
    const sum = reviews.reduce((acc, review) => acc + (review.rating || 0), 0);
    return sum / reviews.length;
  };

  // Dummy book data in case API call fails
  const dummyBook = {
    id: id,
    title: 'Đắc Nhân Tâm',
    author: 'Dale Carnegie',
    publisher: 'NXB Tổng hợp TP.HCM',
    published_year: '2018',
    isbn: '9786048949648',
    price: 88000,
    sale_price: 75000,
    cover_image: 'https://via.placeholder.com/500x700',
    description: 'Đắc nhân tâm là quyển sách nổi tiếng nhất, bán chạy nhất và có tầm ảnh hưởng nhất của mọi thời đại do Dale Carnegie viết. Tác phẩm được xuất bản năm 1936, ngay lập tức trở thành một hiện tượng văn hóa và nằm trong danh mục sách bán chạy nhất suốt 10 năm liền.',
    pages: 320,
    category: 'Kỹ năng sống',
    language: 'Tiếng Việt',
    in_stock: 50,
    format: 'Bìa mềm'
  };

  const bookData = book || dummyBook;

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', my: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 3 }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          Trang chủ
        </Link>
        <Link to="/books" style={{ textDecoration: 'none', color: 'inherit' }}>
          Sách
        </Link>
        <Typography color="text.primary">{bookData.title}</Typography>
      </Breadcrumbs>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {/* Main content */}
      <Grid container spacing={4}>
        {/* Book image */}
        <Grid item xs={12} md={4}>
          <Box sx={{ position: 'relative' }}>
            <img
              src={bookData.cover_image}
              alt={bookData.title}
              style={{ width: '100%', borderRadius: 8 }}
            />
            {bookData.sale_price && bookData.sale_price < bookData.price && (
              <Chip
                label={`Giảm ${Math.round((1 - bookData.sale_price / bookData.price) * 100)}%`}
                color="error"
                size="small"
                sx={{
                  position: 'absolute',
                  top: 16,
                  left: 16,
                }}
              />
            )}
          </Box>
        </Grid>
        
        {/* Book details */}
        <Grid item xs={12} md={8}>
          <Typography variant="h4" component="h1" gutterBottom>
            {bookData.title}
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Typography variant="subtitle1" sx={{ mr: 1 }}>
              Tác giả:
            </Typography>
            <Typography variant="subtitle1" color="primary">
              {bookData.author}
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Rating
              value={calculateAverageRating(reviews)}
              precision={0.5}
              readOnly
              sx={{ mr: 1 }}
            />
            <Typography variant="body2" color="text.secondary">
              ({reviews.length} đánh giá)
            </Typography>
          </Box>
          
          <Box sx={{ mb: 3 }}>
            {bookData.sale_price && bookData.sale_price < bookData.price ? (
              <>
                <Typography
                  variant="h5"
                  component="span"
                  color="error"
                  sx={{ fontWeight: 'bold', mr: 2 }}
                >
                  {bookData.sale_price.toLocaleString()} VNĐ
                </Typography>
                <Typography
                  variant="h6"
                  component="span"
                  color="text.secondary"
                  sx={{ textDecoration: 'line-through' }}
                >
                  {bookData.price.toLocaleString()} VNĐ
                </Typography>
              </>
            ) : (
              <Typography
                variant="h5"
                component="span"
                sx={{ fontWeight: 'bold' }}
              >
                {bookData.price.toLocaleString()} VNĐ
              </Typography>
            )}
          </Box>
          
          <Box sx={{ mb: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={3}>
                <TextField
                  type="number"
                  label="Số lượng"
                  value={quantity}
                  onChange={handleQuantityChange}
                  InputProps={{ inputProps: { min: 1, max: bookData.in_stock || 100 } }}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} sm={9}>
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <Button
                    variant="contained"
                    startIcon={<CartIcon />}
                    onClick={handleAddToCart}
                    sx={{ flex: 1 }}
                  >
                    Thêm vào giỏ
                  </Button>
                  <Button
                    variant={inWishlist ? "outlined" : "text"}
                    color={inWishlist ? "secondary" : "primary"}
                    onClick={handleToggleWishlist}
                    startIcon={inWishlist ? <FavoriteIcon /> : <FavoriteBorderIcon />}
                  >
                    {inWishlist ? 'Đã yêu thích' : 'Thêm vào yêu thích'}
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </Box>
          
          {/* Book info table */}
          <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2">
                  <strong>Nhà xuất bản:</strong> {bookData.publisher}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2">
                  <strong>Năm xuất bản:</strong> {bookData.published_year}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2">
                  <strong>Số trang:</strong> {bookData.pages}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2">
                  <strong>Ngôn ngữ:</strong> {bookData.language}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2">
                  <strong>Định dạng:</strong> {bookData.format}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2">
                  <strong>ISBN:</strong> {bookData.isbn}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
      
      {/* Tabs section */}
      <Box sx={{ mt: 6, mb: 4 }}>
        <Paper>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            variant="fullWidth"
            indicatorColor="primary"
            textColor="primary"
          >
            <Tab label="Mô tả" />
            <Tab label="Đánh giá" />
          </Tabs>
          
          {/* Description tab */}
          {tabValue === 0 && (
            <Box sx={{ p: 3 }}>
              <Typography variant="body1" paragraph>
                {bookData.description}
              </Typography>
            </Box>
          )}
          
          {/* Reviews tab */}
          {tabValue === 1 && (
            <Box sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Đánh giá từ người đọc
              </Typography>
              
              {reviews.length > 0 ? (
                reviews.map((review, index) => (
                  <Box key={review.id || index} sx={{ mb: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="subtitle1">
                        {review.user_name || 'Người dùng ẩn danh'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(review.created_at).toLocaleDateString('vi-VN')}
                      </Typography>
                    </Box>
                    <Rating value={review.rating} readOnly size="small" sx={{ mb: 1 }} />
                    <Typography variant="body1">
                      {review.comment}
                    </Typography>
                    {index < reviews.length - 1 && <Divider sx={{ mt: 2 }} />}
                  </Box>
                ))
              ) : (
                <Typography variant="body1" color="text.secondary">
                  Chưa có đánh giá nào. Hãy là người đầu tiên đánh giá sách này.
                </Typography>
              )}
            </Box>
          )}
        </Paper>
      </Box>
      
      {/* Similar books */}
      {similarBooks.length > 0 && (
        <Box sx={{ mt: 6 }}>
          <Typography variant="h5" gutterBottom>
            Sách tương tự
          </Typography>
          <Grid container spacing={3}>
            {similarBooks.slice(0, 4).map((book) => (
              <Grid item xs={6} sm={3} key={book.id}>
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <CardMedia
                    component="img"
                    height="200"
                    image={book.cover_image || 'https://via.placeholder.com/150'}
                    alt={book.title}
                  />
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography variant="subtitle1" component="div" noWrap>
                      {book.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" noWrap>
                      {book.author}
                    </Typography>
                    <Typography variant="body2" color="primary.main" sx={{ fontWeight: 'bold', mt: 1 }}>
                      {book.sale_price || book.price} VNĐ
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
      
      {/* Snackbar notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default BookDetail; 