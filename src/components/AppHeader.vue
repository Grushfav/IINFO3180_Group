<template>
  <header>
    <nav class="navbar fixed-top">
      <div class="nav-container">
        <RouterLink to="/" class="navbar-brand">
          <span class="brand-icon">🌊</span>
          <span class="brand-name">DriftDater</span>
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
            <RouterLink to="/matches" class="nav-link" @click="menuOpen = false">Matches</RouterLink>
            <RouterLink to="/messages" class="nav-link" @click="menuOpen = false">Messages</RouterLink>
            <RouterLink to="/search" class="nav-link" @click="menuOpen = false">Search</RouterLink>
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
import { ref, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const menuOpen = ref(false)

const initials = computed(() => {
  if (!auth.user) return '?'
  return `${auth.user.firstName?.[0] || ''}${auth.user.lastName?.[0] || ''}`.toUpperCase()
})

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
</style>