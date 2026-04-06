import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useProfileStore = defineStore('profile', () => {
  // State
  const profile = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Get current user's profile
  async function fetchProfile(userId) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/users/${userId}`)
      profile.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch profile'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Update profile
  async function updateProfile(userId, formData) {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/users/${userId}`, formData)
      profile.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update profile'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Upload profile picture
  async function uploadProfilePicture(userId, imageFile) {
    loading.value = true
    error.value = null
    try {
      const formData = new FormData()
      formData.append('photo', imageFile)
      const response = await api.post(`/users/${userId}/photo`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      profile.value.photo = response.data.photo
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to upload photo'
      throw err
    } finally {
      loading.value = false
    }
  }

  // View another user's profile
  async function fetchUserProfile(userId) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/users/${userId}`)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch user profile'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Clear profile
  function clearProfile() {
    profile.value = null
    error.value = null
  }

  return {
    profile,
    loading,
    error,
    fetchProfile,
    updateProfile,
    uploadProfilePicture,
    fetchUserProfile,
    clearProfile
  }
})