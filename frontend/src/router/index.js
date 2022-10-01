import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/Login.vue'
import StaffMain from '../views/StaffMain.vue'
import HrMain from '../views/HrMain.vue'

import Skill from '../views/Skill.vue'
import JobRole from '../views/JobRole.vue'

const routes = [
  {
    path: "/",
    name: "LoginPage",
    component: LoginPage,
    meta: {
      title: "LoginPage",
      requiresAuth: false,
    }
  },

  {
    path: "/StaffMain",
    name: "StaffMain",
    component: StaffMain,
    meta: {
      title: "StaffMain",
      requiresAuth: true,
    }
  },

  {
    path: "/HrMain",
    name: "HrMain",
    component: HrMain,
    meta: {
      title: "HrMain",
      requiresAuth: true,
    }
  },
  {
    path: "/Skill",
    name: "Skill",
    component: Skill,
    meta: {
      title: "Skill",
      requiresAuth: true,
    }
  },

  {
    path: "/JobRole",
    name: "JobRole",
    component: JobRole,
    meta: {
      title: "JobRole",
      requiresAuth: true,
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
