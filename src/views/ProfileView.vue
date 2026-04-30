<template>
  <div class="profile-page">
    <div class="profile-container">
      <div v-if="profileStore.loading" class="loading-state">
        <div class="spinner-large"></div>
        <p>Loading profile...</p>
      </div>

      <div v-else-if="profileData" class="profile-card">
        <!-- Header / hero -->
        <div class="profile-hero">
          <div class="profile-photo-wrap">
            <img
              v-if="profileData.photo"
              :src="profileData.photo"
              :alt="profileData.firstName"
              class="profile-photo"
            />
            <div v-else class="profile-photo-placeholder">
              {{ initials }}
            </div>
          </div>

          <div class="profile-hero-info">
            <h1 class="profile-name">
              {{ profileData.firstName }} {{ profileData.lastName }}
              <span class="profile-age">, {{ profileData.age }}</span>
            </h1>
            <p class="profile-location">📍 {{ profileData.location || 'Location not set' }}</p>
            <p v-if="profileData.bio" class="profile-bio">{{ profileData.bio }}</p>

            <div class="profile-badges">
              <span v-if="profileData.gender" class="badge badge-gender">{{ profileData.gender }}</span>
              <span v-if="profileData.lookingFor" class="badge badge-looking">Looking for {{ profileData.lookingFor }}</span>
            </div>

            <RouterLink to="/profile/edit" class="btn-edit">✏️ Edit Profile</RouterLink>
          </div>
        </div>

        <!-- Interests -->
        <div v-if="profileData.interests?.length" class="profile-section">
          <h3 class="section-heading">Interests</h3>
          <div class="interests-list">
            <span
              v-for="interest in profileData.interests"
              :key="interest"
              class="interest-tag"
            >{{ interest }}</span>
          </div>
        </div>

        <!-- Stats row -->
        <div class="profile-stats">
          <div class="stat">
            <span class="stat-num">{{ matchCount }}</span>
            <span class="stat-label">Matches</span>
          </div>
          <div class="stat">
            <span class="stat-num">{{ messageCount }}</span>
            <span class="stat-label">Messages</span>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <span>👤</span>
        <p>Profile not found.</p>
        <RouterLink to="/profile/edit" class="btn-primary">Create Profile</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProfileStore } from '../stores/profile'
import { useMatchesStore } from '../stores/matches'
import { useMessagesStore } from '../stores/messages'

const auth = useAuthStore()
const profileStore = useProfileStore()
const matchesStore = useMatchesStore()
const messagesStore = useMessagesStore()

const profileData = ref(null)

const initials = computed(() => {
  if (!profileData.value) return '?'
  return `${profileData.value.firstName?.[0] || ''}${profileData.value.lastName?.[0] || ''}`.toUpperCase()
})

const matchCount = computed(() => matchesStore.matches.length)
const messageCount = computed(() => messagesStore.conversations.length)

onMounted(async () => {
  if (auth.user?.id) {
    try {
      const data = await profileStore.fetchProfile(auth.user.id)
      profileData.value = data
    } catch {
      profileData.value = auth.user
    }
  } else {
    profileData.value = auth.user
  }
  try { await matchesStore.fetchMatches() } catch {}
  try { await messagesStore.fetchConversations() } catch {}
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

.profile-page {
  min-height: 100vh;
  background: #fff5f0;
  padding: 5rem 1.5rem 3rem;
}

.profile-container {
  max-width: 720px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 4px 32px rgba(0,0,0,0.07);
  animation: fadeUp 0.4s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.profile-hero {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #fff5f0 0%, white 100%);
  border-bottom: 1px solid #f0eaf6;
  align-items: flex-start;
  flex-wrap: wrap;
}

.profile-photo-wrap { flex-shrink: 0; }

.profile-photo {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #e85d75;
}

.profile-photo-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  font-family: 'Playfair Display', serif;
  font-size: 2.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid transparent;
}

.profile-hero-info { flex: 1; }

.profile-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.9rem;
  color: #1a1025;
  margin: 0 0 0.3rem;
  letter-spacing: -0.02em;
}

.profile-age { font-weight: 600; color: #e85d75; }

.profile-location {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: #8b7fa0;
  margin: 0 0 0.75rem;
}

.profile-bio {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  color: #4a3f5c;
  line-height: 1.6;
  margin: 0 0 1rem;
  max-width: 440px;
}

.profile-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.25rem; }

.badge {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
}

.badge-gender { background: rgba(232, 93, 117, 0.1); color: #c0384d; }
.badge-looking { background: rgba(244, 132, 95, 0.1); color: #b55a30; }

.btn-edit {
  display: inline-block;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  font-weight: 500;
  color: #e85d75;
  border: 1.5px solid #e85d75;
  padding: 0.5rem 1.2rem;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-edit:hover { background: #e85d75; color: white; }

.profile-section { padding: 1.5rem 2rem; border-bottom: 1px solid #f0eaf6; }

.section-heading {
  font-family: 'Playfair Display', serif;
  font-size: 1.1rem;
  color: #1a1025;
  margin: 0 0 1rem;
}

.interests-list { display: flex; flex-wrap: wrap; gap: 0.5rem; }

.interest-tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  background: rgba(232, 93, 117, 0.08);
  color: #e85d75;
  padding: 0.35rem 0.85rem;
  border-radius: 20px;
  border: 1px solid rgba(232, 93, 117, 0.15);
}

.profile-stats {
  display: flex;
  padding: 1.5rem 2rem;
  gap: 2rem;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
}

.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem;
  color: #e85d75;
  line-height: 1;
}

.stat-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  color: #8b7fa0;
}

.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 4rem;
  color: #8b7fa0;
  font-family: 'DM Sans', sans-serif;
}

.empty-state span { font-size: 3rem; }

.btn-primary {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  text-decoration: none;
  font-size: 0.9rem;
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