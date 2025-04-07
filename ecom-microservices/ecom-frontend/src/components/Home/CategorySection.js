import React, { memo } from 'react';
import { Link } from 'react-router-dom';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardMedia,
  CardContent,
  Button,
  Chip,
  useTheme
} from '@mui/material';
import { ChevronRight as ArrowRightIcon } from '@mui/icons-material';

/**
 * Component hiển thị danh mục sản phẩm cho trang chủ
 * @param {Object} props
 * @param {Array} props.categories - Danh sách các danh mục
 * @param {boolean} props.loading - Trạng thái loading
 */
const CategorySection = ({ categories = [], loading = false }) => {
  const theme = useTheme();

  return (
    <Box sx={{ mb: 6 }}>
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        mb: 3,
        borderBottom: `1px solid ${theme.palette.divider}`,
        pb: 1
      }}>
        <Typography variant="h5" component="h2" fontWeight="bold">
          Danh mục sản phẩm
        </Typography>
        <Button
          endIcon={<ArrowRightIcon />}
          component={Link}
          to="/categories"
        >
          Xem tất cả
        </Button>
      </Box>
      
      <Grid container spacing={2}>
        {categories.map((category) => (
          <Grid item xs={6} sm={4} md={4} lg={2} key={category.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-5px)',
                  boxShadow: 6
                },
                containIntrinsicSize: '0 200px',
                contentVisibility: 'auto'
              }}
            >
              <CardMedia
                sx={{ height: 140, cursor: 'pointer' }}
                image={
                  category.image || 
                  `/images/category-${category.id}.jpg` || 
                  '/images/category-placeholder.jpg'
                }
                title={category.name}
                component={Link}
                to={`/products?category=${category.id}&type=${category.product_type || ''}`}
                loading="lazy"
              />
              <CardContent>
                <Typography 
                  variant="h6" 
                  component={Link} 
                  to={`/products?category=${category.id}&type=${category.product_type || ''}`}
                  sx={{ 
                    fontWeight: 'bold', 
                    mb: 1, 
                    textDecoration: 'none',
                    color: 'inherit',
                    '&:hover': { color: 'primary.main' }
                  }}
                >
                  {category.name}
                </Typography>
                
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">
                    {category.count} sản phẩm
                  </Typography>
                  {category.subcategories && category.subcategories.length > 0 && (
                    <Typography variant="body2" color="primary">
                      {category.subcategories.length} danh mục con
                    </Typography>
                  )}
                </Box>
                
                {/* Hiển thị danh mục con nếu có */}
                {category.subcategories && category.subcategories.length > 0 && (
                  <Box sx={{ mt: 1 }}>
                    {category.subcategories.slice(0, 2).map((sub) => (
                      <Box 
                        key={sub.id} 
                        component="span" 
                        sx={{ display: 'inline-block', mr: 0.5, mt: 0.5 }}
                      >
                        <Chip
                          label={sub.name}
                          size="small"
                          sx={{ maxWidth: '100%', overflow: 'hidden' }}
                          component={Link}
                          to={`/products?parent_category=${category.id}&subcategory=${sub.id}&type=${category.product_type || ''}`}
                          clickable
                        />
                      </Box>
                    ))}
                    {category.subcategories.length > 2 && (
                      <Chip
                        label={`+${category.subcategories.length - 2}`}
                        size="small"
                        color="primary"
                        variant="outlined"
                        sx={{ mt: 0.5 }}
                        onClick={() => 
                          window.location.href = `/products?category=${category.id}&type=${category.product_type || ''}`
                        }
                      />
                    )}
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default memo(CategorySection); 