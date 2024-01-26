import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Ref } from 'vue'
import type { RouteLocation } from 'vue-router'
import type { ClusterDescription, ClusterJob } from '@/composables/GatewayAPI'

interface JobsViewFilters {
  states: string[]
  users: string[]
  accounts: string[]
}

interface JobsQueryParameters {
  sort?: string
  states?: string
  users?: string
  accounts?: string
  page?: number
}

export class JobsViewSettings {
  sort: string = 'id'
  page: number = 1
  filters: JobsViewFilters = { states: [], users: [], accounts: [] }

  restoreSortDefault(): void {
    this.sort = 'id'
  }
  emptyFilters(): boolean {
    return (
      this.filters.states.length == 0 &&
      this.filters.users.length == 0 &&
      this.filters.accounts.length == 0
    )
  }
  matchesFilters(job: ClusterJob): boolean {
    if (this.emptyFilters()) {
      return true
    }
    if (this.filters.states.length != 0) {
      if (
        !this.filters.states.some((state) => {
          return state.toLocaleLowerCase() == job.job_state.toLocaleLowerCase()
        })
      ) {
        return false
      }
    }
    if (this.filters.users.length != 0) {
      if (
        !this.filters.users.some((user) => {
          return user.toLocaleLowerCase() == job.user_name.toLocaleLowerCase()
        })
      ) {
        return false
      }
    }
    if (this.filters.accounts.length != 0) {
      if (
        !this.filters.accounts.some((account) => {
          return account.toLocaleLowerCase() == job.account.toLocaleLowerCase()
        })
      ) {
        return false
      }
    }
    return true
  }
  query(): JobsQueryParameters {
    const result: JobsQueryParameters = {}
    if (this.page != 1) {
      result.page = this.page
    }
    if (this.sort != 'id') {
      result.sort = this.sort
    }
    if (this.filters.states.length > 0) {
      result.states = this.filters.states.join()
    }
    if (this.filters.users.length > 0) {
      result.users = this.filters.users.join()
    }
    if (this.filters.accounts.length > 0) {
      result.accounts = this.filters.accounts.join()
    }
    return result
  }
}

type NotificationType = 'INFO' | 'ERROR'

class Notification {
  id: number
  type: NotificationType
  message: string
  timeout: number
  constructor(type: NotificationType, message: string, timeout: number) {
    this.id = Date.now()
    this.type = type
    this.message = message
    this.timeout = timeout
  }
}

class RuntimeError {
  timestamp: Date
  route: string
  message: string
  constructor(route: string, message: string) {
    this.timestamp = new Date()
    this.route = route
    this.message = message
  }
}

export interface RuntimeStore {
  reportError: CallableFunction
}

export const useRuntimeStore = defineStore('runtime', () => {
  const navigation: Ref<string> = ref('home')
  const routePath: Ref<string> = ref('/')
  const beforeSettingsRoute: Ref<RouteLocation | undefined> = ref(undefined)
  const jobs: Ref<JobsViewSettings> = ref(new JobsViewSettings())
  const errors: Ref<Array<RuntimeError>> = ref([])
  const notifications: Ref<Array<Notification>> = ref([])
  const sidebarOpen: Ref<boolean> = ref(false)

  const availableClusters: Ref<Array<ClusterDescription>> = ref(
    JSON.parse(localStorage.getItem('availableClusters') || '[]') as ClusterDescription[]
  )
  const currentCluster: Ref<string | undefined> = ref()

  function addCluster(cluster: ClusterDescription) {
    availableClusters.value.push(cluster)
    localStorage.setItem('availableClusters', JSON.stringify(availableClusters.value))
  }

  function checkClusterAvailable(name: string): boolean {
    return availableClusters.value.filter((cluster) => cluster.name === name).length > 0
  }

  function addNotification(notification: Notification) {
    notifications.value.push(notification)
    setTimeout(removeNotification, notification.timeout * 1000, notification)
  }

  function removeNotification(searched: Notification) {
    console.log(`notification ${searched.id} is removed`)
    notifications.value = notifications.value.filter(
      (notification) => notification.id != searched.id
    )
  }

  function reportError(message: string) {
    errors.value.push(new RuntimeError(routePath.value, message))
    // Do not store more than 100 errors
    if (errors.value.length > 100) {
      errors.value = errors.value.slice(errors.value.length - 100)
    }
    addNotification(new Notification('ERROR', message, 5))
  }
  return {
    navigation,
    routePath,
    beforeSettingsRoute,
    jobs,
    errors,
    notifications,
    sidebarOpen,
    availableClusters,
    currentCluster,
    addCluster,
    checkClusterAvailable,
    addNotification,
    removeNotification,
    reportError
  }
})
