<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">LoveLink</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link to="/dashboard" class="nav-link"
                >Dashboard</router-link
              >
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link to="/profile" class="nav-link">Profile</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/about">About</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/signup" class="nav-link">Sign Up</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <button
                @click="handleLogout"
                class="btn btn-outline-light nav-link"
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const isLoggedIn = ref(false);

const checkAuthStatus = async () => {
  try {
    // Simple check - try to access a protected endpoint
    await axios.get("/api/profile");
    isLoggedIn.value = true;
  } catch (err) {
    isLoggedIn.value = false;
  }
};

const handleLogout = async () => {
  try {
    await axios.post("/api/logout");
    isLoggedIn.value = false;
    router.push("/");
  } catch (err) {
    console.error("Logout failed:", err);
  }
};

onMounted(() => {
  checkAuthStatus();
});
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
}

.nav-link {
  cursor: pointer;
}

.btn-outline-light {
  border-color: rgba(255, 255, 255, 0.5);
  color: white;
}

.btn-outline-light:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: white;
}
</style>
