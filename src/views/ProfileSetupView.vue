<template>
  <div class="setup-page">
    <div class="setup-shell">
      <div class="setup-progress">
        <div class="progress-dots">
          <button
            v-for="(_, i) in steps"
            :key="i"
            type="button"
            class="progress-dot"
            :class="{ active: i === stepIndex }"
            :disabled="i > stepIndex"
            @click="stepIndex = i"
            aria-label="Step"
          />
        </div>
        <div class="progress-label">
          {{ steps[stepIndex].title }}
        </div>
      </div>

      <div class="setup-card">
        <!-- Step 0: Welcome -->
        <section v-if="stepIndex === 0" class="step">
          <h2 class="setup-title">Welcome to DriftDater</h2>
          <p class="setup-subtitle">
            Let’s set you up so you get better matches from the start.
          </p>

          <div class="step-actions">
            <button type="button" class="btn-ghost" @click="skipForNow">
              Skip for now
            </button>
            <button type="button" class="btn-primary" @click="stepIndex = 1">
              Start
            </button>
          </div>
        </section>

        <!-- Step 1: Photo & Bio -->
        <section v-else-if="stepIndex === 1" class="step">
          <h2 class="setup-title">Photo & Bio</h2>
          <p class="setup-subtitle">
            Add a photo and a short bio so people can know you better.
          </p>

          <div class="field-group">
            <div class="photo-preview">
              <img
                v-if="previewPhoto || form.photo"
                :src="previewPhoto || form.photo"
                alt="Profile preview"
              />
              <div v-else class="photo-placeholder">{{ initials }}</div>
            </div>

            <label class="btn-upload" for="setup-photo">Upload photo</label>
            <input
              id="setup-photo"
              type="file"
              accept="image/*"
              class="hidden-input"
              @change="handlePhotoChange"
            />
          </div>

          <div class="field-group">
            <label class="field-label">Bio</label>
            <textarea
              v-model="form.bio"
              class="field-input field-textarea"
              rows="4"
              placeholder="Tell people what makes you, you..."
            />
          </div>

          <div class="step-actions">
            <button type="button" class="btn-ghost" @click="skipForNow">
              Skip for now
            </button>
            <button type="button" class="btn-ghost" @click="stepIndex = 2">
              Skip set parts
            </button>
            <button type="button" class="btn-primary" @click="stepIndex = 2">
              Next
            </button>
          </div>
        </section>

        <!-- Step 2: Location & Interests -->
        <section v-else-if="stepIndex === 2" class="step">
          <h2 class="setup-title">Location & Interests</h2>
          <p class="setup-subtitle">
            Pick your location and add at least 3 interests.
          </p>

          <div class="field-group">
            <label class="field-label">Location</label>
            <select v-model="form.location" class="field-input field-select">
              <option value="">Select parish</option>
              <option v-for="p in JAMAICAN_PARISHES" :key="p" :value="p">
                {{ p }}
              </option>
            </select>
          </div>

          <div class="field-group">
            <label class="field-label">Interests</label>
            <div class="interest-input-row">
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

            <p v-if="form.includeInterests !== false && form.interests.length < 3" class="hint-text">
              Add at least {{ 3 - form.interests.length }} more interest(s), or use “Skip set parts”.
            </p>
          </div>

          <div class="step-actions">
            <button type="button" class="btn-ghost" @click="skipForNow">
              Skip for now
            </button>
            <button
              type="button"
              class="btn-ghost"
              @click="skipInterestsStep"
            >
              Skip set parts
            </button>
            <button
              type="button"
              class="btn-primary"
              :disabled="form.includeInterests !== false && form.interests.length < 3"
              @click="stepIndex = 3"
            >
              Next
            </button>
          </div>
        </section>

        <!-- Step 3: Details -->
        <section v-else-if="stepIndex === 3" class="step">
          <h2 class="setup-title">Details</h2>
          <p class="setup-subtitle">
            Finish setting your preferences to get better matches.
          </p>

          <div class="field-group">
            <label class="field-label">Gender</label>
            <select v-model="form.gender" class="field-input field-select">
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div class="field-group">
            <label class="field-label">Looking For</label>
            <select v-model="form.lookingFor" class="field-input field-select">
              <option value="any">Any</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div class="form-row">
            <div class="field-group">
              <label class="field-label">Date of Birth</label>
              <input v-model="form.dateOfBirth" type="date" class="field-input" />
            </div>
            <div class="field-group">
              <label class="field-label">Max Distance (km)</label>
              <input
                v-model.number="form.maxDistanceKm"
                type="number"
                min="1"
                max="500"
                class="field-input"
              />
            </div>
          </div>

          <div class="field-group">
            <label class="field-label">Relationship Goal</label>
            <input
              v-model="form.relationshipGoal"
              type="text"
              class="field-input"
              placeholder="e.g. long-term"
            />
          </div>

          <div class="form-row">
            <div class="field-group">
              <label class="field-label">Preferred Min Age</label>
              <input
                v-model.number="form.preferredMinAge"
                type="number"
                min="18"
                max="99"
                class="field-input"
              />
            </div>
            <div class="field-group">
              <label class="field-label">Preferred Max Age</label>
              <input
                v-model.number="form.preferredMaxAge"
                type="number"
                min="18"
                max="99"
                class="field-input"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="field-group">
              <label class="field-label">Occupation</label>
              <input v-model="form.occupation" type="text" class="field-input" />
            </div>
            <div class="field-group">
              <label class="field-label">Education Level</label>
              <input v-model="form.educationLevel" type="text" class="field-input" />
            </div>
          </div>

          <div v-if="submitError" class="alert-error">{{ submitError }}</div>

          <div class="step-actions">
            <button type="button" class="btn-ghost" @click="skipForNow">
              Skip for now
            </button>
            <button
              type="button"
              class="btn-ghost"
              @click="finishWithSkip"
              :disabled="loading"
            >
              Skip set parts
            </button>
            <button
              type="button"
              class="btn-primary"
              :disabled="loading || (form.includeInterests !== false && form.interests.length < 3)"
              @click="finish"
            >
              <span v-if="loading" class="spinner"></span>
              <span v-else>Finish</span>
            </button>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { JAMAICAN_PARISHES } from '../data/jamaicanParishes'
