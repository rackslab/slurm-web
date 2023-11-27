<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useRuntimeStore } from '@/stores/runtime'
import { ChevronRightIcon } from '@heroicons/vue/20/solid'

const runtimeStore = useRuntimeStore()
</script>

<template>
  <main>
    <section class="bg-gray-50 dark:bg-gray-900">
      <div class="flex flex-col h-screen justify-center items-center gap-y-6">
      <h1 class="w-[50%] text-left text-lg">Select a cluster</h1>
      <ul
        role="list"
        class="w-[50%] divide-y divide-gray-100 overflow-hidden bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl"
      >
        <li
          v-for="cluster in runtimeStore.availableClusters"
          :key="cluster.name"
          class="relative flex justify-between gap-x-6 px-4 py-5 hover:bg-gray-50 sm:px-6"
        >
          <div class="flex min-w-0 gap-x-4">
            <div class="min-w-0 flex-auto">
              <p class="text-sm font-semibold leading-6 text-gray-900">
                <RouterLink :to="{ name: 'dashboard', params: { cluster: cluster.name } }">
                  <span class="absolute inset-x-0 -top-px bottom-0" />
                  {{ cluster.name }}
                </RouterLink>
              </p>
              <p class="mt-1 flex text-xs leading-5 text-gray-500">
                <a :href="`mailto:${cluster.name}`" class="relative truncate hover:underline">{{
                  cluster.name
                }}</a>
              </p>
            </div>
          </div>
          <div class="flex shrink-0 items-center gap-x-4">
            <div class="hidden sm:flex sm:flex-col sm:items-end">
              <p class="text-sm leading-6 text-gray-900">{{ cluster.name }}</p>
              <div v-if="cluster.status == 'AVAILABLE'" class="mt-1 flex items-center gap-x-1.5">
                <div class="flex-none rounded-full bg-emerald-500/20 p-1">
                  <div class="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                </div>
                <p class="text-xs leading-5 text-gray-500">Online</p>
              </div>
            </div>
            <ChevronRightIcon class="h-5 w-5 flex-none text-gray-400" aria-hidden="true" />
          </div>
        </li>
      </ul>
      </div>
      
    </section>
  </main>
</template>
