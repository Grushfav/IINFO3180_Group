<template>
  <div class="about-page">
    <div class="about-container">
      <div class="about-hero">
        <div class="about-logo">🌊</div>
        <h1 class="about-title">About DriftDater</h1>
        <p class="about-lead">
          A dating platform built with Vue 3 + Flask, designed for the INFO3180 group project.
          DriftDater helps people discover meaningful connections based on shared interests,
          location, and genuine compatibility.
        </p>
      </div>

      <div class="about-features">
        <div class="feature-card">
          <span class="feature-icon">❤️</span>
          <h3>Smart Matching</h3>
          <p>Our algorithm surfaces profiles that align with your interests, age preferences, and location.</p>
        </div>
        <div class="feature-card">
          <span class="feature-icon">💬</span>
          <h3>Real Conversations</h3>
          <p>Message your mutual matches directly — no waiting, just connecting.</p>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🔍</span>
          <h3>Discover People</h3>
          <p>Browse and filter profiles by location, age, gender, and shared interests.</p>
        </div>
      </div>

      <div class="tech-stack">
        <h2 class="tech-title">Built With</h2>
        <div class="tech-chips">
          <span class="tech-chip">Vue 3</span>
          <span class="tech-chip">Pinia</span>
          <span class="tech-chip">Vue Router</span>
          <span class="tech-chip">Flask</span>
          <span class="tech-chip">SQLAlchemy</span>
          <span class="tech-chip">Axios</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

.about-page {
  min-height: 100vh;
  background: #fff5f0;
  padding: 5rem 1.5rem 3rem;
}

.about-container {
  max-width: 760px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.about-hero { text-align: center; }

.about-logo { font-size: 3.5rem; margin-bottom: 1rem; }

.about-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  color: #1a1025;
  margin: 0 0 1.25rem;
  letter-spacing: -0.03em;
}

.about-lead {
  font-family: 'DM Sans', sans-serif;
  font-size: 1.05rem;
  color: #6b5f7a;
  line-height: 1.75;
  max-width: 560px;
  margin: 0 auto;
}

.about-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.25rem;
}

.feature-card {
  background: white;
  border-radius: 18px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  text-align: center;
  transition: transform 0.2s;
}

.feature-card:hover { transform: translateY(-4px); }

.feature-icon { font-size: 2rem; display: block; margin-bottom: 0.75rem; }

.feature-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.1rem;
  color: #1a1025;
  margin: 0 0 0.5rem;
}

.feature-card p {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  color: #6b5f7a;
  margin: 0;
  line-height: 1.6;
}

.tech-stack { text-align: center; }

.tech-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  color: #1a1025;
  margin: 0 0 1rem;
}

.tech-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; }

.tech-chip {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  background: white;
  border: 1.5px solid rgba(232, 93, 117, 0.3);
  color: #e85d75;
  padding: 0.4rem 1rem;
  border-radius: 20px;
}
</style>