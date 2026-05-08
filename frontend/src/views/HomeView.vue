<template>
  <div class="home-page">
    <!-- Hero for logged-out users -->
    <section v-if="!auth.user" class="hero">
      <div class="hero-content">
        <p class="hero-eyebrow">✦ Find your connection</p>
        <h1 class="hero-title">Where hearts<br /><em>drift together</em></h1>
        <p class="hero-desc">
          Match with people who share your vibe. Match by location, by interests and by what really matters to you.
        </p>
        <div class="hero-actions">
          <RouterLink to="/register" class="btn-primary">Get Started</RouterLink>
          <RouterLink to="/login" class="btn-ghost">Sign In</RouterLink>
        </div>
      </div>
      <div class="hero-visual">
        <div class="profile-stack">
          <div v-for="(u, i) in demoUsers" :key="u.id" class="stack-card" :style="{ '--i': i }">
            <img :src="u.photo" :alt="u.firstName" class="stack-photo" />
            <div class="stack-info">
              <strong>{{ u.firstName }}, {{ u.age }}</strong>
              <span>{{ u.location }}</span>
            </div>
            <span class="match-badge">{{ u.matchScore }}% match</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Dashboard for logged-in users -->
    <section v-else class="dashboard">
      <div class="dashboard-inner">
        <!-- Welcome banner -->
        <div class="welcome-banner">
          <div class="welcome-left">
            <img
              v-if="auth.user.photo"
              :src="auth.user.photo"
              class="welcome-avatar"
              alt="You"
            />
            <div v-else class="welcome-avatar-placeholder">
              {{ initials }}
            </div>
            <div>
              <h2 class="welcome-title">Welcome, {{ auth.user.firstName }}!</h2>
              <p class="welcome-sub">{{ auth.user.location || 'No location set' }}</p>
              <p class="welcome-bio">{{ auth.user.bio || '' }}</p>
            </div>
          </div>
          <RouterLink to="/profile/edit" class="btn-outline-sm">Edit Profile</RouterLink>
        </div>

        <!-- Filters bar -->
        <div class="filter-bar">
          <h3 class="section-title">Browse Potential Matches</h3>
          <div class="filters">
            <input
              v-model="search"
              type="text"
              class="filter-input"
              placeholder="Search by name or bio..."
            />
            <select v-model="ageFilter" class="filter-select">
              <option value="">All Ages</option>
              <option value="18-24">18–24</option>
              <option value="25-30">25–30</option>
              <option value="31-40">31–40</option>
              <option value="41+">41+</option>
            </select>
            <select v-model="locationFilter" class="filter-select filter-input">
              <option value="">All parishes</option>
              <option v-for="p in parishes" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>
        </div>

        <!-- Match cards -->
        <div v-if="loading" class="loading-state">
          <div class="spinner-large"></div>
          <p>Finding your matches...</p>
        </div>

        <div v-else-if="filteredMatches.length === 0" class="empty-state">
          <img src="/drift-logo.png" alt="DriftDater" class="brand-icon">
          <p>No potential matches found. Try adjusting your filters.</p>
        </div>

        <div v-else class="matches-grid">
          <div
            v-for="user in filteredMatches"
            :key="user.userId ?? user.id"
            class="match-card"
          >
            <div class="card-photo-wrap">
              <img :src="user.photo" :alt="user.firstName" class="card-photo" />
              <span class="card-score">{{ user.matchScore }}%</span>
            </div>
            <div class="card-body">
              <div class="card-name">{{ user.firstName }} {{ user.lastName }}, {{ user.age }}</div>
              <div class="card-location">📍 {{ user.location }}</div>
              <div v-if="formatDistanceLine(user)" class="card-distance">{{ formatDistanceLine(user) }}</div>
              <p class="card-bio">{{ user.bio }}</p>
              <div class="card-interests">
                <span v-for="tag in user.interests.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
            <div class="card-actions">
              <button class="btn-like" @click="handleLike(user.userId ?? user.id)" title="Like">
                ❤️ Like
              </button>
              <button class="btn-pass" @click="handlePass(user.userId ?? user.id)" title="Pass">
                Pass
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useMatchesStore } from '../stores/matches'
import { mockUsers } from '../data/mockUsers'
import { JAMAICAN_PARISHES } from '../data/jamaicanParishes'

const parishes = JAMAICAN_PARISHES

