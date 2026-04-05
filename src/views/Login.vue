<template>
  <div class="auth-page">
    <div class="auth-container">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
      <p>
        Don’t have an account?
        <router-link to="/signup">Sign up here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
// import axios from "axios";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const router = useRouter();

const handleLogin = async () => {
  try {
    const response = await axios.post("http://localhost:8080/login", {
      email: email.value,
      password: password.value,
    });
    if (response.data.success) {
      router.push("/dashboard");
    } else {
      alert(response.data.message || "Login failed");
    }
  } catch (err) {
    alert("Error logging in");
  }
};
</script>

<style scoped>
.auth-page {
  background: linear-gradient(135deg, #ff5f6d 0%, #ffc371 100%);
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
  background: #ff5f6d;
  border: none;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}
.btn-primary:hover {
  background: #ffc371;
}
</style>
