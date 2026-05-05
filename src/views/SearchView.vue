<template>
  <div class="search-page">
    <div class="search-container">
      <div class="page-header">
        <h1 class="page-title">Search & Discover</h1>
        <p class="page-subtitle">Find someone who gets you</p>
      </div>

      <!-- Filter panel -->
      <div class="filter-panel">
        <div class="filter-row">
          <div class="filter-group">
            <label class="filter-label">Name or Bio</label>
            <input v-model="filters.name" type="text" class="filter-input" placeholder="Search by name or bio..." />
          </div>
          <div class="filter-group">
            <label class="filter-label">Parish</label>
            <select v-model="filters.location" class="filter-input filter-select">
              <option value="">Any parish</option>
              <option v-for="p in parishes" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>
        </div>

        <div class="filter-row">
          <div class="filter-group">
            <label class="filter-label">Min Age</label>
            <input v-model.number="filters.ageMin" type="number" class="filter-input" placeholder="18" min="18" max="99" />
          </div>
          <div class="filter-group">
            <label class="filter-label">Max Age</label>
            <input v-model.number="filters.ageMax" type="number" class="filter-input" placeholder="99" min="18" max="99" />
          </div>
          <div class="filter-group">
            <label class="filter-label">Gender</label>
            <select v-model="filters.gender" class="filter-input filter-select">
              <option value="">Any</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div class="filter-group">
            <label class="filter-label">Sort By</label>
            <select v-model="filters.sortBy" class="filter-input filter-select">
              <option value="newest">Newest</option>
              <option value="age_asc">Age: Low to High</option>
              <option value="age_desc">Age: High to Low</option>
              <option value="name_asc">Name: A-Z</option>
            </select>
          </div>
        </div>

        <!-- Interest chips -->
        <div class="filter-group">
          <label class="filter-label">Interests</label>
          <div class="interest-chips">
            <span
              v-for="interest in allInterests"
              :key="interest"
              class="chip"
              :class="{ active: filters.interests.includes(interest) }"
              @click="toggleInterest(interest)"
            >{{ interest }}</span>
          </div>
        </div>

        <div class="filter-actions">
          <button class="btn-search" @click="handleSearch" :disabled="searchStore.loading">
            <span v-if="searchStore.loading" class="spinner"></span>
            <span v-else>🔍 Search</span>
          </button>
          <button class="btn-reset" @click="handleReset">Reset</button>
        </div>
      </div>

      <!-- Results -->
      <div v-if="searchStore.loading" class="loading-state">
        <div class="spinner-large"></div>
        <p>Searching...</p>
      </div>

      <div v-else-if="results.length === 0 && hasSearched" class="empty-state">
        <span>🔭</span>
        <p>No results found. Try adjusting your filters.</p>
      </div>

      <div v-else-if="results.length > 0" class="results-section">
        <p class="result-count">{{ results.length }} profile{{ results.length !== 1 ? 's' : '' }} found</p>
        <div class="results-grid">
          <div
            v-for="user in results"
            :key="user.id"
            class="result-card"
          >
            <div class="result-photo-wrap">
              <img :src="user.photo" :alt="user.firstName" class="result-photo" />
              <span v-if="user.matchScore" class="result-score">{{ user.matchScore }}%</span>
            </div>
            <div class="result-body">
              <div class="result-name">{{ user.firstName }} {{ user.lastName }}, {{ user.age }}</div>
              <div class="result-location">📍 {{ user.location }}</div>
              <p class="result-bio">{{ user.bio }}</p>
              <div class="result-interests">
                <span v-for="tag in (user.interests || []).slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useSearchStore } from '../stores/search'
import { mockUsers } from '../data/mockUsers'
import { JAMAICAN_PARISHES } from '../data/jamaicanParishes'

const parishes = JAMAICAN_PARISHES

const searchStore = useSearchStore()
const hasSearched = ref(false)

const filters = reactive({
  name: '', location: '', ageMin: null, ageMax: null,
  gender: '', interests: [], sortBy: 'newest'
})

const allInterests = [
  'hiking', 'travel', 'photography', 'gaming', 'coffee', 'anime',
  'cooking', 'food', 'music', 'art', 'coding', 'fitness', 'reading',
  'movies', 'dance', 'yoga', 'sports', 'nature'
]

const results = computed(() => searchStore.results)

function toggleInterest(interest) {
  const idx = filters.interests.indexOf(interest)
  if (idx === -1) filters.interests.push(interest)
  else filters.interests.splice(idx, 1)
}

