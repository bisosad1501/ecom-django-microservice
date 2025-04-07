import React from 'react';
import {
  Box,
  Typography,
  IconButton,
  Card,
  CardMedia,
  TextField,
  Divider
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import { Link } from 'react-router-dom';
import './CartItem.css';

const CartItem = ({
  item,
  onUpdateQuantity,
  onRemove
}) => {
  const handleQuantityChange = (e) => {
    const value = parseInt(e.target.value);
    if (!isNaN(value) && value > 0) {
      onUpdateQuantity(item.id, value);
    }
  };

  const handleIncrease = () => {
    onUpdateQuantity(item.id, item.quantity + 1);
  };

  const handleDecrease = () => {
    if (item.quantity > 1) {
      onUpdateQuantity(item.id, item.quantity - 1);
    }
  };

  return (
    <Card className="cart-item">
      <Box className="cart-item-content">
        <CardMedia
          component="img"
          className="cart-item-image"
          image={item.imageUrl || '/images/placeholder.jpg'}
          alt={item.name}
        />
        
        <Box className="cart-item-details">
          <Box>
            <Typography variant="h6" component={Link} to={`/products/${item.id}`} className="cart-item-name">
              {item.name}
            </Typography>
            
            {item.attributes && (
              <Typography variant="body2" color="text.secondary" className="cart-item-attributes">
                {Object.entries(item.attributes).map(([key, value]) => (
                  `${key}: ${value}`
                )).join(', ')}
              </Typography>
            )}
          </Box>
          
          <Box className="cart-item-price-section">
            <Typography variant="h6" color="primary" className="cart-item-price">
              {item.price.toLocaleString('vi-VN')} ₫
            </Typography>
            
            {item.originalPrice && item.originalPrice > item.price && (
              <Typography variant="body2" color="text.secondary" className="cart-item-original-price">
                {item.originalPrice.toLocaleString('vi-VN')} ₫
              </Typography>
            )}
            
            {item.discount > 0 && (
              <Typography variant="body2" color="error" className="cart-item-discount">
                Giảm {item.discount}%
              </Typography>
            )}
          </Box>
        </Box>
        
        <Box className="cart-item-actions">
          <Box className="cart-item-quantity">
            <IconButton 
              size="small" 
              onClick={handleDecrease} 
              disabled={item.quantity <= 1}
              className="quantity-button"
            >
              <RemoveIcon fontSize="small" />
            </IconButton>
            
            <TextField
              size="small"
              variant="outlined"
              value={item.quantity}
              onChange={handleQuantityChange}
              inputProps={{ 
                min: 1, 
                max: 99,
                style: { textAlign: 'center' }
              }}
              className="quantity-input"
            />
            
            <IconButton 
              size="small" 
              onClick={handleIncrease}
              className="quantity-button"
            >
              <AddIcon fontSize="small" />
            </IconButton>
          </Box>
          
          <Typography variant="h6" className="cart-item-subtotal">
            {(item.price * item.quantity).toLocaleString('vi-VN')} ₫
          </Typography>
          
          <IconButton 
            color="error" 
            onClick={() => onRemove(item.id)}
            className="remove-button"
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      </Box>
      
      <Divider className="cart-item-divider" />
    </Card>
  );
};

export default CartItem; 