<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import type { Ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRuntimeStore } from '@/stores/runtime'
import ClusterMainLayout from '@/components/ClusterMainLayout.vue'
import type { ClusterJob } from '@/composables/GatewayAPI'
import { useGatewayAPI, AuthenticationError, PermissionError } from '@/composables/GatewayAPI'

const props = defineProps({
  cluster: {
    type: String,
    required: true
  },
  id: {
    type: Number,
    required: true
  }
})

interface ClusterPoller {
  timeout: number
  stop: boolean
}

const pollers: Record<string, ClusterPoller> = {}
const router = useRouter()
const gateway = useGatewayAPI()
const runtimeStore = useRuntimeStore()
const unable: Ref<Boolean> = ref(false)
const job: Ref<ClusterJob | undefined> = ref()

function reportAuthenticationError(error: AuthenticationError, cluster: string) {
  runtimeStore.reportError(`Authentication error: ${error.message}`)
  router.push({ name: 'login' })
}

function reportPermissionError(error: PermissionError, cluster: string, id: number) {
  runtimeStore.reportError(`Permission error: ${error.message}`)
  stopClusterJobPoller(cluster, id)
  unable.value = true
}

function reportOtherError(error: Error, cluster: string) {
  runtimeStore.reportError(`Server error: ${error.message}`)
  unable.value = true
}

async function getClusterJob(cluster: string, id: number) {
  try {
    unable.value = false
    job.value = await gateway.job(cluster, id)
  } catch (error: any) {
    /*
     * Skip errors received lately from other clusters, after the view cluster
     * parameter has changed.
     */
    if (cluster == props.cluster) {
      if (error instanceof AuthenticationError) {
        reportAuthenticationError(error, cluster)
      } else if (error instanceof PermissionError) {
        reportPermissionError(error, cluster, id)
      } else {
        reportOtherError(error, cluster)
      }
    }
  }
}
async function startClusterJobPoller(cluster: string, id: number) {
  console.log(`Polling job for job ${id} on cluster ${cluster}`)
  const key = `${cluster}-${id}`
  if (!(key in pollers)) {
    pollers[key] = { timeout: -1, stop: false }
  } else {
    pollers[key].stop = false
  }
  await getClusterJob(cluster, id)
  if (cluster == props.cluster && !pollers[key].stop) {
    pollers[key].timeout = setTimeout(startClusterJobPoller, 5000, cluster, id)
  }
}

function stopClusterJobPoller(cluster: string, id: number) {
  console.log(`Stop job poller for job ${id} on cluster ${cluster}`)
  const key = `${cluster}-${id}`
  pollers[key].stop = true
  clearTimeout(pollers[key].timeout)
  gateway.abort()
}

onMounted(() => {
  startClusterJobPoller(props.cluster, props.id)
})

onUnmounted(() => {
  stopClusterJobPoller(props.cluster, props.id)
})
</script>

<template>
  <ClusterMainLayout :cluster="cluster" :title="`Job ${id}`">
    <div class="bg-white">Job {{ id }}</div>
    <div v-if="job">
      <div v-for="(value, property) in job">{{ property }}: {{ value }}</div>
    </div>
  </ClusterMainLayout>
</template>
