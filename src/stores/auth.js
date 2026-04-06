import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Register
  async function register(formData) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/register', formData)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Login
  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/login', credentials)
      user.value = response.data.user
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Logout
  async function logout() {
    loading.value = true
    error.value = null
    try {
      await api.post('/logout')
      user.value = null
      token.value = null
    } catch (err) {
      error.value = err.response?.data?.message || 'Logout failed'
    } finally {
      loading.value = false
    }
  }

  // Get current logged in user
  async function fetchCurrentUser() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/users/me')
      user.value = response.data
    } catch (err) {
      user.value = null
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    token,
    loading,
    error,
    register,
    login,
    logout,
    fetchCurrentUser
  }
})