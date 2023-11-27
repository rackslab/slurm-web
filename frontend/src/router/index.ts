import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRuntimeStore } from '@/stores/runtime'
import DashboardView from '@/views/DashboardView.vue'
import LoginView from '@/views/LoginView.vue'
import SignoutView from '@/views/SignoutView.vue'
import JobsView from '@/views/JobsView.vue'
import ResourcesView from '@/views/ResourcesView.vue'
import ClustersView from '@/views/ClustersView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/clusters',
      name: 'clusters',
      component: ClustersView
    },
    {
      path: '/signout',
      name: 'signout',
      component: SignoutView
    },
    {
      path: '/:cluster/dashboard',
      name: 'dashboard',
      component: DashboardView,
      props: true
    },
    {
      path: '/:cluster/jobs/',
      name: 'jobs',
      component: JobsView,
      props: true
    },
    {
      path: '/:cluster/resources',
      name: 'resources',
      component: ResourcesView,
      props: true
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
