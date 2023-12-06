<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import type { Ref } from 'vue'
import { useRouter } from 'vue-router'
import { useGatewayAPI, AuthenticationError } from '@/composables/GatewayAPI'
import type { ClusterQos } from '@/composables/GatewayAPI'
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
const qos: Ref<Array<ClusterQos>> = ref([])

const runtimeStore = useRuntimeStore()

function reportAuthenticationError(error: AuthenticationError) {
  runtimeStore.reportError(`Authentication error: ${error.message}`)
  router.push({ name: 'login' })
}

function reportOtherError(error: Error) {
  runtimeStore.reportError(error.message)
}

async function getClusterQos(cluster: string) {
  try {
    qos.value = await gateway.qos(cluster)
  } catch (error: any) {
    if (error instanceof AuthenticationError) {
      reportAuthenticationError(error)
    } else {
      reportOtherError(error)
    }
  }
}

function startClusterQosPoller(cluster: string) {
  console.log(`Start qos poller for cluster ${cluster}`)
  getClusterQos(cluster)
  interval = setInterval(getClusterQos, 5000, cluster)
}

function stopClusterQosPoller(cluster: string) {
  console.log(`Stop qos poller for cluster ${cluster}`)
  clearInterval(interval)
}

watch(
  () => props.cluster,
  (newCluster, oldCluster) => {
    stopClusterQosPoller(oldCluster)
    console.log(`Updating qos for cluster ${newCluster}`)
    qos.value = []
    startClusterQosPoller(newCluster)
  }
)

onMounted(() => {
  startClusterQosPoller(props.cluster)
})

onUnmounted(() => {
  stopClusterQosPoller(props.cluster)
})
</script>

<template>
  <ClusterMainLayout :cluster="props.cluster" title="QOS">
    <ul v-for="_qos in qos" :key="_qos.name">
      <li>{{ _qos.name }} ({{ _qos.description }})</li>
    </ul>
  </ClusterMainLayout>
</template>