import { useAuthStore } from '../stores/auth'
import { useProfileStore } from '../stores/profile'

const router = useRouter()
const auth = useAuthStore()
const profileStore = useProfileStore()

const steps = [
  { key: 'welcome', title: 'Welcome' },
  { key: 'photo', title: 'Photo & Bio' },
  { key: 'location', title: 'Location & Interests' },
  { key: 'details', title: 'Details' },
]

const stepIndex = ref(0)
const loading = ref(false)
const submitError = ref('')

const photoFile = ref(null)
const previewPhoto = ref('')
const newInterest = ref('')

const form = ref({
  includeInterests: true,
  firstName: '',
  lastName: '',
  bio: '',
  photo: '',
  location: '',
  dateOfBirth: '',
  gender: '',
  lookingFor: 'any',
  relationshipGoal: '',
  preferredMinAge: 18,
  preferredMaxAge: 60,
  maxDistanceKm: 50,
  occupation: '',
  educationLevel: '',
  interests: [],
  latitude: null,
  longitude: null,
  isPublic: true,
})

const initials = computed(() => {
  return `${form.value.firstName?.[0] || ''}${form.value.lastName?.[0] || ''}`.toUpperCase() || '?'
})

function handlePhotoChange(e) {
  const file = e.target.files?.[0]
  if (!file) return
  photoFile.value = file
  previewPhoto.value = URL.createObjectURL(file)
  // Keep existing field for UI; upload happens at finish.
}

function addInterest() {
  const val = newInterest.value.trim().toLowerCase()
  if (!val) return
  if (form.value.interests.includes(val)) return
  form.value.interests.push(val)
  newInterest.value = ''
}

function removeInterest(interest) {
  form.value.interests = form.value.interests.filter(i => i !== interest)
}

function skipForNow() {
  router.push('/')
}

function skipInterestsStep() {
  // Omit interests from the payload so the backend doesn't enforce the "min 3 interests" constraint.
  form.value.includeInterests = false
  form.value.interests = []
  stepIndex.value = 3
}

async function finishWithSkip() {
  // "Skip details" means: complete setup without enforcing the interests constraint.
  // We omit interests from the update payload so the backend won't require >= 3 interests.
  form.value.includeInterests = false
  form.value.interests = []
  await finish()
}

