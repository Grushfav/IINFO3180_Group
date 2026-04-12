<template>
  <div class="edit-page">
    <div class="edit-container">
      <div class="edit-header">
        <h1 class="edit-title">Edit Profile</h1>
        <p class="edit-subtitle">Keep your profile fresh and authentic</p>
      </div>

      <form class="edit-form" @submit.prevent="handleSave">
        <!-- Photo upload -->
        <div class="photo-section">
          <div class="photo-preview-wrap">
            <img v-if="previewPhoto || form.photo" :src="previewPhoto || form.photo" class="photo-preview" alt="Profile photo" />
            <div v-else class="photo-placeholder">{{ initials }}</div>
          </div>
          <div class="photo-upload-info">
            <label class="btn-upload" for="photo-input">📷 Upload Photo</label>
            <input
              id="photo-input"
              type="file"
              accept="image/*"
              class="hidden-input"
              @change="handlePhotoChange"
            />
            <p class="photo-hint">JPG, PNG — max 5MB</p>
          </div>
        </div>

        <!-- Basic info -->
        <div class="form-section">
          <h3 class="form-section-title">Basic Info</h3>
          <div class="form-row">
            <div class="field-group">
              <label class="field-label">First Name</label>
              <input v-model="form.firstName" type="text" class="field-input" placeholder="First Name" />
            </div>
            <div class="field-group">
              <label class="field-label">Last Name</label>
              <input v-model="form.lastName" type="text" class="field-input" placeholder="Last Name" />
            </div>
          </div>

          <div class="field-group">
            <label class="field-label">Bio / About You</label>
            <textarea v-model="form.bio" class="field-input field-textarea" placeholder="Tell people what makes you, you..." rows="3"></textarea>
          </div>

          <div class="form-row">
            <div class="field-group">
              <label class="field-label">Location</label>
              <input v-model="form.location" type="text" class="field-input" placeholder="City, Country" />
            </div>
            <div class="field-group">
              <label class="field-label">Date of Birth</label>
              <input v-model="form.dateOfBirth" type="date" class="field-input" />
            </div>
          </div>

          <div class="form-row">
            <div class="field-group">
              <label class="field-label">Gender</label>
              <select v-model="form.gender" class="field-input field-select">
                <option value="">Select gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Non-binary">Non-binary</option>
                <option value="Other">Other</option>
                <option value="Prefer not to say">Prefer not to say</option>
              </select>
            </div>
            <div class="field-group">
              <label class="field-label">Looking For</label>
              <select v-model="form.lookingFor" class="field-input field-select">
                <option value="Any">Any</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Non-binary">Non-binary</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Interests -->
        <div class="form-section">
          <h3 class="form-section-title">Interests (min. 3)</h3>
          <div class="interests-input-row">
            <input
              v-model="newInterest"
              type="text"
              class="field-input"
              placeholder="Add an interest..."
              @keydown.enter.prevent="addInterest"
            />
            <button type="button" class="btn-add" @click="addInterest">Add</button>
          </div>
          <div class="interests-list">
            <span
              v-for="interest in form.interests"
              :key="interest"
              class="interest-tag"
            >
              {{ interest }}
              <button type="button" class="remove-interest" @click="removeInterest(interest)">×</button>
            </span>
          </div>
          <p v-if="form.interests.length < 3" class="hint-text">Add at least {{ 3 - form.interests.length }} more interest(s)</p>
        </div>

        <!-- Profile visibility -->
        <div class="form-section">
          <h3 class="form-section-title">Preferences</h3>
          <label class="toggle-row">
            <span class="toggle-label">Public Profile</span>
            <div class="toggle-switch" :class="{ on: form.isPublic }" @click="form.isPublic = !form.isPublic">
              <div class="toggle-knob"></div>
            </div>
          </label>
          <p class="hint-text">When public, other users can discover your profile</p>
        </div>

        <!-- Feedback -->
        <div v-if="errorMsg" class="alert-error">{{ errorMsg }}</div>
        <div v-if="successMsg" class="alert-success">{{ successMsg }}</div>

        <!-- Actions -->
        <div class="form-actions">
          <RouterLink to="/profile" class="btn-cancel">Cancel</RouterLink>
          <button type="submit" class="btn-save" :disabled="profileStore.loading">
            <span v-if="profileStore.loading" class="spinner"></span>
            <span v-else>Save Changes</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProfileStore } from '../stores/profile'

const auth = useAuthStore()
const profileStore = useProfileStore()

const form = ref({
  firstName: '', lastName: '', bio: '', location: '',
  dateOfBirth: '', gender: '', lookingFor: 'Any',
  photo: '', interests: [], isPublic: true
})

const previewPhoto = ref('')
const photoFile = ref(null)
const newInterest = ref('')
const errorMsg = ref('')
const successMsg = ref('')

const initials = computed(() => {
  return `${form.value.firstName?.[0] || ''}${form.value.lastName?.[0] || ''}`.toUpperCase() || '?'
})

function handlePhotoChange(e) {
  const file = e.target.files[0]
  if (!file) return
  photoFile.value = file
  previewPhoto.value = URL.createObjectURL(file)
}

function addInterest() {
  const val = newInterest.value.trim().toLowerCase()
  if (val && !form.value.interests.includes(val)) {
    form.value.interests.push(val)
  }
  newInterest.value = ''
}

function removeInterest(interest) {
  form.value.interests = form.value.interests.filter(i => i !== interest)
}

