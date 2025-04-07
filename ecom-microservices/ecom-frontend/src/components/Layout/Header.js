import React, { useState, useEffect, useCallback } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Badge,
  Menu,
  MenuItem,
  InputBase,
  Box,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Avatar,
  Tooltip,
  useMediaQuery,
  useTheme
} from '@mui/material';
import {
  ShoppingCart as ShoppingCartIcon,
  Menu as MenuIcon,
  Search as SearchIcon,
  AccountCircle,
  Book,
  Checkroom,
  Favorite,
  ExitToApp,
  Person,
  Favorite as FavoriteIcon,
  History as HistoryIcon,
  Login as LoginIcon,
  PersonAdd as RegisterIcon,
  Home as HomeIcon,
} from '@mui/icons-material';
import { styled, alpha } from '@mui/material/styles';
import { cartService } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { useCart } from '../../contexts/CartContext';
import ThemeToggle from '../UI/ThemeToggle';
import './Header.css';

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginRight: theme.spacing(2),
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(3),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('md')]: {
      width: '20ch',
    },
  },
}));

const Header = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  const { isAuthenticated, user, logout } = useAuth();
  const { cart, resetCart } = useCart();
  
  const [anchorEl, setAnchorEl] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [cartCount, setCartCount] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');

  const isLoggedIn = localStorage.getItem('token') !== null;

  useEffect(() => {
    if (isLoggedIn) {
      fetchCartCount();
    }
  }, [isLoggedIn]);

  useEffect(() => {
    if (cart && cart.items) {
      setCartCount(cart.items.length);
    } else {
      setCartCount(0);
    }
  }, [cart]);

  const fetchCartCount = async () => {
    try {
      const userId = localStorage.getItem('userId');
      
      if (userId) {
        const response = await cartService.getCart(userId);
        const count = response.data.items ? response.data.items.length : 0;
        setCartCount(count);
      } else {
        console.log('Không có userId, bỏ qua việc lấy giỏ hàng');
        setCartCount(0);
      }
    } catch (error) {
      console.error('Error fetching cart:', error);
      setCartCount(0);
    }
  };

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = useCallback(() => {
    handleMenuClose();
    logout();
    resetCart();
    navigate('/', { replace: true });
  }, [logout, resetCart, navigate]);

  const handleSearch = (e) => {
    if (e.key === 'Enter' && searchQuery) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchQuery('');
    }
  };

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  const menuId = 'primary-search-account-menu';
  const renderMenu = (
    <Menu
      anchorEl={anchorEl}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      id={menuId}
      keepMounted
      transformOrigin={{ vertical: 'top', horizontal: 'right' }}
      open={Boolean(anchorEl)}
      onClose={handleMenuClose}
    >
      <MenuItem onClick={() => { handleMenuClose(); navigate('/profile'); }}>Tài khoản</MenuItem>
      <MenuItem onClick={() => { handleMenuClose(); navigate('/orders'); }}>Đơn hàng</MenuItem>
      <MenuItem onClick={handleLogout}>Đăng xuất</MenuItem>
    </Menu>
  );

  const drawerList = (
    <Box
      sx={{ width: 250 }}
      role="presentation"
      onClick={toggleDrawer}
    >
      <List>
        <ListItem component={RouterLink} to="/">
          <ListItemIcon><HomeIcon /></ListItemIcon>
          <ListItemText primary="Trang chủ" />
        </ListItem>
        <ListItem component={RouterLink} to="/books">
          <ListItemIcon><Book /></ListItemIcon>
          <ListItemText primary="Sách" />
        </ListItem>
        <ListItem component={RouterLink} to="/shoes">
          <ListItemIcon><Checkroom /></ListItemIcon>
          <ListItemText primary="Giày" />
        </ListItem>
      </List>
      <Divider />
      <List>
        {isLoggedIn ? (
          <>
            <ListItem component={RouterLink} to="/profile">
              <ListItemIcon><Person /></ListItemIcon>
              <ListItemText primary="Tài khoản" />
            </ListItem>
            <ListItem component={RouterLink} to="/wishlist">
              <ListItemIcon><FavoriteIcon /></ListItemIcon>
              <ListItemText primary="Danh sách yêu thích" />
            </ListItem>
            <ListItem onClick={handleLogout}>
              <ListItemIcon><ExitToApp /></ListItemIcon>
              <ListItemText primary="Đăng xuất" />
            </ListItem>
          </>
        ) : (
          <ListItem component={RouterLink} to="/login">
            <ListItemIcon><LoginIcon /></ListItemIcon>
            <ListItemText primary="Đăng nhập" />
          </ListItem>
        )}
      </List>
    </Box>
  );

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={toggleDrawer}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component={RouterLink}
            to="/"
            sx={{ display: { xs: 'none', sm: 'block' }, color: 'white', textDecoration: 'none' }}
          >
            ECOM Shop
          </Typography>
          <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Tìm kiếm..."
              inputProps={{ 'aria-label': 'search' }}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleSearch}
            />
          </Search>
          <Box sx={{ flexGrow: 1 }} />
          <Box sx={{ display: 'flex' }}>
            <IconButton
              component={RouterLink}
              to="/cart"
              color="inherit"
            >
              <Badge badgeContent={cartCount} color="error">
                <ShoppingCartIcon />
              </Badge>
            </IconButton>
            {isLoggedIn ? (
              <IconButton
                edge="end"
                aria-label="account of current user"
                aria-controls={menuId}
                aria-haspopup="true"
                onClick={handleProfileMenuOpen}
                color="inherit"
              >
                <AccountCircle />
              </IconButton>
            ) : (
              <Button color="inherit" component={RouterLink} to="/login">
                Đăng nhập
              </Button>
            )}
          </Box>
        </Toolbar>
      </AppBar>
      {renderMenu}
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer}
      >
        {drawerList}
      </Drawer>
    </>
  );
};

export default Header; 