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

export const useRuntimeStore = defineStore('runtime', () => {
  const navigation: Ref<string> = ref('home')
  const jobs: Ref<JobsRuntimeSettings> = ref(new JobsRuntimeSettings())
  return { navigation, jobs }
})
