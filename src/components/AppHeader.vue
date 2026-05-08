<template>
  <header>
    <nav class="navbar fixed-top">
      <div class="nav-container">
        <RouterLink to="/" class="navbar-brand">
          <img src="/drift-logo.png" alt="DriftDater" class="brand-icon">
          
        </RouterLink>

        <button class="nav-toggle" @click="menuOpen = !menuOpen" :class="{ open: menuOpen }">
          <span></span><span></span><span></span>
        </button>

        <div class="nav-links" :class="{ open: menuOpen }">
          <!-- Logged out links -->
          <template v-if="!auth.user">
            <RouterLink to="/" class="nav-link" @click="menuOpen = false">Home</RouterLink>
            <RouterLink to="/login" class="nav-link" @click="menuOpen = false">Login</RouterLink>
            <RouterLink to="/register" class="nav-link nav-cta" @click="menuOpen = false">Sign Up</RouterLink>
          </template>

          <!-- Logged in links -->
          <template v-else>
            <RouterLink to="/" class="nav-link" @click="menuOpen = false">Dashboard</RouterLink>

            <RouterLink
              to="/matches"
              class="nav-link nav-link-with-badge"
              @click="handleMatchesClick"
            >
              Matches
              <span v-if="matchesBadgeCount > 0" class="nav-badge">{{ matchesBadgeCount }}</span>
            </RouterLink>

            <RouterLink
              to="/messages"
              class="nav-link nav-link-with-badge"
              @click="handleMessagesClick"
            >
              Messages
              <span v-if="messagesBadgeCount > 0" class="nav-badge">{{ messagesBadgeCount }}</span>
            </RouterLink>

            <RouterLink to="/search" class="nav-link" @click="menuOpen = false">Search</RouterLink>

            <div ref="bellWrap" class="nav-bell-wrap">
              <button type="button" class="nav-bell" :class="{ active: notificationsOpen }" @click="toggleBell">
                🔔
              </button>
              <span v-if="totalNotificationsUnread > 0" class="bell-dot" />

              <div v-if="notificationsOpen" class="notif-dropdown" role="menu">
                <div class="notif-header">Notifications</div>
                <div v-if="totalNotificationsUnread === 0" class="notif-empty">
                  <span class="notif-bell-icon">🔔</span>
                  <p>No notifications yet</p>
                </div>

                <div v-else class="notif-sections">
                  <div class="notif-section">
                    <div class="notif-section-title">New likes</div>
                    <button
                      v-for="like in newLikes.slice(0, 4)"
                      :key="`like-${like.id}`"
                      type="button"
                      class="notif-item"
                      @click="markLikeSeenAndGo(like.id)"
                    >
                      <div class="notif-avatar">
                        <img v-if="like.photo" :src="like.photo" :alt="like.firstName" />
                        <span v-else>{{ initialsFor(like) }}</span>
                      </div>
                      <div class="notif-text">
                        <div class="notif-name">{{ like.firstName }} {{ like.lastName }}</div>
                        <div class="notif-sub">liked you</div>
                      </div>
                    </button>
                    <div v-if="newLikes.length === 0" class="notif-muted">No new likes</div>
                  </div>

                  <div class="notif-section">
                    <div class="notif-section-title">New matches</div>
                    <button
                      v-for="m in newMatches.slice(0, 3)"
                      :key="`match-${m.id}`"
                      type="button"
                      class="notif-item"
                      @click="goToMatchesFromBell"
                    >
                      <div class="notif-avatar">
                        <img v-if="m.user.photo" :src="m.user.photo" :alt="m.user.firstName" />
                        <span v-else>{{ initialsFor(m.user) }}</span>
                      </div>
                      <div class="notif-text">
                        <div class="notif-name">{{ m.user.firstName }} {{ m.user.lastName }}</div>
                        <div class="notif-sub">You matched!</div>
                      </div>
                    </button>
                    <div v-if="newMatches.length === 0" class="notif-muted">No new matches</div>
                  </div>

                  <div class="notif-section">
                    <div class="notif-section-title">New messages</div>
                    <button
                      v-for="c in newMessages.slice(0, 3)"
                      :key="`msg-${c.id}`"
                      type="button"
                      class="notif-item"
                      @click="handleConversationClick(c.user.id)"
                    >
                      <div class="notif-avatar">
                        <img v-if="c.user.photo" :src="c.user.photo" :alt="c.user.firstName" />
                        <span v-else>{{ initialsFor(c.user) }}</span>
                      </div>
                      <div class="notif-text">
                        <div class="notif-name">{{ c.user.firstName }} {{ c.user.lastName }}</div>
                        <div class="notif-sub">{{ c.lastMessage }}</div>
                      </div>
                    </button>
                    <div v-if="newMessages.length === 0" class="notif-muted">No new messages</div>
                  </div>

                  <div class="notif-actions">
                    <RouterLink to="/matches" class="notif-link" @click="handleMatchesClick">
                      View Matches
                    </RouterLink>
                    <RouterLink to="/messages" class="notif-link" @click="handleMessagesClick">
                      View Messages
                    </RouterLink>
                  </div>
                </div>
              </div>
            </div>

            <RouterLink to="/profile" class="nav-link nav-avatar" @click="menuOpen = false">
              <img
                v-if="auth.user?.photo"
                :src="auth.user.photo"
                alt="Profile"
                class="avatar-img"
              />
              <span v-else class="avatar-placeholder">{{ initials }}</span>
            </RouterLink>
            <button class="nav-link nav-logout" @click="handleLogout">Logout</button>
          </template>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useMatchesStore } from '../stores/matches'
