import React, { createContext, useContext, useState, useEffect } from 'react';
import { ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import { lightTheme, darkTheme } from '../theme/theme';
import { useLocalStorage } from '../hooks/useLocalStorage';

// Khởi tạo context
const ThemeContext = createContext();

/**
 * Theme Provider để quản lý theme của ứng dụng
 */
export const ThemeProvider = ({ children }) => {
  // Sử dụng localStorage để lưu trữ theme
  const [themeMode, setThemeMode] = useLocalStorage('themeMode', 'light');
  
  // State để theo dõi theme hiện tại
  const [theme, setTheme] = useState(themeMode === 'dark' ? darkTheme : lightTheme);
  
  // Hàm chuyển đổi theme
  const toggleTheme = () => {
    setThemeMode(prevMode => {
      const newMode = prevMode === 'light' ? 'dark' : 'light';
      return newMode;
    });
  };
  
  // Theo dõi thay đổi của themeMode và cập nhật theme
  useEffect(() => {
    setTheme(themeMode === 'dark' ? darkTheme : lightTheme);
  }, [themeMode]);
  
  // Hàm cập nhật theme dựa vào mode
  const setMode = (mode) => {
    if (mode === 'light' || mode === 'dark') {
      setThemeMode(mode);
    }
  };
  
  // Giá trị context
  const value = {
    themeMode,
    theme,
    toggleTheme,
    setMode,
    isDarkMode: themeMode === 'dark'
  };
  
  return (
    <ThemeContext.Provider value={value}>
      <MuiThemeProvider theme={theme}>
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};

/**
 * Custom hook để sử dụng ThemeContext
 */
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme phải được sử dụng trong ThemeProvider');
  }
  return context;
}; 