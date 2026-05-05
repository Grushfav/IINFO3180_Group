<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <img src="/drift-logo.png" alt="DriftDater" class="brand-icon">
        <h1 class="auth-title">Create account</h1>
        <p class="auth-subtitle">Start your journey on DriftDater</p>
      </div>

      <form class="auth-form" @submit.prevent="handleRegister">
        <div class="form-row">
          <div class="field-group" :class="{ error: errors.first_name }">
            <label class="field-label">First Name</label>
            <input v-model="form.first_name" type="text" class="field-input" placeholder="First Name" @input="errors.first_name = ''" />
            <span v-if="errors.first_name" class="field-error">{{ errors.first_name }}</span>
          </div>
          <div class="field-group" :class="{ error: errors.last_name }">
            <label class="field-label">Last Name</label>
            <input v-model="form.last_name" type="text" class="field-input" placeholder="Last Name" @input="errors.last_name = ''" />
            <span v-if="errors.last_name" class="field-error">{{ errors.last_name }}</span>
          </div>
        </div>

        <div class="field-group" :class="{ error: errors.username }">
          <label class="field-label">Username</label>
          <input v-model="form.username" type="text" class="field-input" placeholder="username" @input="errors.username = ''" />
          <span v-if="errors.username" class="field-error">{{ errors.username }}</span>
        </div>

        <div class="field-group" :class="{ error: errors.email }">
          <label class="field-label">Email</label>
          <input v-model="form.email" type="email" class="field-input" placeholder="you@example.com" @input="errors.email = ''" />
          <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
        </div>

        <div class="form-row">
          <div class="field-group" :class="{ error: errors.date_of_birth }">
            <label class="field-label">Date of Birth</label>
            <input v-model="form.date_of_birth" type="date" class="field-input" @input="errors.date_of_birth = ''" />
            <span v-if="errors.date_of_birth" class="field-error">{{ errors.date_of_birth }}</span>
          </div>
          <div class="field-group" :class="{ error: errors.gender }">
            <label class="field-label">Gender</label>
            <select v-model="form.gender" class="field-input field-select" @change="errors.gender = ''">
              <option value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
              <option value="prefer_not_to_say">Prefer not to say</option>
            </select>
            <span v-if="errors.gender" class="field-error">{{ errors.gender }}</span>
          </div>
        </div>

        <div class="field-group">
          <label class="field-label">Looking For</label>
          <select v-model="form.looking_for" class="field-input field-select">
            <option value="any">Any</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div class="field-group" :class="{ error: errors.password }">
          <label class="field-label">Password</label>
          <div class="input-wrapper">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="field-input"
              placeholder="Min. 6 characters"
              @input="errors.password = ''"
            />
            <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
          <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
        </div>

        <div class="field-group" :class="{ error: errors.confirm_password }">
          <label class="field-label">Confirm Password</label>
          <input
            v-model="form.confirm_password"
            type="password"
            class="field-input"
            placeholder="Re-enter password"
            @input="errors.confirm_password = ''"
          />
          <span v-if="errors.confirm_password" class="field-error">{{ errors.confirm_password }}</span>
        </div>

        <div v-if="authError" class="alert-error">{{ authError }}</div>
        <div v-if="successMsg" class="alert-success">{{ successMsg }}</div>

        <button type="submit" class="btn-primary" :disabled="auth.loading">
          <span v-if="auth.loading" class="spinner"></span>
          <span v-else>Create Account</span>
        </button>

        <p class="auth-switch">
          Already have an account?
          <RouterLink to="/login" class="auth-link">Login here</RouterLink>
        </p>
      </form>
    </div>

    <div class="auth-deco">
      <div class="deco-circle c1"></div>
      <div class="deco-circle c2"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const form = ref({
  first_name: '', last_name: '', username: '', email: '',
  date_of_birth: '', gender: '', looking_for: 'any',
  password: '', confirm_password: ''
})
const errors = ref({})
const authError = ref('')
const successMsg = ref('')
const showPassword = ref(false)

