import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/Home.vue";
import Login from "../views/Login.vue";
import Signup from "../views/Signup.vue";
import Dashboard from "../views/Dashboard.vue";
import Profile from "../views/Profile.vue";
import Matches from "../views/Matches.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
    },
    { path: "/login", name: "Login", component: Login },
    { path: "/signup", name: "Signup", component: Signup },
    { path: "/dashboard", name: "Dashboard", component: Dashboard },
    { path: "/profile", name: "Profile", component: Profile },
    { path: "/matches", name: "Matches", component: Matches },
  ],
});

export default router;
