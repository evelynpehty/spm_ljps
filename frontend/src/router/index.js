import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/Login.vue'
import StaffMain from '../views/StaffMain.vue'
import HrMain from '../views/HrMain.vue'

import CreateSkills from '../views/Skills/CreateSkills.vue'
import ViewAllSkills from '../views/Skills/ViewAllSkills.vue'

import CreateJobs from '../views/JobRoles/CreateJobs.vue'
import ViewAllJobs from '../views/JobRoles/ViewAllJobs.vue'
import UpdateJobRole from '../views/JobRoles/UpdateJobRole.vue'

import SelectJobRole from '../views/LearningJourney/SelectJobRoles.vue'
import CreateLearningJourney from '../views/LearningJourney/CreateLearningJourney.vue'
import ManageLearningJourney from '../views/LearningJourney/ManageAllLearningJourney.vue'

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
      title: "Homepage",
      requiresAuth: true,
    }
  },

  {
    path: "/HrMain",
    name: "HrMain",
    component: HrMain,
    meta: {
      title: "Homepage",
      requiresAuth: true,
    }
  },

  {
    path: "/create-skills",
    name: "CreateSkills",
    component: CreateSkills,
    meta: {
      title: "Create Skills",
      requiresAuth: true,
    }
  },

  {
    path: "/view-all-skills",
    name: "ViewAllSkills",
    component: ViewAllSkills,
    meta: {
      title: "View All Skills",
      requiresAuth: true,
    }
  },

  {
    path: "/create-jobs",
    name: "CreateJobs",
    component: CreateJobs,
    meta: {
      title: "Create Jobs",
      requiresAuth: true,
    }
  },

  {
    path: "/view-all-jobs",
    name: "ViewAllJobs",
    component: ViewAllJobs,
    meta: {
      title: "View All Jobs",
      requiresAuth: true,
    }
  },


  {
    path: "/select-job-role",
    name: "SelectJobRole",
    component: SelectJobRole,
    meta: {
      title: "Select Job Role",
      requiresAuth: true,
    }
  },
  {
    path: "/create-learning-journey/:jobroleid",
    name: "CreateLearningJourney",
    component: CreateLearningJourney,
    meta: {
      title: "CreateLearningJourney",
      requiresAuth: true,
    },
  },

  {
    path: "/manage-learning-journey",
    name: "ManageLearningJourney",
    component: ManageLearningJourney,
    meta: {
      title: "Manage Learning Journey",
      requiresAuth: true,
    }
  },

  {
    path: "/update-job-role/:jobroleid",
    name: "UpdateJobRole",
    component: UpdateJobRole,
    meta: {
      title: "UpdateJobRole",
      requiresAuth: true,
    },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
