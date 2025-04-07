import React, { memo } from 'react';
import {
  Box,
  Typography,
  TableContainer,
  Table,
  TableBody,
  TableRow,
  TableCell,
  Paper,
  Chip,
  List,
  ListItem,
  ListItemText,
  Button,
  Rating
} from '@mui/material';

// Hàm helper để xử lý dữ liệu an toàn
const safeGet = (obj, path, defaultValue = 'Không có thông tin') => {
  try {
    const keys = path.split('.');
    let result = obj;
    for (const key of keys) {
      if (result === undefined || result === null) return defaultValue;
      result = result[key];
    }
    return result === undefined || result === null ? defaultValue : result;
  } catch (e) {
    console.error(`Lỗi khi truy cập ${path}:`, e);
    return defaultValue;
  }
};

// Hàm parse mảng an toàn
const safeParseArray = (field, defaultValue = []) => {
  if (!field) return defaultValue;
  if (Array.isArray(field)) return field;
  
  try {
    // Nếu field là chuỗi dạng "['item1', 'item2']"
    if (typeof field === 'string' && field.startsWith('[') && field.endsWith(']')) {
      return JSON.parse(field.replace(/'/g, '"'));
    }
  } catch (error) {
    console.error("Lỗi khi parse mảng:", error, field);
  }
  
  return [field]; // Trả về mảng có một phần tử nếu không phải mảng
};

// Book details component
const BookDetails = memo(({ product }) => {
  if (!product || !product.details) {
    console.warn("Không có thông tin chi tiết sách:", product);
    return (
      <Typography variant="body1" sx={{ p: 2 }}>
        Không có thông tin chi tiết cho sản phẩm này.
      </Typography>
    );
  }
  
  console.log("Chi tiết sách trong BookDetails:", product.details);
  
  try {
    const { details } = product;
    const authors = safeParseArray(details.authors);
    
    return (
      <TableContainer component={Paper} sx={{ mb: 4, boxShadow: 0, border: '1px solid #eee' }}>
        <Table>
          <TableBody>
            <TableRow>
              <TableCell component="th" width="30%">Tác giả</TableCell>
              <TableCell>{authors.join(', ') || 'Không rõ'}</TableCell>
            </TableRow>
            {details.translator && (
              <TableRow>
                <TableCell component="th">Dịch giả</TableCell>
                <TableCell>{safeGet(details, 'translator')}</TableCell>
              </TableRow>
            )}
            <TableRow>
              <TableCell component="th">Nhà xuất bản</TableCell>
              <TableCell>{safeGet(details, 'publisher')}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell component="th">Ngày xuất bản</TableCell>
              <TableCell>{safeGet(details, 'publication_date')}</TableCell>
            </TableRow>
            {details.edition && (
              <TableRow>
                <TableCell component="th">Phiên bản</TableCell>
                <TableCell>{safeGet(details, 'edition')}</TableCell>
              </TableRow>
            )}
            {details.series && (
              <TableRow>
                <TableCell component="th">Series</TableCell>
                <TableCell>{safeGet(details, 'series')}</TableCell>
              </TableRow>
            )}
            <TableRow>
              <TableCell component="th">Ngôn ngữ</TableCell>
              <TableCell>{safeGet(details, 'language')}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell component="th">Định dạng</TableCell>
              <TableCell>{safeGet(details, 'book_format')}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell component="th">ISBN-13</TableCell>
              <TableCell>{safeGet(details, 'isbn_13')}</TableCell>
            </TableRow>
            {details.reading_age && (
              <TableRow>
                <TableCell component="th">Độ tuổi phù hợp</TableCell>
                <TableCell>{safeGet(details, 'reading_age')}</TableCell>
              </TableRow>
            )}
            <TableRow>
              <TableCell component="th">Số trang</TableCell>
              <TableCell>{safeGet(details, 'page_count')}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    );
  } catch (error) {
    console.error("Lỗi khi render chi tiết sách:", error);
    return (
      <Typography variant="body1" color="error" sx={{ p: 2 }}>
        Đã xảy ra lỗi khi hiển thị thông tin chi tiết. Vui lòng thử lại sau.
      </Typography>
    );
  }
});

// Shoe details component
const ShoeDetails = memo(({ product }) => {
  const shoeDetails = product.details;
  if (!shoeDetails) return null;
  
  return (
    <TableContainer component={Paper} sx={{ mt: 3, mb: 3 }}>
      <Table>
        <TableBody>
          {shoeDetails.size && (
            <TableRow>
              <TableCell component="th" variant="head" width="30%">Kích thước</TableCell>
              <TableCell>{shoeDetails.size}</TableCell>
            </TableRow>
          )}
          {shoeDetails.color && (
            <TableRow>
              <TableCell component="th" variant="head">Màu sắc</TableCell>
              <TableCell>{shoeDetails.color}</TableCell>
            </TableRow>
          )}
          {shoeDetails.material && (
            <TableRow>
              <TableCell component="th" variant="head">Chất liệu</TableCell>
              <TableCell>{shoeDetails.material}</TableCell>
            </TableRow>
          )}
          {shoeDetails.gender && (
            <TableRow>
              <TableCell component="th" variant="head">Giới tính</TableCell>
              <TableCell>
                {shoeDetails.gender === 'M' ? 'Nam' : 
                 shoeDetails.gender === 'F' ? 'Nữ' : 
                 shoeDetails.gender === 'U' ? 'Unisex' : shoeDetails.gender}
              </TableCell>
            </TableRow>
          )}
          {shoeDetails.sport_type && (
            <TableRow>
              <TableCell component="th" variant="head">Loại thể thao</TableCell>
              <TableCell>{shoeDetails.sport_type}</TableCell>
            </TableRow>
          )}
          {shoeDetails.style && (
            <TableRow>
              <TableCell component="th" variant="head">Phong cách</TableCell>
              <TableCell>{shoeDetails.style}</TableCell>
            </TableRow>
          )}
          {shoeDetails.closure_type && (
            <TableRow>
              <TableCell component="th" variant="head">Kiểu đóng</TableCell>
              <TableCell>{shoeDetails.closure_type}</TableCell>
            </TableRow>
          )}
          {shoeDetails.sole_material && (
            <TableRow>
              <TableCell component="th" variant="head">Chất liệu đế</TableCell>
              <TableCell>{shoeDetails.sole_material}</TableCell>
            </TableRow>
          )}
          {shoeDetails.upper_material && (
            <TableRow>
              <TableCell component="th" variant="head">Chất liệu thân</TableCell>
              <TableCell>{shoeDetails.upper_material}</TableCell>
            </TableRow>
          )}
          {shoeDetails.waterproof !== undefined && (
            <TableRow>
              <TableCell component="th" variant="head">Chống nước</TableCell>
              <TableCell>{shoeDetails.waterproof ? 'Có' : 'Không'}</TableCell>
            </TableRow>
          )}
          {shoeDetails.breathability && (
            <TableRow>
              <TableCell component="th" variant="head">Độ thoáng khí</TableCell>
              <TableCell>{shoeDetails.breathability}</TableCell>
            </TableRow>
          )}
          {shoeDetails.recommended_terrain && (
            <TableRow>
              <TableCell component="th" variant="head">Địa hình phù hợp</TableCell>
              <TableCell>{shoeDetails.recommended_terrain}</TableCell>
            </TableRow>
          )}
          {shoeDetails.warranty_period && (
            <TableRow>
              <TableCell component="th" variant="head">Thời hạn bảo hành</TableCell>
              <TableCell>{shoeDetails.warranty_period} tháng</TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
});

// Common details component
const CommonDetails = memo(({ product }) => (
  <TableContainer component={Paper} sx={{ mt: 3, mb: 3 }}>
    <Table>
      <TableBody>
        <TableRow>
          <TableCell component="th" variant="head" width="30%">ID sản phẩm</TableCell>
          <TableCell>{product._id}</TableCell>
        </TableRow>
        <TableRow>
          <TableCell component="th" variant="head">Mã sản phẩm (SKU)</TableCell>
          <TableCell>{product.sku}</TableCell>
        </TableRow>
        {product.brand && (
          <TableRow>
            <TableCell component="th" variant="head">Thương hiệu</TableCell>
            <TableCell>{product.brand}</TableCell>
          </TableRow>
        )}
        <TableRow>
          <TableCell component="th" variant="head">Loại sản phẩm</TableCell>
          <TableCell>{product.product_type}</TableCell>
        </TableRow>
        {product.category_path && product.category_path.length > 0 && (
          <TableRow>
            <TableCell component="th" variant="head">Danh mục</TableCell>
            <TableCell>
              {product.category_path.join(' > ')}
            </TableCell>
          </TableRow>
        )}
        <TableRow>
          <TableCell component="th" variant="head">Giá gốc</TableCell>
          <TableCell>{Number(product.base_price).toLocaleString()} VND</TableCell>
        </TableRow>
        {product.sale_price && (
          <TableRow>
            <TableCell component="th" variant="head">Giá bán</TableCell>
            <TableCell>{Number(product.sale_price).toLocaleString()} VND</TableCell>
          </TableRow>
        )}
        <TableRow>
          <TableCell component="th" variant="head">Số lượng trong kho</TableCell>
          <TableCell>{product.quantity}</TableCell>
        </TableRow>
        {product.rating !== undefined && (
          <TableRow>
            <TableCell component="th" variant="head">Đánh giá</TableCell>
            <TableCell>
              <Box display="flex" alignItems="center">
                <Rating value={product.rating} readOnly precision={0.5} size="small" />
                <Typography variant="body2" sx={{ ml: 1 }}>
                  ({product.review_count || 0} đánh giá)
                </Typography>
              </Box>
            </TableCell>
          </TableRow>
        )}
        {product.weight && (
          <TableRow>
            <TableCell component="th" variant="head">Trọng lượng</TableCell>
            <TableCell>{product.weight} kg</TableCell>
          </TableRow>
        )}
        {product.dimensions && Object.keys(product.dimensions).length > 0 && (
          <TableRow>
            <TableCell component="th" variant="head">Kích thước</TableCell>
            <TableCell>
              {product.dimensions.length && product.dimensions.width && product.dimensions.height
                ? `${product.dimensions.length} x ${product.dimensions.width} x ${product.dimensions.height} cm`
                : JSON.stringify(product.dimensions)}
            </TableCell>
          </TableRow>
        )}
        {product.tags && product.tags.length > 0 && (
          <TableRow>
            <TableCell component="th" variant="head">Thẻ</TableCell>
            <TableCell>
              {product.tags.map((tag, index) => (
                <Chip key={index} label={tag} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
              ))}
            </TableCell>
          </TableRow>
        )}
        {product.created_at && (
          <TableRow>
            <TableCell component="th" variant="head">Ngày tạo</TableCell>
            <TableCell>{new Date(product.created_at).toLocaleString('vi-VN')}</TableCell>
          </TableRow>
        )}
        {product.updated_at && (
          <TableRow>
            <TableCell component="th" variant="head">Cập nhật lần cuối</TableCell>
            <TableCell>{new Date(product.updated_at).toLocaleString('vi-VN')}</TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  </TableContainer>
));

const ProductDetails = ({ product }) => {
  if (!product) return null;
  
  switch (product.product_type) {
    case 'BOOK':
      return (
        <>
          <BookDetails product={product} />
          <CommonDetails product={product} />
        </>
      );
    case 'SHOE':
      return (
        <>
          <ShoeDetails product={product} />
          <CommonDetails product={product} />
        </>
      );
    default:
      return <CommonDetails product={product} />;
  }
};

export default memo(ProductDetails); 