async function finish() {
  submitError.value = ''
  loading.value = true
  try {
    if (!form.value.firstName || !form.value.lastName) {
      submitError.value = 'First and last name are required.'
      return
    }
    if (!form.value.dateOfBirth) {
      submitError.value = 'Date of birth is required.'
      return
    }
    if (!form.value.gender) {
      submitError.value = 'Gender is required.'
      return
    }
    if (
      form.value.includeInterests !== false &&
      Array.isArray(form.value.interests) &&
      form.value.interests.length < 3
    ) {
      submitError.value = 'Please add at least 3 interests, or use “Skip this step”.'
      return
    }

    await profileStore.updateProfile(form.value)
    if (photoFile.value) {
      await profileStore.uploadProfilePicture(photoFile.value)
    }
    router.push('/')
  } catch (e) {
    submitError.value = profileStore.error || 'Failed to complete setup. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const u = auth.user
  if (!u) return

  // Initialize step form with current profile values.
  form.value.firstName = u.firstName || ''
  form.value.lastName = u.lastName || ''
  form.value.bio = u.bio || ''
  form.value.photo = u.photo || ''
  form.value.location = u.location || ''
  form.value.dateOfBirth = u.dateOfBirth || ''
  form.value.gender = u.gender || ''
  form.value.lookingFor = u.lookingFor || 'any'
  form.value.relationshipGoal = u.relationshipGoal || ''
  form.value.preferredMinAge = u.preferredMinAge ?? 18
  form.value.preferredMaxAge = u.preferredMaxAge ?? 60
  form.value.maxDistanceKm = u.maxDistanceKm ?? 50
  form.value.occupation = u.occupation || ''
  form.value.educationLevel = u.educationLevel || ''
  form.value.interests = Array.isArray(u.interests) ? [...u.interests] : []
  form.value.latitude = u.latitude ?? null
  form.value.longitude = u.longitude ?? null
  form.value.isPublic = u.isPublic !== false

  // If the user somehow already has 3+ interests, allow finishing without forcing skip.
  form.value.includeInterests = true
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

.setup-page {
  min-height: 100vh;
  background: #fff5f0;
  padding: 5rem 1.25rem 3rem;
}

.setup-shell {
  max-width: 720px;
  margin: 0 auto;
}

.setup-progress {
  text-align: center;
  margin-bottom: 1.25rem;
}

.progress-dots {
  display: flex;
  justify-content: center;
  gap: 0.65rem;
  margin-bottom: 0.75rem;
}

.progress-dot {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  border: 1px solid rgba(232, 93, 117, 0.35);
  background: rgba(232, 93, 117, 0.06);
  cursor: pointer;
}

.progress-dot.active {
  background: linear-gradient(135deg, #e85d75, #f4845f);
  border-color: rgba(232, 93, 117, 0.45);
}

.progress-dot:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.progress-label {
  font-family: 'Playfair Display', serif;
  color: #1a1025;
  font-size: 1.25rem;
  margin: 0;
}

.setup-card {
  background: white;
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 4px 32px rgba(0, 0, 0, 0.06);
  animation: fadeUp 0.35s ease both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.step {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.setup-title {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  color: #1a1025;
  margin: 0;
}

.setup-subtitle {
  font-family: 'DM Sans', sans-serif;
  color: #8b7fa0;
  margin: 0;
  line-height: 1.5;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.85rem;
}

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
  background: #fdfbfe;
  color: #1a1025;
}

.field-input:focus {
  border-color: #e85d75;
  box-shadow: 0 0 0 3px rgba(232, 93, 117, 0.12);
}

.field-textarea {
  resize: vertical;
  min-height: 120px;
}

.field-select {
  cursor: pointer;
}

.photo-preview {
  width: 108px;
  height: 108px;
  border-radius: 50%;
  border: 3px solid #e85d75;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(232, 93, 117, 0.08), rgba(244, 132, 95, 0.06));
}

.photo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-placeholder {
  color: white;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Playfair Display', serif;
  font-size: 1.6rem;
  font-weight: 700;
}

.hidden-input { display: none; }

.btn-upload {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  color: #e85d75;
  border: 1.5px solid #e85d75;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  display: inline-flex;
  width: fit-content;
  cursor: pointer;
}

.btn-upload:hover {
  background: rgba(232, 93, 117, 0.06);
}

.interest-input-row {
  display: flex;
  gap: 0.6rem;
}

.btn-add {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0 1rem;
  cursor: pointer;
}

.btn-add:hover { opacity: 0.9; }

.interests-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.interest-tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  background: rgba(232, 93, 117, 0.08);
  color: #e85d75;
  padding: 0.35rem 0.65rem;
  border-radius: 999px;
  border: 1px solid rgba(232, 93, 117, 0.15);
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.remove-interest {
  background: none;
  border: none;
  color: #e85d75;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  opacity: 0.75;
}

.remove-interest:hover { opacity: 1; }

.hint-text {
  margin: 0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
  color: #b0a0c0;
}

.alert-error {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  background: rgba(232, 93, 117, 0.08);
  color: #c0384d;
  border: 1px solid rgba(232, 93, 117, 0.2);
  border-radius: 10px;
  padding: 0.75rem 1rem;
}

.step-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 0.75rem;
}

.btn-primary {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  font-size: 1rem;
  background: linear-gradient(135deg, #e85d75, #f4845f);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.85rem 1.25rem;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
}

.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn-ghost {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  color: #8b7fa0;
  border: 1.5px solid rgba(217, 208, 228, 0.9);
  background: transparent;
  padding: 0.75rem 1.05rem;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-ghost:hover {
  background: rgba(232, 93, 117, 0.06);
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.45);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 620px) {
  .form-row { grid-template-columns: 1fr; }
  .interest-input-row { flex-direction: column; }
  .btn-ghost, .btn-primary { width: 100%; }
  .step-actions { justify-content: stretch; }
}
</style>