async function handleSave() {
  errorMsg.value = ''
  successMsg.value = ''

  if (!form.value.firstName || !form.value.lastName) {
    errorMsg.value = 'First and last name are required.'
    return
  }

  const formData = new FormData()
  Object.entries(form.value).forEach(([k, v]) => {
    if (k === 'interests') formData.append(k, JSON.stringify(v))
    else formData.append(k, v)
  })
  if (photoFile.value) formData.append('photo', photoFile.value)

  try {
    await profileStore.updateProfile(auth.user.id, formData)
    successMsg.value = 'Profile updated successfully!'
    if (photoFile.value) {
      await profileStore.uploadProfilePicture(auth.user.id, photoFile.value)
    }
  } catch {
    errorMsg.value = profileStore.error || 'Failed to save profile. Please try again.'
  }
}

onMounted(async () => {
  const user = auth.user
  if (user) {
    Object.assign(form.value, {
      firstName: user.firstName || '',
      lastName: user.lastName || '',
      bio: user.bio || '',
      location: user.location || '',
      dateOfBirth: user.dateOfBirth || '',
      gender: user.gender || '',
      lookingFor: user.lookingFor || 'Any',
      photo: user.photo || '',
      interests: Array.isArray(user.interests) ? [...user.interests] : [],
      isPublic: user.isPublic !== false
    })
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

.edit-page {
  min-height: 100vh;
  background: #fff5f0;
  padding: 5rem 1.5rem 3rem;
}

.edit-container {
  max-width: 620px;
  margin: 0 auto;
}

.edit-header { margin-bottom: 1.75rem; }

.edit-title {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  color: #1a1025;
  margin: 0 0 0.3rem;
  letter-spacing: -0.03em;
}

.edit-subtitle {
  font-family: 'DM Sans', sans-serif;
  color: #8b7fa0;
  font-size: 0.92rem;
  margin: 0;
}

.edit-form {
  background: white;
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 4px 32px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  gap: 0;
  animation: fadeUp 0.4s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.photo-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #f0eaf6;
  margin-bottom: 1.5rem;
}

.photo-preview-wrap { flex-shrink: 0; }

.photo-preview {
  width: 90px; height: 90px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e85d75;
}

.photo-placeholder {
  width: 90px; height: 90px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-upload {
  display: inline-block;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  font-weight: 500;
  color: #e85d75;
  border: 1.5px solid #e85d75;
  padding: 0.5rem 1.1rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-upload:hover { background: #e85d75; color: white; }

.hidden-input { display: none; }

.photo-hint {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: #b0a0c0;
  margin: 0.4rem 0 0;
}

.form-section {
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #f0eaf6;
}

.form-section:last-of-type { border-bottom: none; }

.form-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  color: #1a1025;
  margin: 0 0 1rem;
}

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 0.75rem; }

.field-group { display: flex; flex-direction: column; gap: 0.35rem; margin-bottom: 0.75rem; }
.field-group:last-child { margin-bottom: 0; }

.field-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  font-weight: 500;
  color: #4a3f5c;
}

.field-input {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
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
  box-shadow: 0 0 0 3px rgba(232, 93, 117, 0.1);
}

.field-textarea { resize: vertical; min-height: 80px; }
.field-select { cursor: pointer; }

/* Interests */
.interests-input-row { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; }

.btn-add {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  font-weight: 500;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0 1.2rem;
  cursor: pointer;
  white-space: nowrap;
  transition: opacity 0.2s;
}

.btn-add:hover { opacity: 0.88; }

.interests-list { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.5rem; }

.interest-tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  background: rgba(232, 93, 117, 0.08);
  color: #e85d75;
  padding: 0.3rem 0.6rem 0.3rem 0.8rem;
  border-radius: 20px;
  border: 1px solid rgba(232, 93, 117, 0.15);
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.remove-interest {
  background: none;
  border: none;
  color: #e85d75;
  font-size: 1rem;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  opacity: 0.7;
}

.remove-interest:hover { opacity: 1; }

.hint-text {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: #b0a0c0;
  margin: 0;
}

/* Toggle */
.toggle-row { display: flex; align-items: center; gap: 1rem; cursor: pointer; margin-bottom: 0.4rem; }

.toggle-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: #4a3f5c;
}

.toggle-switch {
  width: 44px; height: 24px;
  background: #e0d8ec;
  border-radius: 12px;
  position: relative;
  transition: background 0.2s;
  flex-shrink: 0;
}

.toggle-switch.on { background: #e85d75; }

.toggle-knob {
  position: absolute;
  width: 18px; height: 18px;
  border-radius: 50%;
  background: white;
  top: 3px; left: 3px;
  transition: left 0.2s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.15);
}

.toggle-switch.on .toggle-knob { left: 23px; }

/* Alerts */
.alert-error, .alert-success {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.75rem;
}

.alert-error {
  background: rgba(232, 93, 117, 0.08);
  color: #c0384d;
  border: 1px solid rgba(232, 93, 117, 0.2);
}

.alert-success {
  background: rgba(52, 199, 89, 0.08);
  color: #1a7a36;
  border: 1px solid rgba(52, 199, 89, 0.2);
}

/* Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #f0eaf6;
  margin-top: 0.75rem;
}

.btn-cancel {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: #8b7fa0;
  text-decoration: none;
  padding: 0.7rem 1.2rem;
  border-radius: 10px;
  transition: background 0.2s;
}

.btn-cancel:hover { background: #f5eff8; }

.btn-save {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  font-size: 0.95rem;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.75rem;
  cursor: pointer;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-save:hover:not(:disabled) { opacity: 0.9; }
.btn-save:disabled { opacity: 0.65; cursor: not-allowed; }

.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 520px) {
  .form-row { grid-template-columns: 1fr; }
  .photo-section { flex-direction: column; align-items: flex-start; }
}
</style>