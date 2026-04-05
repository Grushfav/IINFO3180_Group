<template>
  <div class="home-page">
    <header class="hero">
      <h1>Welcome to LoveConnect</h1>
      <p>
        Find meaningful connections, meet new people, and start your journey
        today.
      </p>
      <div class="hero-buttons">
        <router-link to="/login" class="btn btn-primary">Login</router-link>
        <router-link to="/signup" class="btn btn-secondary"
          >Sign Up</router-link
        >
      </div>
    </header>

    <section class="features">
      <div class="feature">
        <h3>Discover Matches</h3>
        <p>Swipe, like, and connect with people who share your interests.</p>
      </div>
      <div class="feature">
        <h3>Chat Securely</h3>
        <p>
          Message your matches in real time with privacy and security built in.
        </p>
      </div>
      <div class="feature">
        <h3>Personalize Your Profile</h3>
        <p>Show off your personality with photos, bios, and interests.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
// Static landing page for now.
// Later you can fetch featured profiles or stats from Flask API.
</script>

<style scoped>
.home-page {
  font-family: "Segoe UI", sans-serif;
  color: #333;
}

.hero {
  background: linear-gradient(135deg, #ff5f6d 0%, #ffc371 100%);
  color: #fff;
  text-align: center;
  padding: 4rem 2rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
}

.btn-primary {
  background: #ff5f6d;
  color: #fff;
}

.btn-secondary {
  background: #ffc371;
  color: #fff;
}

.features {
  display: flex;
  justify-content: space-around;
  padding: 3rem 2rem;
  background: #f9f9f9;
}

.feature {
  max-width: 250px;
  text-align: center;
}

.feature h3 {
  color: #ff5f6d;
  margin-bottom: 0.5rem;
}
</style>
