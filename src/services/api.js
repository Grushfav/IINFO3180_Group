import axios from 'axios'

// In development: Flask runs on localhost:5000
// In production (Render): set VITE_API_BASE_URL env variable to your Render backend URL
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL,
  withCredentials: true, // Required for Flask-Login session cookies
})

// Add response interceptor to handle 401s gracefully
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Session expired — clear local storage but don't redirect here
      // Let the router guard handle the redirect
      sessionStorage.removeItem('dd_user')
    }
    return Promise.reject(error)
  }
)

export default api