const auth = useAuthStore()
const matchesStore = useMatchesStore()

const loading = ref(false)
const search = ref('')
const ageFilter = ref('')
const locationFilter = ref('')
const potentialMatches = ref([])

// Demo cards for logged-out hero
const demoUsers = mockUsers.slice(0, 3)

const initials = computed(() => {
  if (!auth.user) return '?'
  return `${auth.user.firstName?.[0] || ''}${auth.user.lastName?.[0] || ''}`.toUpperCase()
})

function formatDistanceLine(u) {
  if (u == null || u.distanceKm == null) return ''
  const km = `${u.distanceKm} km away`
  if (u.distanceMi != null) return `${km} (${u.distanceMi} mi)`
  return km
}

const filteredMatches = computed(() => {
  return potentialMatches.value.filter(u => {
    const q = search.value.toLowerCase()
    const matchesSearch = !q ||
      `${u.firstName} ${u.lastName}`.toLowerCase().includes(q) ||
      (u.bio && u.bio.toLowerCase().includes(q))

    const matchesLocation = !locationFilter.value ||
      (u.location && u.location.toLowerCase().includes(locationFilter.value.toLowerCase()))

    let matchesAge = true
    if (ageFilter.value) {
      const [min, max] = ageFilter.value.split('-').map(Number)
      if (max) matchesAge = u.age >= min && u.age <= max
      else matchesAge = u.age >= 41
    }

    return matchesSearch && matchesLocation && matchesAge
  })
})

async function loadMatches() {
  if (!auth.user) return
  loading.value = true
  try {
    const data = await matchesStore.fetchPotentialMatches()
    potentialMatches.value = data
  } catch {
    // fallback to mock data during development
    potentialMatches.value = mockUsers.filter(u => u.id !== auth.user?.id)
  } finally {
    loading.value = false
  }
}

async function handleLike(userId) {
  try {
    await matchesStore.likeUser(userId)
    potentialMatches.value = potentialMatches.value.filter(u => (u.userId ?? u.id) !== userId)
  } catch {
    potentialMatches.value = potentialMatches.value.filter(u => (u.userId ?? u.id) !== userId)
  }
}

async function handlePass(userId) {
  try {
    await matchesStore.passUser(userId)
    potentialMatches.value = potentialMatches.value.filter(u => (u.userId ?? u.id) !== userId)
  } catch {
    potentialMatches.value = potentialMatches.value.filter(u => (u.userId ?? u.id) !== userId)
  }
}

onMounted(loadMatches)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=DM+Sans:wght@300;400;500&display=swap');

