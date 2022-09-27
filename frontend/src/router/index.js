import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'

const routes = [
  {
    path: "/",
    name: "LoginPage",
    component: Login,
    meta: {
      title: "LoginPage",
      requiresAuth: false,
    },
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
