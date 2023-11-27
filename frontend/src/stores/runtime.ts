import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Ref } from 'vue'

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

type ClusterStatus = 'AVAILABLE' | 'UNAVAILABLE'

class Cluster {
  name: string
  status: ClusterStatus

  constructor(name: string, status: ClusterStatus) {
    this.name = name
    this.status = status
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

interface RuntimeError {
  message: string
}

export const useRuntimeStore = defineStore('runtime', () => {

  const navigation: Ref<string> = ref('home')
  const jobs: Ref<JobsRuntimeSettings> = ref(new JobsRuntimeSettings())
  const errors: Ref<Array<RuntimeError>> = ref([])
  const notifications: Ref<Array<Notification>> = ref([])
  const availableClusters: Ref<Array<Cluster>> = ref(JSON.parse(localStorage.getItem('availableClusters') || "[]") as Cluster[])
  const currentCluster: Ref<string | undefined> = ref()

  function addCluster(name: string) {
    availableClusters.value.push(new Cluster(name, 'AVAILABLE'))
    localStorage.setItem("availableClusters", JSON.stringify(availableClusters.value));
  }

  function checkClusterAvailable(name: string): boolean {
    return (availableClusters.value.filter((cluster) => cluster.name === name).length) > 0
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
    errors.value.push({ message: message })
    // Do not store more than 100 errors
    if (errors.value.length > 100) {
      errors.value = errors.value.slice(errors.value.length - 100)
    }
    addNotification(new Notification('ERROR', message, 5))
  }
  return {
    navigation,
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
