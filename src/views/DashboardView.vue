<template>
  <div class="dash-page">
    <div class="dash-container">

      <!-- Welcome banner -->
      <div class="welcome-banner">
        <div class="welcome-left">
          <div class="welcome-avatar-wrap">
            <img v-if="auth.user?.photo" :src="auth.user.photo" class="welcome-avatar" alt="You" />
            <div v-else class="welcome-avatar-placeholder">{{ initials }}</div>
            <div class="online-dot"></div>
          </div>
          <div>
            <p class="welcome-eyebrow">Good {{ timeOfDay }} ✦</p>
            <h1 class="welcome-name">{{ auth.user?.firstName || 'There' }}!</h1>
            <p class="welcome-sub">{{ auth.user?.location || 'Set your location to find nearby matches' }}</p>
          </div>
        </div>
        <RouterLink to="/profile/edit" class="btn-edit-profile">✏️ Edit Profile</RouterLink>
      </div>

      <!-- Quick stats -->
      <div class="stats-row">
        <div class="stat-card">
          <span class="stat-icon">❤️</span>
          <div>
            <div class="stat-num">{{ matchCount }}</div>
            <div class="stat-label">Matches</div>
          </div>
        </div>
        <div class="stat-card">
          <span class="stat-icon">💬</span>
          <div>
            <div class="stat-num">{{ messageCount }}</div>
            <div class="stat-label">Conversations</div>
          </div>
        </div>
        <div class="stat-card">
          <span class="stat-icon">🔍</span>
          <div>
            <div class="stat-num">{{ profileComplete }}%</div>
            <div class="stat-label">Profile complete</div>
          </div>
        </div>
      </div>

      <!-- Profile completion nudge -->
      <div v-if="profileComplete < 100" class="completion-bar-card">
        <div class="completion-header">
          <span class="completion-title">Complete your profile to get better matches</span>
          <span class="completion-pct">{{ profileComplete }}%</span>
        </div>
        <div class="completion-track">
          <div class="completion-fill" :style="{ width: profileComplete + '%' }"></div>
        </div>
        <div class="completion-tips">
          <span v-if="!auth.user?.bio" class="tip">+ Add a bio</span>
          <span v-if="!auth.user?.photo" class="tip">+ Upload a photo</span>
          <span v-if="!auth.user?.location" class="tip">+ Add your location</span>
          <span v-if="!auth.user?.interests?.length" class="tip">+ Add interests</span>
        </div>
      </div>

      <!-- Quick action cards -->
      <h2 class="section-title">What would you like to do?</h2>
      <div class="action-grid">

        <RouterLink to="/matches" class="action-card action-matches">
          <div class="action-icon">❤️</div>
          <div class="action-body">
            <h3>Browse Matches</h3>
            <p>Discover people who match your vibe</p>
          </div>
          <span class="action-arrow">→</span>
        </RouterLink>

        <RouterLink to="/messages" class="action-card action-messages">
          <div class="action-icon">💬</div>
          <div class="action-body">
            <h3>Messages</h3>
            <p>Chat with your connections</p>
          </div>
          <span class="action-arrow">→</span>
        </RouterLink>

        <RouterLink to="/search" class="action-card action-search">
          <div class="action-icon">🔍</div>
          <div class="action-body">
            <h3>Search Profiles</h3>
            <p>Filter by location, age, interests</p>
          </div>
          <span class="action-arrow">→</span>
        </RouterLink>

        <RouterLink to="/profile" class="action-card action-profile">
          <div class="action-icon">👤</div>
          <div class="action-body">
            <h3>My Profile</h3>
            <p>View and manage your profile</p>
          </div>
          <span class="action-arrow">→</span>
        </RouterLink>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useMatchesStore } from '../stores/matches'
import { useMessagesStore } from '../stores/messages'

const auth = useAuthStore()
const matchesStore = useMatchesStore()
const messagesStore = useMessagesStore()

const initials = computed(() => {
  const u = auth.user
  if (!u) return '?'
  return `${u.firstName?.[0] || ''}${u.lastName?.[0] || ''}`.toUpperCase()
})

const timeOfDay = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 17) return 'afternoon'
  return 'evening'
})

const matchCount = computed(() => matchesStore.matches.length)
const messageCount = computed(() => messagesStore.conversations.length)

