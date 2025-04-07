import React, { useState } from 'react';
import { 
  Paper, 
  InputBase, 
  IconButton, 
  Box,
  Divider 
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import './SearchBar.css';

const SearchBar = ({ 
  placeholder = 'Tìm kiếm sản phẩm...', 
  initialValue = '', 
  onSearch,
  fullWidth = false 
}) => {
  const [searchQuery, setSearchQuery] = useState(initialValue);

  const handleInputChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleClear = () => {
    setSearchQuery('');
    if (onSearch) onSearch('');
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (onSearch) onSearch(searchQuery.trim());
  };

  return (
    <Paper 
      component="form" 
      className={`search-bar ${fullWidth ? 'full-width' : ''}`}
      onSubmit={handleSubmit}
    >
      <InputBase
        className="search-input"
        placeholder={placeholder}
        value={searchQuery}
        onChange={handleInputChange}
        fullWidth
        inputProps={{ 'aria-label': 'tìm kiếm' }}
      />
      
      {searchQuery && (
        <>
          <IconButton 
            type="button" 
            aria-label="clear" 
            onClick={handleClear}
            className="search-clear-button"
          >
            <ClearIcon />
          </IconButton>
          <Divider orientation="vertical" flexItem className="search-divider" />
        </>
      )}
      
      <IconButton 
        type="submit" 
        aria-label="search" 
        className="search-button"
      >
        <SearchIcon />
      </IconButton>
    </Paper>
  );
};

export default SearchBar; 