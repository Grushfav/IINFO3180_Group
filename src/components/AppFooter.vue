<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <img src="/src/assets/logo.png" alt="DriftDater" class="brand-icon">
      <span class="footer-copy">© 2026 DriftDater · INFO3180 Group Project</span>
    </div>
  </footer>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400&display=swap');

.app-footer {
  background: #1a1025;
  color: rgba(255,255,255,0.4);
  padding: 1.2rem 2rem;
  margin-top: auto;
}

.brand-icon {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.82rem;
}

.footer-brand {
  color: rgba(255,255,255,0.7);
  font-weight: 500;
  letter-spacing: 0.02em;
}

@media (max-width: 600px) {
  .footer-inner { flex-direction: column; gap: 0.4rem; text-align: center; }
}
</style>