const profileComplete = computed(() => {
  const u = auth.user
  if (!u) return 0
  const fields = [u.firstName, u.lastName, u.bio, u.location, u.photo, u.interests?.length]
  const filled = fields.filter(Boolean).length
  return Math.round((filled / fields.length) * 100)
})

onMounted(async () => {
  try { await matchesStore.fetchMatches() } catch {}
  try { await messagesStore.fetchConversations() } catch {}
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=DM+Sans:wght@300;400;500&display=swap');

.dash-page {
  min-height: 100vh;
  background: #fff5f0;
  padding: 5rem 1.5rem 3rem;
}

.dash-container {
  max-width: 860px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Welcome banner */
.welcome-banner {
  background: white;
  border-radius: 22px;
  padding: 1.75rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  box-shadow: 0 2px 20px rgba(0,0,0,0.05);
  flex-wrap: wrap;
  animation: fadeUp 0.4s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}

.welcome-left { display: flex; align-items: center; gap: 1.25rem; }

.welcome-avatar-wrap { position: relative; flex-shrink: 0; }

.welcome-avatar {
  width: 72px; height: 72px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e85d75;
}

.welcome-avatar-placeholder {
  width: 72px; height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.online-dot {
  position: absolute;
  bottom: 2px; right: 2px;
  width: 14px; height: 14px;
  background: #34c759;
  border-radius: 50%;
  border: 2px solid white;
}

.welcome-eyebrow {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  color: #8b7fa0;
  margin: 0 0 0.2rem;
  letter-spacing: 0.05em;
}

.welcome-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem;
  color: #1a1025;
  margin: 0 0 0.2rem;
  letter-spacing: -0.03em;
}

.welcome-sub {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: #8b7fa0;
  margin: 0;
}

.btn-edit-profile {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  color: #e85d75;
  border: 1.5px solid #e85d75;
  padding: 0.5rem 1.2rem;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-edit-profile:hover { background: #e85d75; color: white; }

/* Stats */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  animation: fadeUp 0.4s ease 0.05s both;
}

.stat-card {
  background: white;
  border-radius: 18px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

.stat-icon { font-size: 1.8rem; }

.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 1.7rem;
  color: #e85d75;
  line-height: 1;
}

.stat-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  color: #8b7fa0;
  margin-top: 0.1rem;
}

/* Profile completion */
.completion-bar-card {
  background: white;
  border-radius: 18px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  animation: fadeUp 0.4s ease 0.1s both;
}

.completion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.completion-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: #4a3f5c;
  font-weight: 500;
}

.completion-pct {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  color: #e85d75;
  font-weight: 600;
}

.completion-track {
  background: #f0eaf6;
  border-radius: 8px;
  height: 8px;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.completion-fill {
  height: 100%;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  border-radius: 8px;
  transition: width 0.6s ease;
}

.completion-tips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tip {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  background: rgba(232, 93, 117, 0.08);
  color: #e85d75;
  padding: 0.25rem 0.65rem;
  border-radius: 16px;
  border: 1px solid rgba(232, 93, 117, 0.15);
  cursor: pointer;
}

/* Action grid */
.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.3rem;
  color: #1a1025;
  margin: 0;
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  animation: fadeUp 0.4s ease 0.15s both;
}

.action-card {
  background: white;
  border-radius: 18px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1.5px solid transparent;
}

.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 24px rgba(232, 93, 117, 0.12);
  border-color: rgba(232, 93, 117, 0.15);
}

.action-icon { font-size: 2rem; flex-shrink: 0; }

.action-body { flex: 1; }

.action-body h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  color: #1a1025;
  margin: 0 0 0.2rem;
}

.action-body p {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  color: #8b7fa0;
  margin: 0;
}

.action-arrow {
  font-size: 1.1rem;
  color: #e85d75;
  font-weight: 500;
  flex-shrink: 0;
  transition: transform 0.2s;
}

.action-card:hover .action-arrow { transform: translateX(3px); }

@media (max-width: 600px) {
  .stats-row { grid-template-columns: 1fr 1fr; }
  .stats-row .stat-card:last-child { grid-column: span 2; }
  .action-grid { grid-template-columns: 1fr; }
  .welcome-banner { flex-direction: column; align-items: flex-start; }
}
</style>