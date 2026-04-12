import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useSearchStore = defineStore('search', () => {
  const results = ref([])
  const loading = ref(false)
  const error = ref(null)
  const filters = ref({ name: '', location: '', ageMin: null, ageMax: null, gender: '', interests: [] })

  // GET /api/users with query params
  async function searchUsers() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/users', {
        params: {
          name: filters.value.name || undefined,
          location: filters.value.location || undefined,
          age_min: filters.value.ageMin || undefined,
          age_max: filters.value.ageMax || undefined,
          gender: filters.value.gender || undefined,
          interests: filters.value.interests.length ? filters.value.interests.join(',') : undefined,
        }
      })
      results.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Search failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  function setFilter(key, value) { filters.value[key] = value }

  function resetFilters() {
    filters.value = { name: '', location: '', ageMin: null, ageMax: null, gender: '', interests: [] }
    results.value = []
  }

  function clearResults() { results.value = []; error.value = null }

  return { results, loading, error, filters, searchUsers, setFilter, resetFilters, clearResults }
})