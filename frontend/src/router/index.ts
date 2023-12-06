import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRuntimeStore } from '@/stores/runtime'
import DashboardView from '@/views/DashboardView.vue'
import LoginView from '@/views/LoginView.vue'
import SignoutView from '@/views/SignoutView.vue'
import SettingsMainView from '@/views/settings/SettingsMain.vue'
import SettingsErrorsView from '@/views/settings/SettingsErrors.vue'
import SettingsAccountView from '@/views/settings/SettingsAccount.vue'
import ClustersView from '@/views/ClustersView.vue'
import JobsView from '@/views/JobsView.vue'
import ResourcesView from '@/views/ResourcesView.vue'
import QosView from '@/views/QosView.vue'
import ReservationsView from '@/views/ReservationsView.vue'
import AccountsView from '@/views/AccountsView.vue'
import ReportsView from '@/views/ReportsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: {
        name: 'clusters'
      }
    },
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
      path: '/settings',
      name: 'settings',
      component: SettingsMainView,
      meta: {
        settings: true
      }
    },
    {
      path: '/settings/errors',
      name: 'settings-errors',
      component: SettingsErrorsView,
      meta: {
        settings: true
      }
    },
    {
      path: '/settings/account',
      name: 'settings-account',
      component: SettingsAccountView,
      meta: {
        settings: true
      }
    },
    {
      path: '/:cluster/dashboard',
      name: 'dashboard',
      component: DashboardView,
      props: true
    },
    {
      path: '/:cluster/jobs',
      name: 'jobs',
      component: JobsView,
      props: true
    },
    {
      path: '/:cluster/resources',
      name: 'resources',
      component: ResourcesView,
      props: true
    },
    {
      path: '/:cluster/qos',
      name: 'qos',
      component: QosView,
      props: true
    },
    {
      path: '/:cluster/reservations',
      name: 'reservations',
      component: ReservationsView,
      props: true
    },
    {
      path: '/:cluster/accounts',
      name: 'accounts',
      component: AccountsView,
      props: true
    },
    {
      path: '/:cluster/reports',
      name: 'reports',
      component: ReportsView,
      props: true
    }
  ]
})

router.beforeEach(async (to, from) => {
  /* redirect to login page if not logged in and trying to access a restricted page */
  const publicPages = ['/login']
  const authRequired = !publicPages.includes(to.path)
  const auth = useAuthStore()
  const runtime = useRuntimeStore()
  if (authRequired && !auth.token) {
    auth.returnUrl = to.fullPath
    return '/login'
  }
  runtime.navigation = to.name as string
  runtime.routePath = to.path as string

  /* If entering settings page, save previous route to get it back */
  if (
    from.name !== undefined &&
    runtime.beforeSettingsRoute === undefined &&
    'settings' in to.meta
  ) {
    runtime.beforeSettingsRoute = from
  }
})

export default router
