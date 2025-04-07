import { useState, useEffect } from 'react';

/**
 * Custom hook để đọc/ghi dữ liệu vào localStorage với type-safety
 * 
 * @param {string} key - Khóa lưu trữ trong localStorage
 * @param {any} initialValue - Giá trị mặc định nếu khóa không tồn tại
 * @returns {Array} - [value, setValue, removeValue]
 */
export const useLocalStorage = (key, initialValue) => {
  // Hàm để lấy giá trị từ localStorage
  const readValue = () => {
    if (typeof window === 'undefined') {
      return initialValue;
    }

    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.warn(`Lỗi khi đọc localStorage key "${key}":`, error);
      return initialValue;
    }
  };

  // State để lưu trữ giá trị hiện tại
  const [storedValue, setStoredValue] = useState(readValue);

  // Hàm để cập nhật giá trị trong localStorage và state
  const setValue = (value) => {
    if (typeof window === 'undefined') {
      console.warn(
        `Không thể lưu "${key}" vào localStorage khi không có window.`
      );
    }

    try {
      // Cho phép value là function giống như useState
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      
      // Lưu vào state
      setStoredValue(valueToStore);
      
      // Lưu vào localStorage
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.warn(`Lỗi khi lưu "${key}" vào localStorage:`, error);
    }
  };

  // Hàm để xóa giá trị khỏi localStorage
  const removeValue = () => {
    if (typeof window === 'undefined') {
      console.warn(
        `Không thể xóa "${key}" khỏi localStorage khi không có window.`
      );
    }

    try {
      // Xóa khỏi localStorage
      window.localStorage.removeItem(key);
      
      // Đặt state về giá trị mặc định
      setStoredValue(initialValue);
    } catch (error) {
      console.warn(`Lỗi khi xóa "${key}" khỏi localStorage:`, error);
    }
  };

  // Lắng nghe sự kiện thay đổi để đồng bộ hóa giữa các tab/window
  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === key) {
        setStoredValue(e.newValue ? JSON.parse(e.newValue) : initialValue);
      }
    };
    
    // Đăng ký sự kiện
    window.addEventListener('storage', handleStorageChange);
    
    // Hủy đăng ký khi component unmount
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key, initialValue]);

  return [storedValue, setValue, removeValue];
}; 