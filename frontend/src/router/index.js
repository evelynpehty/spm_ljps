import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/Login.vue'
import StaffMain from '../views/StaffMain.vue'
import HrMain from '../views/HrMain.vue'

import CreateSkills from '../views/Skills/CreateSkills.vue'
import ViewAllSkills from '../views/Skills/ViewAllSkills.vue'
import ViewSkillDetails from '../views/Skills/ViewSkillDetails.vue'
import UpdateSkill from '../views/Skills/UpdateSkills.vue'

import CreateJobs from '../views/JobRoles/CreateJobs.vue'
import ViewAllJobs from '../views/JobRoles/ViewAllJobs.vue'
import ViewJobDetails from '../views/JobRoles/ViewJobDetails.vue'
import UpdateJobRole from '../views/JobRoles/UpdateJobRole.vue'

import SelectJobRole from '../views/LearningJourney/SelectJobRoles.vue'
import CreateLearningJourney from '../views/LearningJourney/CreateLearningJourney.vue'
import ViewLearningJourney from '../views/LearningJourney/ViewAllLearningJourney.vue'
import ViewLJDetails from '../views/LearningJourney/ViewLJDetails.vue'
import UpdateLearningJourney from '../views/LearningJourney/UpdateLearningJourney.vue'

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
    path: "/view-all-skills/",
    name: "ViewAllSkills",
    component: ViewAllSkills,
    meta: {
      title: "View All Skills",
      requiresAuth: true,
    }
  },

  {
    path: "/view-skill-details/:skillID",
    name: "ViewSkillDetails",
    component: ViewSkillDetails,
    meta: {
      title: "View Skill Details",
      requiresAuth: true,
    }
  },

  {
    path: "/update-skill/:skillID",
    name: "UpdateSkill",
    component: UpdateSkill,
    meta: {
      title: "Update Skill",
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
    path: "/view-learning-journey",
    name: "ViewLearningJourney",
    component: ViewLearningJourney,
    meta: {
      title: "View Learning Journey",
      requiresAuth: true,
    }
  },

  {
    path: "/view-learning-journey/:learningjourneyid",
    name: "ViewLJDetails",
    component: ViewLJDetails,
    meta: {
      title: "CreateLeViewLJDetailsarningJourney",
      requiresAuth: true,
    },
  },

  {
    path: "/update-learning-journey/:learningjourneyid",
    name: "UpdateLearningJourney",
    component: UpdateLearningJourney,
    meta: {
      title: "UpdateLearningJourney",
      requiresAuth: true,
    },
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

  {
    path: "/view-job-details/:jobroleid",
    name: "ViewJobDetails",
    component: ViewJobDetails,
    meta: {
      title: "ViewJobDetails",
      requiresAuth: true,
    },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
