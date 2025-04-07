import React, { memo } from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText
} from '@mui/material';

const BookDescription = memo(({ product }) => {
  if (!product.details) {
    console.warn('Không có chi tiết sách:', product);
    return (
      <Box>
        <Typography variant="body1">Không tìm thấy thông tin mô tả chi tiết cho sách này.</Typography>
      </Box>
    );
  }
  
  const { details } = product;
  console.log('Chi tiết sách:', details);
  
  // Xử lý dữ liệu mảng dạng chuỗi
  const parseArrayField = (field) => {
    if (!field) return [];
    if (Array.isArray(field)) return field;
    
    try {
      // Nếu field là chuỗi dạng "['item1', 'item2']"
      if (typeof field === 'string' && field.startsWith('[') && field.endsWith(']')) {
        return JSON.parse(field.replace(/'/g, '"'));
      }
    } catch (error) {
      console.error("Error parsing array field:", error);
      console.log("Field value:", field);
    }
    
    return [field]; // Trả về mảng có một phần tử nếu không phải mảng
  };
  
  // Sử dụng try-catch để tránh lỗi khi xử lý dữ liệu
  try {
    const tableOfContents = parseArrayField(details.table_of_contents || []);
    const authors = parseArrayField(details.authors || []);
    
    return (
      <Box>
        {authors.length > 0 && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>Tác giả</Typography>
            <Typography variant="body1">
              {authors.join(', ')}
            </Typography>
          </Box>
        )}
      
        {details.summary && (
          <>
            <Typography variant="h6" gutterBottom>Tóm tắt</Typography>
            <Typography variant="body1" paragraph>
              {details.summary}
            </Typography>
          </>
        )}
        
        {tableOfContents.length > 0 && (
          <>
            <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>Mục lục</Typography>
            <List dense>
              {tableOfContents.map((item, index) => (
                <ListItem key={index}>
                  <ListItemText primary={item} />
                </ListItem>
              ))}
            </List>
          </>
        )}
      </Box>
    );
  } catch (error) {
    console.error('Lỗi khi hiển thị chi tiết sách:', error);
    return (
      <Box>
        <Typography variant="body1">
          {product.description || "Đã xảy ra lỗi khi hiển thị thông tin chi tiết sách. Vui lòng thử lại sau."}
        </Typography>
      </Box>
    );
  }
});

const ShoeDescription = memo(({ product }) => {
  if (!product.details) return null;
  
  const { details } = product;
  
  return (
    <Box>
      <Typography variant="h6" gutterBottom>Thông tin sản phẩm</Typography>
      <Typography variant="body1" paragraph>
        {product.name} là sản phẩm giày của {product.brand || 'thương hiệu nổi tiếng'}, 
        được thiết kế đặc biệt cho các hoạt động {details?.sport_type?.toLowerCase() || 'thể thao'}.
      </Typography>
      
      <Typography variant="body1" paragraph sx={{ mt: 2 }}>
        Với chất liệu {details.material || 'cao cấp'}, 
        đôi giày mang lại cảm giác thoải mái và bền bỉ suốt thời gian sử dụng.
        {details.waterproof ? ' Đặc biệt, sản phẩm có khả năng chống nước giúp bảo vệ đôi chân trong mọi điều kiện thời tiết.' : ''}
      </Typography>
      
      <Typography variant="body1" paragraph>
        {details.breathability === 'High' ? 'Độ thoáng khí cao giúp chân luôn khô thoáng trong suốt quá trình sử dụng.' : ''}
        {details.recommended_terrain ? ` Đây là sản phẩm lý tưởng cho địa hình ${details.recommended_terrain}.` : ''}
      </Typography>
      
      <Typography variant="body1" paragraph>
        {product.brand} cam kết mang đến cho khách hàng sản phẩm chất lượng với 
        {details?.warranty_period ? ` thời gian bảo hành lên đến ${details.warranty_period} tháng.` : ' chế độ bảo hành tốt nhất.'}
      </Typography>
    </Box>
  );
});

const GenericDescription = memo(({ product }) => {
  return (
    <Box>
      <Typography variant="body1">
        {product.description || "Không có thông tin mô tả chi tiết"}
      </Typography>
    </Box>
  );
});

const ProductDescription = ({ product }) => {
  if (!product) return null;

  // Hiển thị mô tả sản phẩm tùy theo loại
  switch (product.product_type) {
    case 'BOOK':
      return <BookDescription product={product} />;
    case 'SHOE':
      return <ShoeDescription product={product} />;
    default:
      return <GenericDescription product={product} />;
  }
};

export default memo(ProductDescription); 