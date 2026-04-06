import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/edit',
      name: 'edit-profile',
      component: () => import('../views/EditProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/matches',
      name: 'matches',
      component: () => import('../views/MatchesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/messages',
      name: 'messages',
      component: () => import('../views/MessagesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.user) {
    next({ name: 'login' })
  } else if ((to.name === 'login' || to.name === 'register') && auth.user) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
