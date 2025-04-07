import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Custom hook để theo dõi khi một element xuất hiện trong viewport
 * 
 * @param {Object} options - Các tùy chọn cho Intersection Observer
 * @param {Number} options.threshold - Phần trăm phần tử phải hiển thị để kích hoạt callback (0-1)
 * @param {String} options.rootMargin - Lề xung quanh root element
 * @param {Boolean} options.triggerOnce - Nếu true, observer sẽ ngắt kết nối sau lần đầu tiên element hiện ra
 * @returns {Array} - Mảng [ref, isVisible] để sử dụng
 */
export const useIntersectionObserver = ({
  threshold = 0,
  rootMargin = '0px',
  triggerOnce = false
} = {}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [wasTriggered, setWasTriggered] = useState(false);
  const elementRef = useRef(null);
  
  const handleIntersect = useCallback(
    (entries) => {
      const [entry] = entries;
      const newIsVisible = entry.isIntersecting;
      
      setIsVisible(newIsVisible);
      
      if (newIsVisible && triggerOnce && !wasTriggered) {
        setWasTriggered(true);
      }
    },
    [triggerOnce, wasTriggered]
  );
  
  useEffect(() => {
    const element = elementRef.current;
    
    // Không làm gì nếu không có ref element hoặc trình duyệt không hỗ trợ
    if (!element || typeof IntersectionObserver !== 'function') {
      return;
    }
    
    // Thoát sớm nếu đã được kích hoạt trước đó và triggerOnce=true
    if (triggerOnce && wasTriggered) {
      setIsVisible(true);
      return;
    }
    
    const options = {
      threshold,
      rootMargin
    };
    
    // Tạo observer và kết nối với element
    const observer = new IntersectionObserver(handleIntersect, options);
    observer.observe(element);
    
    // Cleanup khi component unmount
    return () => {
      if (element) {
        observer.unobserve(element);
      }
      observer.disconnect();
    };
  }, [handleIntersect, rootMargin, threshold, triggerOnce, wasTriggered]);
  
  // Trả về ref để gắn vào element và state isVisible
  return [elementRef, isVisible];
};

/**
 * Custom hook tương tự nhưng hỗ trợ nhiều element với một callback
 * 
 * @param {Function} callback - Hàm được gọi khi element xuất hiện
 * @param {Object} options - Các tùy chọn cho Intersection Observer
 * @returns {Function} - createRef function để tạo nhiều ref
 */
export const useMultiElementIntersectionObserver = (callback, options = {}) => {
  const observer = useRef(null);
  const elements = useRef(new Map());
  
  const createRef = useCallback(
    (id) => (element) => {
      if (element) {
        elements.current.set(id, element);
      } else {
        elements.current.delete(id);
      }
    },
    []
  );
  
  useEffect(() => {
    const { threshold = 0, rootMargin = '0px' } = options;
    
    const handleIntersect = (entries) => {
      entries.forEach((entry) => {
        callback(entry.target, entry.isIntersecting);
      });
    };
    
    observer.current = new IntersectionObserver(handleIntersect, {
      threshold,
      rootMargin
    });
    
    // Observe tất cả các elements hiện tại
    elements.current.forEach((element) => {
      observer.current.observe(element);
    });
    
    return () => {
      if (observer.current) {
        observer.current.disconnect();
      }
    };
  }, [callback, options]);
  
  // Mỗi khi elements map thay đổi, cập nhật observer
  useEffect(() => {
    if (!observer.current) return;
    
    observer.current.disconnect();
    
    elements.current.forEach((element) => {
      observer.current.observe(element);
    });
    
    return () => {
      if (observer.current) {
        observer.current.disconnect();
      }
    };
  }, [elements.current]);
  
  return createRef;
};

export default useIntersectionObserver;

/**
 * Hook đặc biệt cho lazy loading ảnh, kết hợp IntersectionObserver với preloading
 * 
 * @param {Object} options - Options cho IntersectionObserver
 * @returns {Array} [ref, isVisible, isLoaded, load] - ref để gắn, trạng thái hiển thị, trạng thái load, và hàm load
 */
export function useLazyImage(options = {}) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [shouldLoad, setShouldLoad] = useState(false);
  const [ref, isIntersecting] = useIntersectionObserver({
    triggerOnce: true,
    threshold: 0.1,
    rootMargin: '200px 0px',
    ...options
  });
  
  // Khi phần tử hiển thị trong viewport, bắt đầu tải ảnh
  useEffect(() => {
    if (isIntersecting && !shouldLoad) {
      setShouldLoad(true);
    }
  }, [isIntersecting, shouldLoad]);
  
  // Hàm load ảnh thủ công (sử dụng khi cần preload)
  const load = useCallback(() => {
    if (!shouldLoad) {
      setShouldLoad(true);
    }
  }, [shouldLoad]);
  
  // Sử dụng với <img> như sau:
  // <img 
  //   ref={ref}
  //   src={shouldLoad ? realSrc : placeholderSrc}
  //   onLoad={() => setIsLoaded(true)}
  // />
  
  return [ref, isIntersecting, isLoaded, setIsLoaded, shouldLoad, load];
} 