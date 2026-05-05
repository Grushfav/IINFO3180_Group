<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <img src="/src/assets/logo.png" alt="DriftDater" class="brand-icon">
        <h1 class="auth-title">Welcome back</h1>
        <p class="auth-subtitle">Sign in to find your drift</p>
      </div>

      <form class="auth-form" @submit.prevent="handleLogin">
        <div class="field-group" :class="{ error: errors.email }">
          <label class="field-label">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="field-input"
            placeholder="you@example.com"
            autocomplete="email"
            @input="errors.email = ''"
          />
          <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
        </div>

        <div class="field-group" :class="{ error: errors.password }">
          <label class="field-label">Password</label>
          <div class="input-wrapper">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="field-input"
              placeholder="••••••••"
              autocomplete="current-password"
              @input="errors.password = ''"
            />
            <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
          <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
        </div>

        <div v-if="authError" class="alert-error">
          {{ authError }}
        </div>

        <button type="submit" class="btn-primary" :disabled="auth.loading">
          <span v-if="auth.loading" class="spinner"></span>
          <span v-else>Sign In</span>
        </button>

        <p class="auth-switch">
          Don't have an account?
          <RouterLink to="/register" class="auth-link">Sign up here</RouterLink>
        </p>
      </form>
    </div>

    <div class="auth-deco">
      <div class="deco-circle c1"></div>
      <div class="deco-circle c2"></div>
      <div class="deco-circle c3"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const form = ref({ email: '', password: '' })
const errors = ref({ email: '', password: '' })
const authError = ref('')
const showPassword = ref(false)

function validate() {
  let valid = true
  errors.value = { email: '', password: '' }
  if (!form.value.email) { errors.value.email = 'Email is required'; valid = false }
  else if (!/\S+@\S+\.\S+/.test(form.value.email)) { errors.value.email = 'Enter a valid email'; valid = false }
  if (!form.value.password) { errors.value.password = 'Password is required'; valid = false }
  return valid
}

async function handleLogin() {
  if (!validate()) return
  authError.value = ''
  try {
    await auth.login(form.value)
    router.push('/')
  } catch (e) {
    authError.value = auth.error || 'Login failed. Please try again.'
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff5f0;
  padding: 2rem 1rem;
  position: relative;
  overflow: hidden;
}

.brand-icon {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.auth-card {
  background: white;
  border-radius: 24px;
  padding: 2.5rem 2rem;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 4px 40px rgba(232, 93, 117, 0.1), 0 1px 4px rgba(0,0,0,0.04);
  position: relative;
  z-index: 1;
  animation: fadeUp 0.5s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-logo { font-size: 2.5rem; margin-bottom: 0.75rem; }

.auth-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.9rem;
  color: #1a1025;
  margin: 0 0 0.35rem;
  letter-spacing: -0.03em;
}

.auth-subtitle {
  font-family: 'DM Sans', sans-serif;
  color: #8b7fa0;
  font-size: 0.95rem;
  margin: 0;
}

.auth-form { display: flex; flex-direction: column; gap: 1.1rem; }

.field-group { display: flex; flex-direction: column; gap: 0.4rem; }

.field-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  color: #4a3f5c;
}

.field-input {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  padding: 0.75rem 1rem;
  border: 1.5px solid #e8dff0;
  border-radius: 12px;
  outline: none;
  color: #1a1025;
  background: #fdfbfe;
  transition: border-color 0.2s, box-shadow 0.2s;
  width: 100%;
}

.field-input:focus {
  border-color: #e85d75;
  box-shadow: 0 0 0 3px rgba(232, 93, 117, 0.12);
}

.field-group.error .field-input { border-color: #e85d75; }

.field-error {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  color: #e85d75;
}

.input-wrapper { position: relative; }
.input-wrapper .field-input { padding-right: 3rem; }

.toggle-pw {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 0;
}

.alert-error {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  background: rgba(232, 93, 117, 0.08);
  color: #c0384d;
  border: 1px solid rgba(232, 93, 117, 0.2);
  border-radius: 10px;
  padding: 0.75rem 1rem;
}

.btn-primary {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  font-size: 1rem;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.85rem;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.btn-primary:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.65; cursor: not-allowed; }

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.auth-switch {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  color: #8b7fa0;
  text-align: center;
  margin: 0;
}

.auth-link {
  color: #e85d75;
  text-decoration: none;
  font-weight: 500;
}
.auth-link:hover { text-decoration: underline; }

/* Decorative background circles */
.auth-deco { position: fixed; inset: 0; pointer-events: none; }

.deco-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.35;
}

.c1 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, #f4845f33, transparent 70%);
  top: -100px; right: -100px;
}

.c2 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, #e85d7533, transparent 70%);
  bottom: -80px; left: -80px;
}

.c3 {
  width: 200px; height: 200px;
  background: radial-gradient(circle, #c47aff22, transparent 70%);
  bottom: 30%; right: 10%;
}
</style>