function validate() {
  const e = {}
  if (!form.value.first_name) e.first_name = 'Required'
  if (!form.value.last_name) e.last_name = 'Required'
  if (!form.value.username || form.value.username.length < 3) e.username = 'Min. 3 characters'
  if (!form.value.email || !/\S+@\S+\.\S+/.test(form.value.email)) e.email = 'Valid email required'
  if (!form.value.date_of_birth) e.date_of_birth = 'Required'
  if (!form.value.gender) e.gender = 'Required'
  if (!form.value.password || form.value.password.length < 6) e.password = 'Min. 6 characters'
  if (form.value.password !== form.value.confirm_password) e.confirm_password = 'Passwords do not match'
  errors.value = e
  return Object.keys(e).length === 0
}

async function handleRegister() {
  if (!validate()) return
  authError.value = ''
  successMsg.value = ''

  try {
    // Send exactly what the backend SignupForm expects
    await auth.register({
      email: form.value.email,
      username: form.value.username,
      password: form.value.password,
      confirm_password: form.value.confirm_password,
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      date_of_birth: form.value.date_of_birth,
      gender: form.value.gender,
      looking_for: form.value.looking_for,
    })
    successMsg.value = 'Account created! Redirecting to login...'
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    authError.value = auth.error || 'Registration failed. Please try again.'
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
  padding: 5rem 1rem 2rem;
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
  max-width: 480px;
  box-shadow: 0 4px 40px rgba(232, 93, 117, 0.1), 0 1px 4px rgba(0,0,0,0.04);
  position: relative;
  z-index: 1;
  animation: fadeUp 0.5s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.auth-header { text-align: center; margin-bottom: 1.75rem; }
.auth-logo { font-size: 2rem; margin-bottom: 0.5rem; }

.auth-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.75rem;
  color: #1a1025;
  margin: 0 0 0.3rem;
  letter-spacing: -0.03em;
}

.auth-subtitle {
  font-family: 'DM Sans', sans-serif;
  color: #8b7fa0;
  font-size: 0.9rem;
  margin: 0;
}

.auth-form { display: flex; flex-direction: column; gap: 1rem; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }

.field-group { display: flex; flex-direction: column; gap: 0.35rem; }

.field-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  font-weight: 500;
  color: #4a3f5c;
}

.field-input {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.92rem;
  padding: 0.7rem 0.9rem;
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

.field-select { cursor: pointer; }
.field-group.error .field-input { border-color: #e85d75; }

.field-error {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
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
  padding: 0;
}

.alert-error {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  background: rgba(232, 93, 117, 0.08);
  color: #c0384d;
  border: 1px solid rgba(232, 93, 117, 0.2);
  border-radius: 10px;
  padding: 0.7rem 1rem;
}

.alert-success {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  background: rgba(52, 199, 89, 0.08);
  color: #1a7a36;
  border: 1px solid rgba(52, 199, 89, 0.2);
  border-radius: 10px;
  padding: 0.7rem 1rem;
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
  margin-top: 0.25rem;
}

.btn-primary:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
.btn-primary:disabled { opacity: 0.65; cursor: not-allowed; }

.spinner {
  width: 18px; height: 18px;
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

.auth-link { color: #e85d75; text-decoration: none; font-weight: 500; }
.auth-link:hover { text-decoration: underline; }

.auth-deco { position: fixed; inset: 0; pointer-events: none; }
.deco-circle { position: absolute; border-radius: 50%; opacity: 0.35; }
.c1 { width: 380px; height: 380px; background: radial-gradient(circle, #f4845f33, transparent 70%); top: -100px; right: -100px; }
.c2 { width: 280px; height: 280px; background: radial-gradient(circle, #e85d7533, transparent 70%); bottom: -60px; left: -60px; }

@media (max-width: 480px) {
  .form-row { grid-template-columns: 1fr; }
}
</style>