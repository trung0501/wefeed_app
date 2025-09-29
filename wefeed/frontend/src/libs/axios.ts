import axios from 'axios';

// Tạo instance axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  withCredentials: false, // nếu backend cần cookie thì bật true
});

// Interceptor cho request: tự động gắn token nếu có
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor cho response: xử lý lỗi chung
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Ví dụ: token hết hạn → logout
    if (error.response?.status === 401) {
      console.warn('Token hết hạn hoặc không hợp lệ');
      // Có thể redirect về trang login ở đây
    }
    return Promise.reject(error);
  }
);

export default api;

