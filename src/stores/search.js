import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { profilePhotoUrl } from '../services/api'

export const useSearchStore = defineStore('search', () => {
  const results = ref([])
  const loading = ref(false)
  const error = ref(null)
  const filters = ref({ name: '', location: '', ageMin: null, ageMax: null, gender: '', interests: [], sortBy: 'newest' })

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
          sort_by: filters.value.sortBy || undefined,
        }
      })
      results.value = response.data.map(normalizeUser)
      return results.value
    } catch (err) {
      error.value = err.response?.data?.errors?.[0] || 'Search failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  function setFilter(key, value) { filters.value[key] = value }

  function resetFilters() {
    filters.value = { name: '', location: '', ageMin: null, ageMax: null, gender: '', interests: [], sortBy: 'newest' }
    results.value = []
  }

  function clearResults() { results.value = []; error.value = null }

  function normalizeUser(user = {}) {
    return {
      id: user.id,
      userId: user.user_id,
      firstName: user.first_name || '',
      lastName: user.last_name || '',
      age: user.age ?? null,
      gender: user.gender || '',
      bio: user.bio || '',
      location: user.location || '',
      interests: user.interests || [],
      photo: profilePhotoUrl(user.profile_photo),
      matchScore: user.match_score ?? null,
    }
  }

  return { results, loading, error, filters, searchUsers, setFilter, resetFilters, clearResults }
})