import { useMessagesStore } from '../stores/messages'

const auth = useAuthStore()
const router = useRouter()
const menuOpen = ref(false)

const matchesStore = useMatchesStore()
const messagesStore = useMessagesStore()

const bellWrap = ref(null)
const notificationsOpen = ref(false)

const initials = computed(() => {
  if (!auth.user) return '?'
  return `${auth.user.firstName?.[0] || ''}${auth.user.lastName?.[0] || ''}`.toUpperCase()
})

function safeParseJsonArray(v, fallback = []) {
  try {
    const arr = JSON.parse(v)
    return Array.isArray(arr) ? arr : fallback
  } catch {
    return fallback
  }
}

function readMs(key) {
  const raw = sessionStorage.getItem(key)
  const n = Number(raw)
  return Number.isFinite(n) ? n : 0
}

function initialsFor(user) {
  if (!user) return '?'
  return `${user.firstName?.[0] || ''}${user.lastName?.[0] || ''}`.toUpperCase() || '?'
}

const seenVersion = ref(0)

const likesSeenSet = computed(() => {
  // Make this computed re-run after we update sessionStorage.
  void seenVersion.value
  const ids = safeParseJsonArray(sessionStorage.getItem('dd_seen_like_ids') || '[]', [])
  return new Set(ids)
})

const seenMatchesAtMs = computed(() => {
  void seenVersion.value
  return readMs('dd_seen_matches_at')
})

const seenMessagesAtMs = computed(() => {
  void seenVersion.value
  return readMs('dd_seen_messages_at')
})

const newLikes = computed(() => {
  return matchesStore.potentialMatches.filter(p => !likesSeenSet.value.has(p.id))
})

const newMatches = computed(() => {
  const t0 = seenMatchesAtMs.value
  return matchesStore.matches.filter(m => {
    const t = Date.parse(m.matchedAt)
    return Number.isFinite(t) && t > t0
  })
})

const newMessages = computed(() => {
  const t0 = seenMessagesAtMs.value
  return messagesStore.conversations.filter(c => {
    const t = Date.parse(c.lastMessageAt)
    return Number.isFinite(t) && t > t0
  })
})

const messagesBadgeCount = computed(() => newMessages.value.length)
const matchesBadgeCount = computed(() => newMatches.value.length)
const totalNotificationsUnread = computed(() => newLikes.value.length + newMatches.value.length + newMessages.value.length)

async function ensureNotificationsData() {
  if (auth.user) {
    try {
      if (matchesStore.potentialMatches.length === 0) await matchesStore.fetchPotentialMatches()
    } catch {}
    try {
      if (matchesStore.matches.length === 0) await matchesStore.fetchMatches()
    } catch {}
    try {
      if (messagesStore.conversations.length === 0) await messagesStore.fetchConversations()
    } catch {}
  }
}

function markLikesSeen(ids = []) {
  const existing = safeParseJsonArray(sessionStorage.getItem('dd_seen_like_ids') || '[]', [])
  const set = new Set(existing)
  ids.forEach(id => set.add(id))
  sessionStorage.setItem('dd_seen_like_ids', JSON.stringify(Array.from(set)))
  seenVersion.value++
}

function markMessagesSeenNow() {
  sessionStorage.setItem('dd_seen_messages_at', String(Date.now()))
  seenVersion.value++
}

function markMatchesSeenNow() {
  sessionStorage.setItem('dd_seen_matches_at', String(Date.now()))
  seenVersion.value++
}

function toggleBell() {
  menuOpen.value = false
  notificationsOpen.value = !notificationsOpen.value
}

function handleMessagesClick() {
  notificationsOpen.value = false
  menuOpen.value = false
  markMessagesSeenNow()
}

function handleMatchesClick() {
  notificationsOpen.value = false
  menuOpen.value = false
  markMatchesSeenNow()
}

function goToMatchesFromBell() {
  handleMatchesClick()
  router.push('/matches')
}

function handleConversationClick(userId) {
  handleMessagesClick()
  router.push(`/messages?user=${userId}`)
}

function markLikeSeenAndGo(likeProfileId) {
  markLikesSeen([likeProfileId])
  notificationsOpen.value = false
  menuOpen.value = false
  router.push('/')
}

onMounted(async () => {
  if (!auth.user) return
  await ensureNotificationsData()

  document.addEventListener('click', onDocumentClick)
})

onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
})

