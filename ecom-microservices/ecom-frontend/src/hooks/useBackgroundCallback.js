import { useCallback, useState, useRef } from 'react';

/**
 * Hook custom để chạy các tác vụ nặng trong background thread (Web Worker)
 * Sử dụng kỹ thuật inline worker để không cần tạo file riêng
 * 
 * @param {Function} heavyTask - Hàm thực hiện tác vụ nặng
 * @param {Object} options - Tùy chọn
 * @param {boolean} options.immediate - Có thực hiện tác vụ ngay khi component mount không
 * @param {Array} deps - Các dependencies cho callback
 * @returns {Object} - { execute, result, error, loading } 
 */
export default function useBackgroundCallback(heavyTask, options = {}, deps = []) {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Lưu worker trong một ref để tránh tạo mới mỗi lần render
  const workerRef = useRef(null);
  
  // Hàm để tạo mã nguồn cho web worker từ callback function
  const createWorkerBlob = useCallback((fn) => {
    // Chuyển đổi function thành text
    const fnString = fn.toString();
    
    // Tạo mã nguồn cho worker
    const code = `
      self.onmessage = function(e) {
        const args = e.data.args;
        try {
          // Khởi tạo hàm từ chuỗi và thực thi với arguments
          const fn = ${fnString};
          const result = fn.apply(null, args);
          
          // Xử lý Promise nếu hàm trả về Promise
          if (result && typeof result.then === 'function') {
            result
              .then(value => {
                self.postMessage({ status: 'success', result: value });
              })
              .catch(err => {
                self.postMessage({ 
                  status: 'error', 
                  error: { message: err.message, stack: err.stack } 
                });
              });
          } else {
            // Trả về kết quả nếu không phải Promise
            self.postMessage({ status: 'success', result });
          }
        } catch (err) {
          self.postMessage({ 
            status: 'error', 
            error: { message: err.message, stack: err.stack } 
          });
        }
      };
    `;
    
    // Tạo Blob từ code
    const blob = new Blob([code], { type: 'application/javascript' });
    return URL.createObjectURL(blob);
  }, []);
  
  // Hàm tạo worker
  const createWorker = useCallback((fn) => {
    if (typeof window === 'undefined' || !window.Worker) {
      console.warn('Web Workers không được hỗ trợ trong môi trường này');
      return null;
    }
    
    // Dọn dẹp worker cũ nếu có
    if (workerRef.current) {
      workerRef.current.terminate();
    }
    
    // Tạo URL cho worker
    const workerUrl = createWorkerBlob(fn);
    
    // Tạo worker mới
    const worker = new Worker(workerUrl);
    
    // Giải phóng URL
    URL.revokeObjectURL(workerUrl);
    
    return worker;
  }, [createWorkerBlob]);
  
  // Hàm để thực thi tác vụ trong worker
  const execute = useCallback((...args) => {
    setLoading(true);
    setError(null);
    
    // Tạo worker mới cho mỗi lần gọi để tránh xung đột
    const worker = createWorker(heavyTask);
    
    // Không thể tạo worker
    if (!worker) {
      try {
        // Fallback: thực thi trực tiếp trên main thread
        const result = heavyTask(...args);
        if (result && typeof result.then === 'function') {
          // Xử lý Promise
          result
            .then(value => {
              setResult(value);
              setLoading(false);
            })
            .catch(err => {
              setError(err);
              setLoading(false);
            });
        } else {
          // Kết quả không phải Promise
          setResult(result);
          setLoading(false);
        }
      } catch (err) {
        setError(err);
        setLoading(false);
      }
      return;
    }
    
    // Lưu worker vào ref
    workerRef.current = worker;
    
    // Xử lý kết quả từ worker
    worker.onmessage = (e) => {
      const { status, result: workerResult, error: workerError } = e.data;
      
      if (status === 'success') {
        setResult(workerResult);
      } else if (status === 'error') {
        setError(new Error(workerError.message));
      }
      
      setLoading(false);
      worker.terminate();
    };
    
    // Xử lý lỗi từ worker
    worker.onerror = (err) => {
      setError(err);
      setLoading(false);
      worker.terminate();
    };
    
    // Gửi arguments đến worker
    worker.postMessage({ args });
  }, [heavyTask, createWorker, ...deps]);
  
  // Chạy tác vụ ngay khi component mount nếu immediate = true
  const { immediate } = options;
  const initialRun = useRef(false);
  
  if (immediate && !initialRun.current) {
    initialRun.current = true;
    execute();
  }
  
  // Dọn dẹp khi component unmount
  useCallback(() => {
    return () => {
      if (workerRef.current) {
        workerRef.current.terminate();
        workerRef.current = null;
      }
    };
  }, []);
  
  return { execute, result, error, loading };
} 