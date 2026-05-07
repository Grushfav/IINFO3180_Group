import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { profilePhotoUrl } from '../services/api'

export const useMatchesStore = defineStore('matches', () => {
  const matches = ref([])
  const potentialMatches = ref([])
  const loading = ref(false)
  const error = ref(null)

  // GET /api/matches — mutual matches
  async function fetchMatches() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/matches')
      matches.value = response.data.map(normalizeMatch)
      return matches.value
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to fetch matches'
      throw err
    } finally {
      loading.value = false
    }
  }

  // GET /api/matches/potential
  async function fetchPotentialMatches() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/matches/potential')
      potentialMatches.value = response.data.map(normalizePotentialMatch)
      return potentialMatches.value
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to fetch potential matches'
      throw err
    } finally {
      loading.value = false
    }
  }

  // POST /api/matches/like/<user_id>
  async function likeUser(userId) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/api/matches/like/${userId}`)
      potentialMatches.value = potentialMatches.value.filter(m => m.userId !== userId)
      if (response.data.matched) {
        await fetchMatches()
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to like user'
      throw err
    } finally {
      loading.value = false
    }
  }

  // POST /api/matches/pass/<user_id>
  async function passUser(userId) {
    loading.value = true
    error.value = null
    try {
      await api.post(`/api/matches/pass/${userId}`)
      potentialMatches.value = potentialMatches.value.filter(m => m.userId !== userId)
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Failed to pass user'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearMatches() {
    matches.value = []
    potentialMatches.value = []
    error.value = null
  }

  function normalizeUser(user = {}) {
    return {
      id: user.user_id || user.id,
      userId: user.user_id || user.id,
      firstName: user.first_name || '',
      lastName: user.last_name || '',
      age: user.age ?? null,
      bio: user.bio || '',
      location: user.location || '',
      interests: user.interests || [],
      photo: profilePhotoUrl(user.profile_photo),
    }
  }

  function normalizeMatch(match) {
    return {
      id: match.id,
      matchedAt: match.matched_at,
      user: normalizeUser(match.user),
      matchScore: match.match_score ?? null,
      distanceKm: match.distance_km ?? null,
      distanceMi: match.distance_mi ?? null,
    }
  }

  function normalizePotentialMatch(profile) {
    return {
      id: profile.id,
      userId: profile.user_id,
      firstName: profile.first_name || '',
      lastName: profile.last_name || '',
      age: profile.age ?? null,
      bio: profile.bio || '',
      location: profile.location || '',
      interests: profile.interests || [],
      photo: profilePhotoUrl(profile.profile_photo),
      matchScore: profile.match_score ?? null,
      distanceKm: profile.distance_km ?? null,
      distanceMi: profile.distance_mi ?? null,
    }
  }

  return { matches, potentialMatches, loading, error, fetchMatches, fetchPotentialMatches, likeUser, passUser, clearMatches }
})