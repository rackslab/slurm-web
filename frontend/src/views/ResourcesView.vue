<script setup lang="ts">
import { useClusterDataPoller } from '@/composables/DataPoller'
import type { ClusterNode } from '@/composables/GatewayAPI'
import ClusterCanvas from '@/components/ClusterCanvas.vue'
import ClusterMainLayout from '@/components/ClusterMainLayout.vue'

const props = defineProps({
  cluster: {
    type: String,
    required: true
  }
})

const { data, unable } = useClusterDataPoller<ClusterNode[]>('nodes', 10000, props)
</script>

<template>
  <ClusterMainLayout :cluster="props.cluster" title="Resources">
    <div class="bg-white">
      <div class="mx-auto px-4 py-16 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900">Nodes</h1>
        <p class="mt-4 max-w-xl text-sm text-gray-700">Nodes available on cluster</p>
      </div>
      <ClusterCanvas :cluster="props.cluster" />
      <div v-if="unable">Unable to retrieve nodes information from cluster {{ props.cluster }}</div>
      <div v-else class="mt-8 flow-root">
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
                <tr v-for="node in data" :key="node.name">
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
