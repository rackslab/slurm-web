<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import type { Ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  useGatewayAPI,
  AuthenticationError,
  PermissionError,
  ClusterStats
} from '@/composables/GatewayAPI'
import { useRuntimeStore } from '@/stores/runtime'
import ClusterMainLayout from '@/components/ClusterMainLayout.vue'

const props = defineProps({
  cluster: {
    type: String,
    required: true
  }
})

const router = useRouter()
const gateway = useGatewayAPI()

const stats: Ref<ClusterStats | undefined> = ref()
const unable: Ref<Boolean> = ref(false)

const runtimeStore = useRuntimeStore()

interface ClusterPoller {
  timeout: number
  stop: boolean
}

const pollers: Record<string, ClusterPoller> = {}

function reportAuthenticationError(error: AuthenticationError, cluster: string) {
  runtimeStore.reportError(`Authentication error: ${error.message}`)
  router.push({ name: 'login' })
}

function reportPermissionError(error: PermissionError, cluster: string) {
  runtimeStore.reportError(`Permission error: ${error.message}`)
  stopClusterStatsPoller(cluster)
  unable.value = true
}

function reportOtherError(error: Error, cluster: string) {
  runtimeStore.reportError(`Server error: ${error.message}`)
  unable.value = true
}

async function getClusterStats(cluster: string) {
  try {
    unable.value = false
    stats.value = await gateway.stats(cluster)
  } catch (error: any) {
    /*
     * Skip errors received lately from other clusters, after the view cluster
     * parameter has changed.
     */
    if (cluster == props.cluster) {
      if (error instanceof AuthenticationError) {
        reportAuthenticationError(error, cluster)
      } else if (error instanceof PermissionError) {
        reportPermissionError(error, cluster)
      } else {
        reportOtherError(error, cluster)
      }
    }
  }
}

async function startClusterStatsPoller(cluster: string) {
  console.log(`Polling stats for cluster ${cluster}`)
  if (!(cluster in pollers)) {
    pollers[cluster] = { timeout: -1, stop: false }
  } else {
    pollers[cluster].stop = false
  }
  await getClusterStats(cluster)
  if (cluster == props.cluster && !pollers[cluster].stop) {
    pollers[cluster].timeout = setTimeout(startClusterStatsPoller, 5000, cluster)
  }
}

function stopClusterStatsPoller(cluster: string) {
  console.log(`Stop stats poller for cluster ${cluster}`)
  pollers[cluster].stop = true
  clearTimeout(pollers[cluster].timeout)
  gateway.abort()
}

watch(
  () => props.cluster,
  (newCluster, oldCluster) => {
    stopClusterStatsPoller(oldCluster)
    console.log(`Updating stats for cluster ${newCluster}`)
    stats.value = undefined
    startClusterStatsPoller(newCluster)
  }
)

onMounted(() => {
  startClusterStatsPoller(props.cluster)
})

onUnmounted(() => {
  stopClusterStatsPoller(props.cluster)
})
</script>

<template>
  <ClusterMainLayout :cluster="props.cluster" title="Dashboard">
    <div class="mx-auto max-w-7xl bg-white">
      <div v-if="unable">Unable to display data from cluster {{ props.cluster }}</div>
      <div v-else class="grid grid-cols-1 gap-px bg-gray-200 sm:grid-cols-2 lg:grid-cols-4">
        <div class="bg-white px-4 py-6 sm:px-6 lg:px-8">
          <p class="text-sm font-medium leading-6 text-gray-400">Nodes</p>
          <span v-if="stats" class="text-4xl font-semibold tracking-tight text-gray-600">
            {{ stats.resources.nodes }}
          </span>
          <div v-else class="animate-pulse flex space-x-4">
            <div class="rounded-full bg-slate-200 h-10 w-10"></div>
          </div>
        </div>
        <div class="bg-white px-4 py-6 sm:px-6 lg:px-8">
          <p class="text-sm font-medium leading-6 text-gray-400">Cores</p>
          <span v-if="stats" class="text-4xl font-semibold tracking-tight text-gray-600">
            {{ stats.resources.cores }}
          </span>
          <div v-else class="animate-pulse flex space-x-4">
            <div class="rounded-full bg-slate-200 h-10 w-10"></div>
          </div>
        </div>
        <div class="bg-white px-4 py-6 sm:px-6 lg:px-8">
          <p class="text-sm font-medium leading-6 text-gray-400">Running jobs</p>
          <span v-if="stats" class="text-4xl font-semibold tracking-tight text-gray-600">
            {{ stats.jobs.running }}
          </span>
          <div v-else class="animate-pulse flex space-x-4">
            <div class="rounded-full bg-slate-200 h-10 w-10"></div>
          </div>
        </div>
        <div class="bg-white px-4 py-6 sm:px-6 lg:px-8">
          <p class="text-sm font-medium leading-6 text-gray-400">Total jobs</p>
          <span v-if="stats" class="text-4xl font-semibold tracking-tight text-gray-600">
            {{ stats.jobs.total }}
          </span>
          <div v-else class="animate-pulse flex space-x-4">
            <div class="rounded-full bg-slate-100 h-10 w-10"></div>
          </div>
        </div>
      </div>
    </div>
  </ClusterMainLayout>
</template>
