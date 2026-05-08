<template>
  <div class="dashboard">
    <AppHeader />
    <div class="dashboard-content">
      <div class="container">
        <h1>Welcome to LoveLink!</h1>
        <div class="dashboard-grid">
          <div class="card">
            <h3>My Profile</h3>
            <p>Complete your profile to find better matches</p>
            <router-link to="/profile" class="btn btn-primary"
              >Edit Profile</router-link
            >
          </div>
          <div class="card">
            <h3>Find Matches</h3>
            <p>Discover people who match your preferences</p>
            <router-link to="/matches" class="btn btn-secondary"
              >Browse Matches</router-link
            >
          </div>
          <div class="card">
            <h3>Messages</h3>
            <p>Chat with your matches</p>
            <router-link to="/messages" class="btn btn-secondary"
              >View Messages</router-link
            >
          </div>
          <div class="card">
            <h3>Settings</h3>
            <p>Manage your account and preferences</p>
            <router-link to="/settings" class="btn btn-secondary"
              >Account Settings</router-link
            >
          </div>
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from "../components/AppHeader.vue";
import AppFooter from "../components/AppFooter.vue";
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.dashboard-content {
  flex: 1;
  padding: 2rem 0;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.card h3 {
  margin-bottom: 0.5rem;
  color: #333;
}

.card p {
  color: #666;
  margin-bottom: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}
</style>
