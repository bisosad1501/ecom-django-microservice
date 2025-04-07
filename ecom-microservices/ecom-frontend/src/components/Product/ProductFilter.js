import React from 'react';
import {
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Divider,
  Checkbox,
  FormControlLabel,
  FormGroup,
  Button,
  Rating,
  IconButton
} from '@mui/material';
import FilterListIcon from '@mui/icons-material/FilterList';
import ClearIcon from '@mui/icons-material/Clear';
import './ProductFilter.css';

const PRODUCT_TYPES = [
  { value: 'BOOK', label: 'Sách' },
  { value: 'SHOE', label: 'Giày' },
  { value: 'ELECTRONIC', label: 'Điện tử' },
  { value: 'CLOTHING', label: 'Quần áo' },
  { value: 'HOME_APPLIANCE', label: 'Đồ gia dụng' },
  { value: 'FURNITURE', label: 'Nội thất' },
  { value: 'BEAUTY', label: 'Mỹ phẩm' },
  { value: 'FOOD', label: 'Thực phẩm' },
  { value: 'SPORTS', label: 'Đồ thể thao' },
  { value: 'TOYS', label: 'Đồ chơi' }
];

const ProductFilter = ({
  categories = [],
  brands = [],
  filters,
  onFilterChange,
  onApplyFilters,
  onResetFilters,
  productType,
  onProductTypeChange,
  sort,
  onSortChange,
  isMobile = false
}) => {
  const handleFilterChange = (name, value) => {
    onFilterChange(name, value);
  };

  return (
    <Box className={`product-filter ${isMobile ? 'mobile' : ''}`}>
      <Box className="filter-header">
        <Typography variant="h6" className="filter-title">
          <FilterListIcon /> Bộ lọc
        </Typography>
        <IconButton 
          size="small" 
          onClick={onResetFilters} 
          title="Xóa bộ lọc"
          className="reset-button"
        >
          <ClearIcon />
        </IconButton>
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Loại sản phẩm */}
      <Box className="filter-section">
        <Typography variant="subtitle1" gutterBottom>
          Loại sản phẩm
        </Typography>
        <FormControl fullWidth size="small">
          <InputLabel id="product-type-label">Chọn loại</InputLabel>
          <Select
            labelId="product-type-label"
            id="product-type"
            value={productType}
            onChange={onProductTypeChange}
            label="Chọn loại"
          >
            <MenuItem value="">Tất cả</MenuItem>
            {PRODUCT_TYPES.map((type) => (
              <MenuItem key={type.value} value={type.value}>
                {type.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Sắp xếp */}
      <Box className="filter-section">
        <Typography variant="subtitle1" gutterBottom>
          Sắp xếp theo
        </Typography>
        <FormControl fullWidth size="small">
          <InputLabel id="sort-label">Sắp xếp</InputLabel>
          <Select
            labelId="sort-label"
            id="sort"
            value={sort}
            onChange={onSortChange}
            label="Sắp xếp"
          >
            <MenuItem value="newest">Mới nhất</MenuItem>
            <MenuItem value="price-asc">Giá tăng dần</MenuItem>
            <MenuItem value="price-desc">Giá giảm dần</MenuItem>
            <MenuItem value="popular">Phổ biến nhất</MenuItem>
            <MenuItem value="rating">Đánh giá cao</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Danh mục */}
      <Box className="filter-section">
        <Typography variant="subtitle1" gutterBottom>
          Danh mục
        </Typography>
        <FormControl fullWidth size="small">
          <InputLabel id="category-label">Danh mục</InputLabel>
          <Select
            labelId="category-label"
            id="category"
            value={filters.category}
            onChange={(e) => handleFilterChange('category', e.target.value)}
            label="Danh mục"
          >
            <MenuItem value="">Tất cả</MenuItem>
            {categories.map((category) => (
              <MenuItem key={category.id} value={category.id.toString()}>
                {category.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Khoảng giá */}
      <Box className="filter-section">
        <Typography variant="subtitle1" gutterBottom>
          Khoảng giá
        </Typography>
        <Typography variant="body2" gutterBottom>
          {filters.price[0].toLocaleString('vi-VN')}₫ - {filters.price[1].toLocaleString('vi-VN')}₫
        </Typography>
        <Slider
          value={filters.price}
          onChange={(e, newValue) => handleFilterChange('price', newValue)}
          valueLabelDisplay="auto"
          min={0}
          max={50000000}
          step={100000}
          valueLabelFormat={(value) => `${value.toLocaleString('vi-VN')}₫`}
        />
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Thương hiệu */}
      {brands.length > 0 && (
        <Box className="filter-section brands-filter">
          <Typography variant="subtitle1" gutterBottom>
            Thương hiệu
          </Typography>
          <FormGroup>
            {brands.map((brand) => (
              <FormControlLabel
                key={brand.id}
                control={
                  <Checkbox
                    checked={filters.brand.includes(brand.id.toString())}
                    onChange={(e) => {
                      const newBrands = e.target.checked
                        ? [...filters.brand, brand.id.toString()]
                        : filters.brand.filter((id) => id !== brand.id.toString());
                      handleFilterChange('brand', newBrands);
                    }}
                    size="small"
                  />
                }
                label={brand.name}
              />
            ))}
          </FormGroup>
        </Box>
      )}

      <Divider sx={{ my: 2 }} />

      {/* Đánh giá */}
      <Box className="filter-section">
        <Typography variant="subtitle1" gutterBottom>
          Đánh giá
        </Typography>
        <Box display="flex" alignItems="center">
          <Rating
            name="rating-filter"
            value={filters.rating}
            onChange={(e, newValue) => handleFilterChange('rating', newValue)}
            precision={1}
          />
          <Typography variant="body2" sx={{ ml: 1 }}>
            {filters.rating > 0 ? `${filters.rating} sao trở lên` : 'Tất cả đánh giá'}
          </Typography>
        </Box>
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Buttons */}
      <Box className="filter-actions">
        <Button
          variant="contained"
          color="primary"
          onClick={onApplyFilters}
          fullWidth
        >
          Áp dụng bộ lọc
        </Button>
        <Button
          variant="outlined"
          color="secondary"
          onClick={onResetFilters}
          fullWidth
          sx={{ mt: 1 }}
        >
          Đặt lại
        </Button>
      </Box>
    </Box>
  );
};

export default ProductFilter; 