import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useSearchStore = defineStore('search', () => {
  // State
  const results = ref([])
  const loading = ref(false)
  const error = ref(null)
  const filters = ref({
    name: '',
    location: '',
    ageMin: null,
    ageMax: null,
    interests: []
  })

  // Search users based on filters
  async function searchUsers() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/users/search', {
        params: {
          name: filters.value.name || null,
          location: filters.value.location || null,
          age_min: filters.value.ageMin || null,
          age_max: filters.value.ageMax || null,
          interests: filters.value.interests.length
            ? filters.value.interests.join(',')
            : null
        }
      })
      results.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Search failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Update a single filter
  function setFilter(key, value) {
    filters.value[key] = value
  }

  // Reset all filters
  function resetFilters() {
    filters.value = {
      name: '',
      location: '',
      ageMin: null,
      ageMax: null,
      interests: []
    }
    results.value = []
  }

  // Add an interest filter
  function addInterest(interest) {
    if (!filters.value.interests.includes(interest)) {
      filters.value.interests.push(interest)
    }
  }

  // Remove an interest filter
  function removeInterest(interest) {
    filters.value.interests = filters.value.interests.filter(
      i => i !== interest
    )
  }

  // Clear results
  function clearResults() {
    results.value = []
    error.value = null
  }

  return {
    results,
    loading,
    error,
    filters,
    searchUsers,
    setFilter,
    resetFilters,
    addInterest,
    removeInterest,
    clearResults
  }
})