import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { profilePhotoUrl } from '../services/api'
import { useAuthStore } from './auth'

export const useProfileStore = defineStore('profile', () => {
  const profile = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // ── Fetch logged-in user's profile ────────────────────────────────────────
  // Backend: GET /api/profile
  async function fetchProfile() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/profile')
      profile.value = normalizeProfile(response.data)
      return profile.value
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to fetch profile'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ── Update profile ────────────────────────────────────────────────────────
  // Backend: POST /api/profile
  // Expects JSON: { first_name, last_name, date_of_birth, gender, bio,
  //                 location, occupation, education_level, relationship_goal }
  async function updateProfile(formData) {
    loading.value = true
    error.value = null
    try {
      // Convert camelCase frontend fields to snake_case backend fields
      const payload = {
        first_name: formData.firstName,
        last_name: formData.lastName,
        date_of_birth: formData.dateOfBirth,
        gender: formData.gender,
        looking_for: formData.lookingFor,
        bio: formData.bio,
        location: formData.location,
        occupation: formData.occupation,
        education_level: formData.educationLevel,
        relationship_goal: formData.relationshipGoal,
        preferred_min_age: formData.preferredMinAge,
        preferred_max_age: formData.preferredMaxAge,
        max_distance_km: formData.maxDistanceKm,
        latitude: formData.latitude,
        longitude: formData.longitude,
        interests: formData.interests || [],
        is_public: formData.isPublic,
      }
      const response = await api.post('/api/profile', payload)
      // Refresh auth store user so header updates
      const auth = useAuthStore()
      await auth.fetchCurrentUser()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to update profile'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ── Upload profile photo ──────────────────────────────────────────────────
  // Backend: POST /api/upload-photo
  async function uploadProfilePicture(imageFile) {
    loading.value = true
    error.value = null
    try {
      const fd = new FormData()
      fd.append('photo', imageFile)
      const response = await api.post('/api/upload-photo', fd, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      // Refresh to get updated photo URL
      const auth = useAuthStore()
      await auth.fetchCurrentUser()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to upload photo'
      throw err
    } finally {
      loading.value = false
    }
  }

  // ── View another user's profile ───────────────────────────────────────────
  // Backend: GET /api/users/<user_id>  (needs to be added — see notes)
  async function fetchUserProfile(userId) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/api/users/${userId}`)
      return normalizeProfile(response.data)
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to fetch user profile'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearProfile() {
    profile.value = null
    error.value = null
  }

  // Normalize snake_case backend response to camelCase for the views
  function normalizeProfile(data) {
    return {
      id: data.id,
      userId: data.user_id,
      firstName: data.first_name || '',
      lastName: data.last_name || '',
      dateOfBirth: data.date_of_birth || '',
      gender: data.gender || '',
      lookingFor: data.looking_for || 'any',
      bio: data.bio || '',
      location: data.location || '',
      photo: profilePhotoUrl(data.profile_photo),
      occupation: data.occupation || '',
      educationLevel: data.education_level || '',
      heightCm: data.height_cm || null,
      relationshipGoal: data.relationship_goal || '',
      preferredMinAge: data.preferred_min_age ?? 18,
      preferredMaxAge: data.preferred_max_age ?? 60,
      maxDistanceKm: data.max_distance_km ?? 50,
      latitude: data.latitude ?? null,
      longitude: data.longitude ?? null,
      interests: data.interests || [],
      isPublic: data.is_public !== false,
    }
  }

  return {
    profile,
    loading,
    error,
    fetchProfile,
    updateProfile,
    uploadProfilePicture,
    fetchUserProfile,
    clearProfile,
  }
})