async function handleSearch() {
  hasSearched.value = true
  searchStore.setFilter('name', filters.name)
  searchStore.setFilter('location', filters.location)
  searchStore.setFilter('ageMin', filters.ageMin)
  searchStore.setFilter('ageMax', filters.ageMax)
  searchStore.setFilter('gender', filters.gender)
  searchStore.setFilter('sortBy', filters.sortBy)
  searchStore.filters.interests = [...filters.interests]

  try {
    await searchStore.searchUsers()
  } catch {
    // Fallback: filter mock data locally
    searchStore.results = mockUsers.filter(u => {
      const q = filters.name.toLowerCase()
      const matchName = !q || `${u.firstName} ${u.lastName}`.toLowerCase().includes(q) || u.bio?.toLowerCase().includes(q)
      const matchLoc = !filters.location || u.location?.toLowerCase().includes(filters.location.toLowerCase())
      const matchMin = !filters.ageMin || u.age >= filters.ageMin
      const matchMax = !filters.ageMax || u.age <= filters.ageMax
      const matchGender = !filters.gender || u.gender === filters.gender
      const matchInterests = !filters.interests.length || filters.interests.some(i => u.interests?.includes(i))
      return matchName && matchLoc && matchMin && matchMax && matchGender && matchInterests
    })
  }
}

function handleReset() {
  Object.assign(filters, { name: '', location: '', ageMin: null, ageMax: null, gender: '', interests: [], sortBy: 'newest' })
  searchStore.resetFilters()
  hasSearched.value = false
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

.search-page {
  min-height: 100vh;
  background: #fff5f0;
  padding: 5rem 1.5rem 3rem;
}

.search-container { max-width: 900px; margin: 0 auto; }

.page-header { margin-bottom: 1.75rem; }

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.2rem;
  color: #1a1025;
  margin: 0 0 0.3rem;
  letter-spacing: -0.03em;
}

.page-subtitle {
  font-family: 'DM Sans', sans-serif;
  color: #8b7fa0;
  font-size: 0.95rem;
  margin: 0;
}

.filter-panel {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 2px 16px rgba(0,0,0,0.05);
  margin-bottom: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-row { display: flex; gap: 0.75rem; flex-wrap: wrap; }

.filter-group { display: flex; flex-direction: column; gap: 0.35rem; flex: 1; min-width: 160px; }

.filter-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  font-weight: 500;
  color: #4a3f5c;
}

.filter-input {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  padding: 0.65rem 0.9rem;
  border: 1.5px solid #e8dff0;
  border-radius: 10px;
  outline: none;
  background: #fdfbfe;
  color: #1a1025;
  transition: border-color 0.2s;
  width: 100%;
}

.filter-input:focus { border-color: #e85d75; }
.filter-select { cursor: pointer; }

/* Interest chips */
.interest-chips { display: flex; flex-wrap: wrap; gap: 0.4rem; }

.chip {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  border: 1.5px solid #e8dff0;
  cursor: pointer;
  color: #8b7fa0;
  background: #fdfbfe;
  transition: all 0.2s;
  user-select: none;
}

.chip:hover { border-color: #e85d75; color: #e85d75; }
.chip.active { background: rgba(232, 93, 117, 0.1); border-color: #e85d75; color: #e85d75; font-weight: 500; }

/* Actions */
.filter-actions { display: flex; gap: 0.75rem; align-items: center; }

.btn-search {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  font-size: 0.9rem;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.7rem 1.5rem;
  cursor: pointer;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.btn-search:hover:not(:disabled) { opacity: 0.88; }
.btn-search:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-reset {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  color: #8b7fa0;
  background: #f0eaf6;
  border: none;
  border-radius: 10px;
  padding: 0.7rem 1.25rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-reset:hover { background: #e4dced; }

/* Results */
.result-count {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  color: #8b7fa0;
  margin: 0 0 1rem;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.1rem;
}

.result-card {
  background: white;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.result-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 24px rgba(232, 93, 117, 0.1);
}

.result-photo-wrap { position: relative; }

.result-photo {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.result-score {
  position: absolute;
  top: 8px; right: 8px;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.25rem 0.6rem;
  border-radius: 14px;
}

.result-body { padding: 0.9rem; }

.result-name {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  color: #1a1025;
  margin-bottom: 0.2rem;
}

.result-location {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: #8b7fa0;
  margin-bottom: 0.5rem;
}

.result-bio {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  color: #4a3f5c;
  margin: 0 0 0.6rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.result-interests { display: flex; flex-wrap: wrap; gap: 0.3rem; }

.tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  background: rgba(232, 93, 117, 0.08);
  color: #e85d75;
  padding: 0.18rem 0.5rem;
  border-radius: 14px;
}

/* Loading / empty */
.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 4rem;
  font-family: 'DM Sans', sans-serif;
  color: #8b7fa0;
  text-align: center;
}

.empty-state span { font-size: 3rem; }

.spinner-large {
  width: 40px; height: 40px;
  border: 3px solid rgba(232, 93, 117, 0.2);
  border-top-color: #e85d75;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>