function onDocumentClick(e) {
  if (!notificationsOpen.value) return
  const el = bellWrap.value
  if (!el) return
  if (e.target instanceof Node && !el.contains(e.target)) {
    notificationsOpen.value = false
  }
}

async function handleLogout() {
  menuOpen.value = false
  await auth.logout()
  router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --drift-rose: #e85d75;
  --drift-coral: #f4845f;
  --drift-warm: #fff5f0;
  --drift-dark: #1a1025;
  --drift-muted: #8b7fa0;
}

.brand-icon {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.navbar {
  background: rgba(255, 245, 240, 0.92);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(232, 93, 117, 0.12);
  z-index: 1000;
  width: 100%;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  font-family: 'Playfair Display', serif;
  font-size: 1.4rem;
  color: var(--drift-dark);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  letter-spacing: -0.02em;
}

.brand-icon { font-size: 1.2rem; }

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.nav-link {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 400;
  color: #4a3f5c;
  text-decoration: none;
  padding: 0.45rem 0.85rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  border: none;
  background: none;
  cursor: pointer;
}

.nav-link:hover, .nav-link.router-link-active {
  background: rgba(232, 93, 117, 0.1);
  color: var(--drift-rose);
}

.nav-cta {
  background: linear-gradient(135deg, var(--drift-rose), var(--drift-coral));
  color: white !important;
  font-weight: 500;
  padding: 0.45rem 1.1rem;
}
.nav-cta:hover {
  opacity: 0.9;
  background: linear-gradient(135deg, var(--drift-rose), var(--drift-coral)) !important;
  color: white !important;
}

.nav-logout {
  color: var(--drift-muted);
  font-size: 0.85rem;
}

.nav-avatar {
  padding: 0.2rem;
  display: flex;
  align-items: center;
}

.avatar-img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--drift-rose);
}

.avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--drift-rose), var(--drift-coral));
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.nav-toggle span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--drift-dark);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.nav-link-with-badge {
  position: relative;
  padding-right: 1.8rem;
}

.nav-badge {
  position: absolute;
  top: -7px;
  right: -4px;
  background: rgba(232, 93, 117, 1);
  color: white;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 245, 240, 0.92);
  pointer-events: none;
}

.nav-bell-wrap {
  position: relative;
}

.nav-bell {
  font-family: 'DM Sans', sans-serif;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.45rem 0.55rem;
  border-radius: 10px;
  color: var(--drift-rose);
  transition: background 0.2s;
  position: relative;
  line-height: 1;
}

.nav-bell:hover {
  background: rgba(232, 93, 117, 0.1);
}

.nav-bell.active {
  background: rgba(232, 93, 117, 0.14);
}

.bell-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ff4d7d;
  box-shadow: 0 0 0 3px rgba(255, 245, 240, 0.92);
}

.notif-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 360px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.16);
  border: 1px solid rgba(232, 93, 117, 0.12);
  padding: 0.75rem;
  z-index: 2000;
}

.notif-header {
  font-family: 'Playfair Display', serif;
  font-size: 1.35rem;
  color: #1a1025;
  padding: 0.25rem 0.35rem 0.65rem;
}

.notif-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 2.25rem 1rem;
  font-family: 'DM Sans', sans-serif;
  color: #8b7fa0;
}

.notif-bell-icon {
  font-size: 1.9rem;
  color: #e85d75;
}

.notif-sections {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.notif-section {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.notif-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  color: #1a1025;
  margin: 0 0 0.2rem;
}

.notif-item {
  display: flex;
  gap: 0.75rem;
  padding: 0.65rem 0.6rem;
  border-radius: 12px;
  background: rgba(232, 93, 117, 0.04);
  border: 1px solid rgba(232, 93, 117, 0.08);
  cursor: pointer;
  text-align: left;
}

.notif-item:hover {
  background: rgba(232, 93, 117, 0.08);
}

.notif-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
  font-family: 'Playfair Display', serif;
  font-weight: 700;
}

.notif-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.notif-text {
  flex: 1;
  min-width: 0;
}

.notif-name {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 700;
  color: #1a1025;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notif-sub {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: #8b7fa0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notif-muted {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  color: #b0a0c0;
  padding: 0.25rem 0.2rem 0.1rem;
}

.notif-actions {
  display: flex;
  gap: 0.6rem;
  justify-content: space-between;
}

.notif-link {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  color: #e85d75;
  text-decoration: none;
  font-weight: 600;
  padding: 0.5rem 0.6rem;
  border-radius: 12px;
  background: rgba(232, 93, 117, 0.06);
  border: 1px solid rgba(232, 93, 117, 0.12);
}

.notif-link:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .nav-toggle { display: flex; }

  .nav-links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: rgba(255, 245, 240, 0.98);
    flex-direction: column;
    padding: 1rem;
    border-bottom: 1px solid rgba(232, 93, 117, 0.12);
    gap: 0.25rem;
  }

  .nav-links.open { display: flex; }

  .nav-link { width: 100%; text-align: left; }
}

@media (max-width: 480px) {
  .notif-dropdown {
    width: 92vw;
    right: -6px;
  }
}
</style>