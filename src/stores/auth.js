import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { profilePhotoUrl } from '../services/api'

function readStoredUser() {
  try {
    const raw = sessionStorage.getItem('dd_user')
    if (!raw || raw === 'null') return null
    const u = JSON.parse(raw)
    if (!u || typeof u !== 'object' || u.id == null) {
      sessionStorage.removeItem('dd_user')
      return null
    }
    return u
  } catch {
    sessionStorage.removeItem('dd_user')
    return null
  }
}

export function hasPersistedUserSnapshot() {
  return readStoredUser() != null
}

export const useAuthStore = defineStore('auth', () => {
  // State — persisted in sessionStorage so page refresh keeps you logged in
  const user = ref(readStoredUser())
  const loading = ref(false)
  const error = ref(null)

  // ── Register ──────────────────────────────────────────────────────────────
  // Backend endpoint: POST /api/signup
  // Expects JSON: { email, username, password, confirm_password,
  //                 first_name, last_name, date_of_birth, gender }
  async function register(payload) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/api/signup', payload)
      return response.data
    } catch (err) {
      const msgs = err.response?.data?.errors || [err.response?.data?.error] || ['Registration failed']
      error.value = msgs.join(', ')
      throw err
    } finally {
      loading.value = false
    }
  }

  // ── Login ─────────────────────────────────────────────────────────────────
  // Backend endpoint: POST /api/login
  // Expects JSON: { email, password, remember }
  // Returns: { message, user_id }
  // Then we fetch the full profile to populate user state
  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const loginRes = await api.post('/api/login', {
        ...credentials,
        remember: credentials.remember ?? false,
      })
      // After login, fetch the profile to get name/photo etc.
      await fetchCurrentUser()
      if (!user.value) {
        error.value =
          'Login succeeded but the session was not saved. Try a normal (non-private) window, or disable strict tracking prevention for this site — the app needs cookies to talk to the API.'
        throw new Error('Session not established')
      }
      return loginRes.data
    } catch (err) {
      const msg = err.response?.data?.error ||
        (err.response?.data?.errors || []).join(', ') ||
        'Login failed'
      error.value = msg
      throw err
    } finally {
      loading.value = false
    }
  }

  // ── Logout ────────────────────────────────────────────────────────────────
  // Backend endpoint: POST /api/logout
  async function logout() {
    loading.value = true
    error.value = null
    try {
      await api.post('/api/logout')
    } catch (err) {
      // Even if the request fails, clear local state
      console.warn('Logout request failed, clearing local state anyway')
    } finally {
      user.value = null
      sessionStorage.removeItem('dd_user')
      loading.value = false
    }
  }

  // ── Fetch current user ────────────────────────────────────────────────────
  // Backend endpoint: GET /api/profile
  // Returns the logged-in user's profile data
  async function fetchCurrentUser() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/profile')
      // Shape the user object to match what our views expect
      const profileData = response.data
      user.value = {
        id: profileData.user_id,
        firstName: profileData.first_name,
        lastName: profileData.last_name,
        email: profileData.email || '',
        username: profileData.username || '',
        bio: profileData.bio || '',
        location: profileData.location || '',
        gender: profileData.gender || '',
        lookingFor: profileData.looking_for || 'any',
        dateOfBirth: profileData.date_of_birth || '',
        photo: profilePhotoUrl(profileData.profile_photo),
        interests: profileData.interests || [],
        occupation: profileData.occupation || '',
        educationLevel: profileData.education_level || '',
        relationshipGoal: profileData.relationship_goal || '',
        preferredMinAge: profileData.preferred_min_age ?? 18,
        preferredMaxAge: profileData.preferred_max_age ?? 60,
        maxDistanceKm: profileData.max_distance_km ?? 50,
        latitude: profileData.latitude ?? null,
        longitude: profileData.longitude ?? null,
        isPublic: profileData.is_public !== false,
      }
      sessionStorage.setItem('dd_user', JSON.stringify(user.value))
      return user.value
    } catch (err) {
      user.value = null
      sessionStorage.removeItem('dd_user')
      // 401 = not logged in; caller may treat as soft failure
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    loading,
    error,
    register,
    login,
    logout,
    fetchCurrentUser,
  }
})