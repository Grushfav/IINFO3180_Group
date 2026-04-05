<template>
  <div class="auth-page">
    <div class="auth-container">
      <h2>Sign Up</h2>
      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" class="form-control" required />
        </div>
        <div class="form-group">
          <label>Username</label>
          <input v-model="username" type="text" class="form-control" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label>Confirm Password</label>
          <input
            v-model="confirmPassword"
            type="password"
            class="form-control"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary">Sign Up</button>
      </form>
      <p>
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
// import axios from "axios";
import { useRouter } from "vue-router";

const email = ref("");
const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const router = useRouter();

const handleSignup = async () => {
  if (password.value !== confirmPassword.value) {
    alert("Passwords do not match");
    return;
  }
  try {
    const response = await axios.post("/signup", {
      email: email.value,
      username: username.value,
      password: password.value,
    });
    if (response.data.success) {
      router.push("/login");
    } else {
      alert(response.data.message || "Signup failed");
    }
  } catch (err) {
    alert("Error signing up");
  }
};
</script>

<style scoped>
/* Reuse the same styles as Login.vue */
.auth-page {
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.auth-container {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.form-group {
  margin-bottom: 1rem;
}
.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: #6a11cb;
  border: none;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}
.btn-primary:hover {
  background: #2575fc;
}
</style>
