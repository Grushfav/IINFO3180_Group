<template>
  <div class="matches-page">
    <div class="matches-container">
      <div class="page-header">
        <h1 class="page-title">Your Matches</h1>
        <p class="page-subtitle">People who liked you back 💫</p>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner-large"></div>
        <p>Finding your matches...</p>
      </div>

      <div v-else-if="displayMatches.length === 0" class="empty-state">
        <div class="empty-icon">💔</div>
        <h3>No matches yet</h3>
        <p>Keep browsing — your match is out there!</p>
        <RouterLink to="/" class="btn-primary">Browse Profiles</RouterLink>
      </div>

      <div v-else class="matches-list">
        <div
          v-for="match in displayMatches"
          :key="`${match.user.id}-${match.id}`"
          class="match-row"
        >
          <img
            v-if="match.user.photo"
            :src="match.user.photo"
            :alt="match.user.firstName"
            class="match-avatar"
          />
          <div v-else class="match-avatar match-avatar-placeholder" aria-hidden="true">
            {{ initialsFor(match.user) }}
          </div>
            <div class="match-info">
            <div class="match-name">{{ match.user.firstName }} {{ match.user.lastName }}, {{ formatAge(match.user.age) }}</div>
            <p v-if="distancePrimary(match)" class="match-distance">{{ distancePrimary(match) }}</p>
            <p class="match-bio">{{ match.user.bio }}</p>
            <div v-if="match.user.interests?.length" class="match-interests">
              <span v-for="tag in match.user.interests.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
          <div class="match-meta">
            <span v-if="match.matchScore" class="score-badge">{{ match.matchScore }}% match</span>
            <span class="match-date">Matched {{ formatDate(match.matchedAt) }}</span>
            <RouterLink
              :to="`/messages?user=${match.user.id}`"
              class="btn-message"
            >
              ✉️ Message
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useMatchesStore } from '../stores/matches'
import { mockMatches } from '../data/mockMatches'

const matchesStore = useMatchesStore()
const loading = ref(false)

const displayMatches = computed(() => {
  return matchesStore.matches.length ? matchesStore.matches : []
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function formatAge(age) {
  if (age == null || age === '' || Number(age) < 1) return '—'
  return age
}

function initialsFor(user) {
  if (!user) return '?'
  return `${user.firstName?.[0] || ''}${user.lastName?.[0] || ''}`.toUpperCase() || '?'
}

function distancePrimary(match) {
  if (match?.distanceKm == null) return ''
  const km = `${match.distanceKm} km away`
  if (match.distanceMi != null) return `${km} (${match.distanceMi} mi)`
  return km
}

onMounted(async () => {
  loading.value = true
  try {
    await matchesStore.fetchMatches()
  } catch {
    matchesStore.matches = mockMatches
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

.matches-page {
  min-height: 100vh;
  background: #fff5f0;
  padding: 5rem 1.5rem 3rem;
}

.matches-container {
  max-width: 760px;
  margin: 0 auto;
}

.page-header { margin-bottom: 2rem; }

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

.matches-list { display: flex; flex-direction: column; gap: 0.75rem; }

.match-row {
  background: white;
  border-radius: 18px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  flex-wrap: wrap;
  animation: fadeUp 0.35s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.match-row:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(232, 93, 117, 0.1);
}

.match-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e85d75;
  flex-shrink: 0;
}

.match-avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Playfair Display', serif;
  font-size: 1.35rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  object-fit: unset;
}

.match-info { flex: 1; min-width: 160px; }

.match-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.1rem;
  color: #1a1025;
  margin-bottom: 0.3rem;
}

.match-distance {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  color: #b0a0c0;
  margin: 0 0 0.35rem;
}

.match-bio {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: #6b5f7a;
  margin: 0 0 0.5rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.match-interests { display: flex; flex-wrap: wrap; gap: 0.35rem; }

.tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  background: rgba(232, 93, 117, 0.08);
  color: #e85d75;
  padding: 0.2rem 0.55rem;
  border-radius: 16px;
}

.match-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  flex-shrink: 0;
}

.score-badge {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  font-weight: 500;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  padding: 0.25rem 0.65rem;
  border-radius: 16px;
}

.match-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: #b0a0c0;
}

.btn-message {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  font-weight: 500;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  padding: 0.55rem 1.2rem;
  border-radius: 10px;
  text-decoration: none;
  transition: opacity 0.2s;
  white-space: nowrap;
}

.btn-message:hover { opacity: 0.88; }

.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 5rem 2rem;
  text-align: center;
  font-family: 'DM Sans', sans-serif;
  color: #8b7fa0;
}

.empty-icon { font-size: 3.5rem; }

.empty-state h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.4rem;
  color: #1a1025;
  margin: 0;
}

.empty-state p { margin: 0; font-size: 0.92rem; }

.btn-primary {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  text-decoration: none;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  transition: opacity 0.2s;
}

.btn-primary:hover { opacity: 0.9; }

.spinner-large {
  width: 40px; height: 40px;
  border: 3px solid rgba(232, 93, 117, 0.2);
  border-top-color: #e85d75;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>