import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Ref } from 'vue'
import type { RouteLocation } from 'vue-router'
import type { ClusterPermissions } from '@/composables/GatewayAPI'

export class JobsViewFilter {
  name: string
  constructor(name: string) {
    this.name = name
  }
}

export class JobsViewSettings {
  sort: string = 'id'
  filters: JobsViewFilter[] = []

  restoreSortDefault(): void {
    this.sort = 'id'
  }
}

export class JobsRuntimeSettings {
  view: JobsViewSettings = new JobsViewSettings()
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

export const useRuntimeStore = defineStore('runtime', () => {
  const navigation: Ref<string> = ref('home')
  const routePath: Ref<string> = ref('/')
  const beforeSettingsRoute: Ref<RouteLocation | undefined> = ref(undefined)
  const jobs: Ref<JobsRuntimeSettings> = ref(new JobsRuntimeSettings())
  const errors: Ref<Array<RuntimeError>> = ref([])
  const notifications: Ref<Array<Notification>> = ref([])
  const availableClusters: Ref<Array<ClusterPermissions>> = ref(
    JSON.parse(localStorage.getItem('availableClusters') || '[]') as ClusterPermissions[]
  )
  const currentCluster: Ref<string | undefined> = ref()

  function addCluster(cluster: ClusterPermissions) {
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
    availableClusters,
    currentCluster,
    addCluster,
    checkClusterAvailable,
    addNotification,
    removeNotification,
    reportError
  }
})