.home-page { min-height: 100vh; background: #fff5f0; }

/* ── HERO ── */
.hero {
  max-width: 1100px;
  margin: 0 auto;
  padding: 6rem 1.5rem 4rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.brand-icon {
  width: 100px;
  height: 100px;
  object-fit: contain;
}
.hero-eyebrow {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  letter-spacing: 0.1em;
  color: #e85d75;
  margin-bottom: 1rem;
  text-transform: uppercase;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.5rem, 5vw, 3.8rem);
  color: #1a1025;
  line-height: 1.1;
  letter-spacing: -0.03em;
  margin: 0 0 1.25rem;
}

.hero-title em { color: #e85d75; font-style: italic; }

.hero-desc {
  font-family: 'DM Sans', sans-serif;
  color: #6b5f7a;
  font-size: 1.05rem;
  line-height: 1.7;
  max-width: 420px;
  margin-bottom: 2rem;
}

.hero-actions { display: flex; gap: 1rem; align-items: center; }

.btn-primary {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  padding: 0.85rem 1.75rem;
  border-radius: 12px;
  text-decoration: none;
  font-size: 0.95rem;
  transition: opacity 0.2s, transform 0.1s;
  border: none;
  cursor: pointer;
}

.btn-primary:hover { opacity: 0.9; transform: translateY(-1px); }

.btn-ghost {
  font-family: 'DM Sans', sans-serif;
  color: #4a3f5c;
  text-decoration: none;
  font-size: 0.95rem;
  padding: 0.85rem 1.25rem;
  border-radius: 12px;
  transition: background 0.2s;
}

.btn-ghost:hover { background: rgba(232, 93, 117, 0.08); }

/* Profile stack */
.hero-visual { display: flex; justify-content: center; }

.profile-stack {
  position: relative;
  width: 280px;
  height: 360px;
}

.stack-card {
  position: absolute;
  inset: 0;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  transform: rotate(calc(var(--i) * 6deg - 6deg)) translateY(calc(var(--i) * -10px));
  transition: transform 0.3s ease;
}

.stack-photo { width: 100%; height: 220px; object-fit: cover; }

.stack-info {
  padding: 0.75rem 1rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  font-family: 'DM Sans', sans-serif;
}

.stack-info strong { font-size: 1rem; color: #1a1025; }
.stack-info span { font-size: 0.82rem; color: #8b7fa0; }

.match-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  font-weight: 500;
  padding: 0.3rem 0.65rem;
  border-radius: 20px;
}

/* ── DASHBOARD ── */
.dashboard { padding: 5rem 1.5rem 3rem; }

.dashboard-inner {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.welcome-banner {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  box-shadow: 0 2px 16px rgba(0,0,0,0.05);
  flex-wrap: wrap;
}

.welcome-left { display: flex; align-items: center; gap: 1rem; }

.welcome-avatar {
  width: 64px; height: 64px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e85d75;
}

.welcome-avatar-placeholder {
  width: 64px; height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  font-family: 'Playfair Display', serif;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.4rem;
  color: #1a1025;
  margin: 0 0 0.2rem;
}

.welcome-sub {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: #8b7fa0;
  margin: 0 0 0.2rem;
}

.welcome-bio {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  color: #4a3f5c;
  margin: 0;
  max-width: 400px;
}

.btn-outline-sm {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  color: #e85d75;
  border: 1.5px solid #e85d75;
  padding: 0.5rem 1.1rem;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-outline-sm:hover { background: #e85d75; color: white; }

/* Filter bar */
.filter-bar { display: flex; flex-direction: column; gap: 0.75rem; }

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.35rem;
  color: #1a1025;
  margin: 0;
}

.filters { display: flex; gap: 0.75rem; flex-wrap: wrap; }

.filter-input, .filter-select {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  padding: 0.6rem 0.9rem;
  border: 1.5px solid #e8dff0;
  border-radius: 10px;
  outline: none;
  background: white;
  color: #1a1025;
  transition: border-color 0.2s;
}

.filter-input { flex: 1; min-width: 160px; }
.filter-select { min-width: 130px; cursor: pointer; }
.filter-input:focus, .filter-select:focus { border-color: #e85d75; }

/* Match grid */
.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
}

.match-card {
  background: white;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 2px 16px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}

.match-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 28px rgba(232, 93, 117, 0.12);
}

.card-photo-wrap { position: relative; }

.card-photo {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-score {
  position: absolute;
  top: 10px;
  right: 10px;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  font-weight: 500;
  padding: 0.28rem 0.6rem;
  border-radius: 16px;
}

.card-body { padding: 1rem; flex: 1; }

.card-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  color: #1a1025;
  margin-bottom: 0.2rem;
}

.card-location {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  color: #8b7fa0;
  margin-bottom: 0.25rem;
}

.card-distance {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  color: #b0a0c0;
  margin-bottom: 0.5rem;
}

.card-bio {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: #4a3f5c;
  margin: 0 0 0.75rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-interests { display: flex; flex-wrap: wrap; gap: 0.35rem; }

.tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  background: rgba(232, 93, 117, 0.08);
  color: #e85d75;
  padding: 0.2rem 0.55rem;
  border-radius: 20px;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-top: 1px solid #f5eff8;
}

.btn-like {
  flex: 1;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  font-weight: 500;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.6rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-like:hover { opacity: 0.88; }

.btn-pass {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  font-weight: 500;
  background: #f0eaf6;
  color: #8b7fa0;
  border: none;
  border-radius: 10px;
  padding: 0.6rem 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-pass:hover { background: #e4dced; }

/* Loading / empty states */
.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 4rem;
  color: #8b7fa0;
  font-family: 'DM Sans', sans-serif;
}

.empty-state span { font-size: 2.5rem; }

.spinner-large {
  width: 40px; height: 40px;
  border: 3px solid rgba(232, 93, 117, 0.2);
  border-top-color: #e85d75;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .hero { grid-template-columns: 1fr; padding-top: 5rem; text-align: center; }
  .hero-visual { display: none; }
  .hero-actions { justify-content: center; }
  .hero-desc { margin: 0 auto 2rem; }
}
</style>