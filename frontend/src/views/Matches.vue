<template>
  <div class="matches-page">
    <AppHeader />
    <div class="matches-content">
      <div class="container">
        <h1>Find Your Match</h1>
        <div class="matches-grid">
          <div class="match-card" v-for="match in matches" :key="match.id">
            <div class="match-photo">
              <img
                :src="match.photo || '/static/default-avatar.png'"
                :alt="match.name"
              />
            </div>
            <div class="match-info">
              <h3>{{ match.name }}</h3>
              <p>{{ match.age }} years old</p>
              <p>{{ match.location }}</p>
              <p class="bio">{{ match.bio }}</p>
            </div>
            <div class="match-actions">
              <button @click="likeMatch(match.id)" class="btn btn-success">
                Like
              </button>
              <button @click="passMatch(match.id)" class="btn btn-secondary">
                Pass
              </button>
            </div>
          </div>
        </div>
        <div v-if="matches.length === 0" class="no-matches">
          <p>No matches found. Try updating your preferences!</p>
          <router-link to="/profile" class="btn btn-primary"
            >Update Profile</router-link
          >
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import AppHeader from "../components/AppHeader.vue";
import AppFooter from "../components/AppFooter.vue";

const router = useRouter();
const matches = ref([]);

// Mock data for now - replace with actual API call
const loadMatches = async () => {
  try {
    // TODO: Replace with actual matches API
    // const response = await axios.get('/api/matches')
    // matches.value = response.data

    // Mock data
    matches.value = [
      {
        id: 1,
        name: "Sarah Johnson",
        age: 28,
        location: "New York",
        bio: "Love hiking and trying new restaurants!",
        photo: null,
      },
      {
        id: 2,
        name: "Mike Chen",
        age: 32,
        location: "San Francisco",
        bio: "Tech enthusiast and coffee lover.",
        photo: null,
      },
    ];
  } catch (err) {
    console.error("Failed to load matches:", err);
    if (err.response?.status === 401) {
      router.push("/login");
    }
  }
};

const likeMatch = async (matchId) => {
  try {
    // TODO: Implement like functionality
    // await axios.post(`/api/matches/${matchId}/like`)
    alert("Liked! (Feature coming soon)");
  } catch (err) {
    console.error("Failed to like match:", err);
  }
};

const passMatch = async (matchId) => {
  try {
    // TODO: Implement pass functionality
    matches.value = matches.value.filter((match) => match.id !== matchId);
  } catch (err) {
    console.error("Failed to pass match:", err);
  }
};

onMounted(() => {
  loadMatches();
});
</script>

<style scoped>
.matches-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.matches-content {
  flex: 1;
  padding: 2rem 0;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.match-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.match-card:hover {
  transform: translateY(-5px);
}

.match-photo {
  height: 200px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.match-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.match-info {
  padding: 1rem;
}

.match-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.match-info p {
  margin: 0.25rem 0;
  color: #666;
}

.bio {
  font-style: italic;
  margin-top: 0.5rem !important;
}

.match-actions {
  padding: 1rem;
  display: flex;
  gap: 0.5rem;
}

.btn {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.no-matches {
  text-align: center;
  margin-top: 3rem;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.no-matches p {
  margin-bottom: 1rem;
  color: #666;
}
</style>
