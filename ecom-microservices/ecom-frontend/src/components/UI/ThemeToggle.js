import React from 'react';
import { IconButton, Tooltip, useTheme as useMuiTheme } from '@mui/material';
import { Brightness4 as DarkModeIcon, Brightness7 as LightModeIcon } from '@mui/icons-material';
import { useTheme } from '../../contexts/ThemeContext';

/**
 * Component nút chuyển đổi theme light/dark
 */
const ThemeToggle = ({ size = 'medium', tooltip = true }) => {
  const { themeMode, toggleTheme } = useTheme();
  const muiTheme = useMuiTheme();
  
  const isDarkMode = themeMode === 'dark';
  
  const button = (
    <IconButton
      onClick={toggleTheme}
      color="inherit"
      size={size}
      aria-label={isDarkMode ? 'Chuyển sang chế độ sáng' : 'Chuyển sang chế độ tối'}
      sx={{
        bgcolor: isDarkMode ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.04)',
        '&:hover': {
          bgcolor: isDarkMode ? 'rgba(255, 255, 255, 0.12)' : 'rgba(0, 0, 0, 0.08)'
        },
        transition: muiTheme.transitions.create(['background-color', 'box-shadow'], {
          duration: muiTheme.transitions.duration.short
        }),
        boxShadow: isDarkMode ? '0 0 5px rgba(255, 255, 255, 0.2)' : 'none'
      }}
    >
      {isDarkMode ? <LightModeIcon /> : <DarkModeIcon />}
    </IconButton>
  );
  
  if (tooltip) {
    return (
      <Tooltip title={isDarkMode ? 'Chuyển sang chế độ sáng' : 'Chuyển sang chế độ tối'}>
        {button}
      </Tooltip>
    );
  }
  
  return button;
};

export default ThemeToggle; 