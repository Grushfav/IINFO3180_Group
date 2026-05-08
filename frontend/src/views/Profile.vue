<template>
  <div class="profile-page">
    <AppHeader />
    <div class="profile-content">
      <div class="container">
        <h1>My Profile</h1>
        <div class="profile-form-container">
          <form @submit.prevent="handleSubmit" class="profile-form">
            <div class="form-row">
              <div class="form-group">
                <label>First Name</label>
                <input v-model="profile.first_name" type="text" required />
              </div>
              <div class="form-group">
                <label>Last Name</label>
                <input v-model="profile.last_name" type="text" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Date of Birth</label>
                <input v-model="profile.date_of_birth" type="date" required />
              </div>
              <div class="form-group">
                <label>Gender</label>
                <select v-model="profile.gender" required>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>Bio</label>
              <textarea
                v-model="profile.bio"
                rows="4"
                placeholder="Tell us about yourself..."
              ></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Location</label>
                <input v-model="profile.location" type="text" />
              </div>
              <div class="form-group">
                <label>Occupation</label>
                <input v-model="profile.occupation" type="text" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Education Level</label>
                <input v-model="profile.education_level" type="text" />
              </div>
              <div class="form-group">
                <label>Relationship Goal</label>
                <input v-model="profile.relationship_goal" type="text" />
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? "Saving..." : "Save Profile" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import AppHeader from "../components/AppHeader.vue";
import AppFooter from "../components/AppFooter.vue";
import api from "../services/api";

const router = useRouter();
const loading = ref(false);
const profile = ref({
  first_name: "",
  last_name: "",
  date_of_birth: "",
  gender: "",
  bio: "",
  location: "",
  occupation: "",
  education_level: "",
  relationship_goal: "",
});

const loadProfile = async () => {
  try {
    const response = await api.get("/api/profile");
    profile.value = response.data;
  } catch (err) {
    console.error("Failed to load profile:", err);
    // If not authenticated, redirect to login
    if (err.response?.status === 401) {
      router.push("/login");
    }
  }
};

const handleSubmit = async () => {
  loading.value = true;
  try {
    await api.post("/api/profile", profile.value);
    alert("Profile updated successfully!");
  } catch (err) {
    if (err.response?.data?.errors) {
      alert("Validation errors: " + JSON.stringify(err.response.data.errors));
    } else {
      alert("Failed to update profile");
    }
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadProfile();
});
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.profile-content {
  flex: 1;
  padding: 2rem 0;
  background: #f8f9fa;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.profile-form-container {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
