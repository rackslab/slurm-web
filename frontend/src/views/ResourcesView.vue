<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import type { Ref } from 'vue'
import { useRuntimeStore } from '@/stores/runtime'
import { useRouter } from 'vue-router'
import { useGatewayAPI, AuthenticationError } from '@/composables/GatewayAPI'
import type { ClusterNode } from '@/composables/GatewayAPI'
import ClusterCanvas from '@/components/ClusterCanvas.vue'
import ClusterMainLayout from '@/components/ClusterMainLayout.vue'

const props = defineProps({
  cluster: {
    type: String,
    required: true
  }
})

const runtimeStore = useRuntimeStore()
const nodes: Ref<Array<ClusterNode>> = ref([])
const canvas: Ref<HTMLCanvasElement | null> = ref(null)
const router = useRouter()
const gateway = useGatewayAPI()

let interval: number = 0

function reportAuthenticationError(error: AuthenticationError) {
  runtimeStore.reportError(`Authentication error: ${error.message}`)
  router.push({ name: 'login' })
}

function reportOtherError(error: Error) {
  console.log(`Error: ${error.message}`)
}

async function getClusterNodes(cluster: string) {
  try {
    nodes.value = await gateway.nodes(cluster)
  } catch (error: any) {
    if (error instanceof AuthenticationError) {
      reportAuthenticationError(error)
    } else {
      reportOtherError(error)
    }
  }
}

function startClusterNodesPoller(cluster: string) {
  console.log(`Start nodes poller for cluster ${cluster}`)
  getClusterNodes(cluster)
  interval = setInterval(getClusterNodes, 5000, cluster)
}

function stopClusterNodesPoller(cluster: string) {
  console.log(`Stop nodes poller for cluster ${cluster}`)
  clearInterval(interval)
}

watch(
  () => props.cluster,
  (newCluster, oldCluster) => {
    stopClusterNodesPoller(oldCluster)
    console.log(`Updating nodes for cluster ${newCluster}`)
    nodes.value = []
    startClusterNodesPoller(newCluster)
  }
)

onMounted(() => {
  startClusterNodesPoller(props.cluster)
})

onUnmounted(() => {
  stopClusterNodesPoller(props.cluster)
})
</script>

<template>
  <ClusterMainLayout :cluster="props.cluster" title="Resources">
    <div class="bg-white">
      <div class="mx-auto px-4 py-16 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900">Nodes</h1>
        <p class="mt-4 max-w-xl text-sm text-gray-700">Nodes available on cluster</p>
      </div>
      <ClusterCanvas />
      <div class="mt-8 flow-root">
        <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="inline-block min-w-full py-2 align-middle">
            <table class="min-w-full divide-y divide-gray-300">
              <thead>
                <tr>
                  <th
                    scope="col"
                    class="w-12 py-3.5 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6 lg:pl-8"
                  >
                    Nodename
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                    Cores
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                    Memory
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                    State
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                    Partitions
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 bg-white">
                <tr v-for="node in nodes" :key="node.id">
                  <td
                    class="whitespace-nowrap py-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6 lg:pl-8"
                  >
                    {{ node.name }}
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {{ node.cpus }} x {{ node.cores }}
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {{ node.real_memory }}
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {{ node.state }}
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {{ node.partitions }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </ClusterMainLayout>
</template>
