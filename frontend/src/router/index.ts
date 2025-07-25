import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/Home.vue'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Profile from '@/components/Profile.vue'
import SkillTree from '@/components/SkillTree.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home', 
      component: HomeView,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      meta: { requiresAuth: true }, // Protect this route
    },
    {
      path: '/skills',
      name: 'SkillTree',
      component: SkillTree,
    }
  ],
})

export default router
