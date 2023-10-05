import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRuntimeStore } from '@/stores/runtime'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignoutView from '@/views/SignoutView.vue'
import JobsView from '@/views/JobsView.vue'
import ResourcesView from '@/views/ResourcesView.vue'
import { runtimeConfiguration } from '@/plugins/runtimeConfiguration'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signout',
      name: 'signout',
      component: SignoutView
    },
    {
      path: '/jobs',
      name: 'jobs',
      component: JobsView
    },
    {
      path: '/resources',
      name: 'resources',
      component: ResourcesView
    }
  ]
})

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login']
  const authRequired = !publicPages.includes(to.path)
  const auth = useAuthStore()
  const runtime = useRuntimeStore()
  if (authRequired && !auth.token) {
    auth.returnUrl = to.fullPath
    return '/login'
  }
  runtime.navigation = to.name as string
})

export default router
