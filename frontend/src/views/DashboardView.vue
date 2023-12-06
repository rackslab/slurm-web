<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import type { Ref } from 'vue'
import { useRouter } from 'vue-router'
import { useGatewayAPI, AuthenticationError, ClusterStats } from '@/composables/GatewayAPI'
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

let interval: number = 0
const stats: Ref<ClusterStats | undefined> = ref()

const runtimeStore = useRuntimeStore()

function reportAuthenticationError(error: AuthenticationError) {
  runtimeStore.reportError(`Authentication error: ${error.message}`)
  router.push({ name: 'login' })
}

function reportOtherError(error: Error) {
  console.log(`Error: ${error.message}`)
}

async function getClusterStats(cluster: string) {
  try {
    stats.value = await gateway.stats(cluster)
  } catch (error: any) {
    if (error instanceof AuthenticationError) {
      reportAuthenticationError(error)
    } else {
      reportOtherError(error)
    }
  }
}

function startClusterStatsPoller(cluster: string) {
  console.log(`Start stats poller for cluster ${cluster}`)
  getClusterStats(cluster)
  interval = setInterval(getClusterStats, 5000, cluster)
}

function stopClusterStatsPoller(cluster: string) {
  console.log(`Stop stats poller for cluster ${cluster}`)
  clearInterval(interval)
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
      <div class="grid grid-cols-1 gap-px bg-gray-200 sm:grid-cols-2 lg:grid-cols-4">
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
