import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useMatchesStore = defineStore('matches', () => {
  // State
  const matches = ref([])
  const potentialMatches = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Get all matches for current user
  async function fetchMatches() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/matches')
      matches.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch matches'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Get potential matches (browse mode)
  async function fetchPotentialMatches() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/matches/potential')
      potentialMatches.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch potential matches'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Like a user
  async function likeUser(userId) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(`/matches/like/${userId}`)
      // remove from potential matches after liking
      potentialMatches.value = potentialMatches.value.filter(
        match => match.id !== userId
      )
      // if mutual match add to matches
      if (response.data.matched) {
        matches.value.push(response.data.match)
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to like user'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Pass/Dislike a user
  async function passUser(userId) {
    loading.value = true
    error.value = null
    try {
      await api.post(`/matches/pass/${userId}`)
      // remove from potential matches after passing
      potentialMatches.value = potentialMatches.value.filter(
        match => match.id !== userId
      )
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to pass user'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Check if two users are matched
  async function checkMatch(userId) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/matches/check/${userId}`)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to check match'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Clear matches
  function clearMatches() {
    matches.value = []
    potentialMatches.value = []
    error.value = null
  }

  return {
    matches,
    potentialMatches,
    loading,
    error,
    fetchMatches,
    fetchPotentialMatches,
    likeUser,
    passUser,
    checkMatch,
    clearMatches
  }
})