import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

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
      matches.value = response.data
      return response.data
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
      potentialMatches.value = response.data
      return response.data
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
      potentialMatches.value = potentialMatches.value.filter(m => m.user_id !== userId)
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
      potentialMatches.value = potentialMatches.value.filter(m => m.user_id !== userId)
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

  return { matches, potentialMatches, loading, error, fetchMatches, fetchPotentialMatches, likeUser, passUser, clearMatches }
})