import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Typography,
  Button,
  Box,
  CircularProgress,
  Rating,
  Pagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { shoeService } from '../services/api';

const ShoeList = () => {
  const navigate = useNavigate();
  const [shoes, setShoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [sortBy, setSortBy] = useState('newest');
  const [category, setCategory] = useState('all');

  useEffect(() => {
    fetchShoes();
  }, [page, sortBy, category]);

  const fetchShoes = async () => {
    try {
      setLoading(true);
      const response = await shoeService.getShoes({
        page,
        sort: sortBy,
        category: category !== 'all' ? category : undefined,
      });
      setShoes(response.data.items);
      setTotalPages(Math.ceil(response.data.total / response.data.per_page));
    } catch (err) {
      setError('Không thể tải danh sách giày');
      console.error('Error fetching shoes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (event, value) => {
    setPage(value);
    window.scrollTo(0, 0);
  };

  const handleSortChange = (event) => {
    setSortBy(event.target.value);
    setPage(1);
  };

  const handleCategoryChange = (event) => {
    setCategory(event.target.value);
    setPage(1);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box mb={4}>
        <Typography variant="h4" gutterBottom>
          Danh sách giày
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={4}>
            <FormControl fullWidth>
              <InputLabel>Sắp xếp theo</InputLabel>
              <Select value={sortBy} onChange={handleSortChange}>
                <MenuItem value="newest">Mới nhất</MenuItem>
                <MenuItem value="price_asc">Giá tăng dần</MenuItem>
                <MenuItem value="price_desc">Giá giảm dần</MenuItem>
                <MenuItem value="rating">Đánh giá cao</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <FormControl fullWidth>
              <InputLabel>Danh mục</InputLabel>
              <Select value={category} onChange={handleCategoryChange}>
                <MenuItem value="all">Tất cả</MenuItem>
                <MenuItem value="sneaker">Sneaker</MenuItem>
                <MenuItem value="boots">Boots</MenuItem>
                <MenuItem value="sandals">Sandals</MenuItem>
                <MenuItem value="formal">Giày tây</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Box>

      <Grid container spacing={3}>
        {shoes.map((shoe) => (
          <Grid item key={shoe.id} xs={12} sm={6} md={4} lg={3}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                '&:hover': {
                  transform: 'scale(1.02)',
                  transition: 'transform 0.2s ease-in-out',
                },
              }}
            >
              <CardMedia
                component="img"
                height="200"
                image={shoe.image_url || '/placeholder.png'}
                alt={shoe.name}
                sx={{ objectFit: 'contain', p: 2 }}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h6" component="h2" noWrap>
                  {shoe.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {shoe.brand}
                </Typography>
                <Box display="flex" alignItems="center" mb={1}>
                  <Rating value={shoe.rating || 0} readOnly precision={0.5} size="small" />
                  <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                    ({shoe.review_count || 0})
                  </Typography>
                </Box>
                <Typography variant="h6" color="primary">
                  {new Intl.NumberFormat('vi-VN', {
                    style: 'currency',
                    currency: 'VND',
                  }).format(shoe.price)}
                </Typography>
                <Button
                  variant="contained"
                  fullWidth
                  sx={{ mt: 2 }}
                  onClick={() => navigate(`/shoes/${shoe.id}`)}
                >
                  Xem chi tiết
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {totalPages > 1 && (
        <Box display="flex" justifyContent="center" mt={4}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={handlePageChange}
            color="primary"
            size="large"
          />
        </Box>
      )}
    </Container>
  );
};

export default ShoeList; 