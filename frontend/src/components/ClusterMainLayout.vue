<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import type { RouteRecordName } from 'vue-router'
import { onMounted, ref } from 'vue'
import type { Ref } from 'vue'
import { useRuntimeStore } from '@/stores/runtime'
import { useAuthStore } from '@/stores/auth'
import {
  Popover,
  PopoverButton,
  PopoverPanel
} from '@headlessui/vue'
import { Bars3Icon, BellIcon, ArrowRightOnRectangleIcon } from '@heroicons/vue/24/outline'
import { ChevronDownIcon, ChevronRightIcon } from '@heroicons/vue/20/solid'
import MainMenu from '@/components/MainMenu.vue'

const props = defineProps({
  cluster: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  }
})

const route = useRoute()

const userNavigation = [
  { name: 'Jobs', route: 'jobs' },
  { name: 'Sign out', route: 'signout' }
]

const sidebarOpen = ref(false)

const clusterNotFound: Ref<boolean> = ref(false)
const runtimeStore = useRuntimeStore()
const authStore = useAuthStore()

onMounted(() => {
  if (!runtimeStore.checkClusterAvailable(props.cluster)) {
    clusterNotFound.value = true
  }
})
</script>

<template>
  <MainMenu />
  <div class="lg:pl-72">
    <div
      class="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b lg:px-4 border-gray-200 bg-white shadow-sm sm:gap-x-6"
    >
      <button
        type="button"
        class="-m-2.5 p-2.5 text-gray-700 lg:hidden"
        @click="sidebarOpen = true"
      >
        <span class="sr-only">Open sidebar</span>
        <Bars3Icon class="h-6 w-6" aria-hidden="true" />
      </button>

      <!-- Separator -->
      <div class="h-6 w-px bg-gray-900/10 lg:hidden" aria-hidden="true" />

      <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <div class="relative flex flex-1 mt-1 items-center">
          <Popover class="relative">
            <PopoverButton
              class="inline-flex items-center gap-x-1 font-bold leading-6 text-transparent hover:text-gray-400 rounded p-3 hover:bg-slurmweb-light"
            >
              <ChevronDownIcon class="h-5 w-5" aria-hidden="true" />
              <span class="text-gray-700 hover:text-gray-900">{{ props.cluster }}</span>
            </PopoverButton>

            <transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100 translate-y-0"
              leave-to-class="opacity-0 translate-y-1"
            >
              <PopoverPanel
                v-slot="{ close }"
                class="absolute left-0 z-10 mt-5 flex w-screen max-w-max px-0"
              >
                <div
                  class="w-screen max-w-md flex-auto overflow-hidden rounded-3xl bg-white text-sm leading-6 shadow-lg ring-1 ring-gray-900/5"
                >
                  <div class="p-4">
                    <div
                      v-for="cluster in runtimeStore.availableClusters"
                      :key="cluster.name"
                      class="group relative flex gap-x-6 rounded-lg p-4 hover:bg-gray-50"
                    >
                      <div
                        class="mt-1 flex h-11 w-11 flex-none items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white"
                      >
                        <component
                          :is="cluster.name"
                          class="h-6 w-6 text-gray-600 group-hover:text-indigo-600"
                          aria-hidden="true"
                        />
                      </div>
                      <div>
                        <RouterLink
                          :to="{
                            name: route.name as RouteRecordName,
                            params: { cluster: cluster.name },
                            query: route.query
                          }"
                          class="font-semibold text-gray-900"
                          @click="close()"
                        >
                          {{ cluster.name }}
                          <span class="absolute inset-0" />
                        </RouterLink>
                        <p class="mt-1 text-gray-600">{{ cluster.name }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </PopoverPanel>
            </transition>
          </Popover>
          <ChevronRightIcon class="h-5 w-10 flex-shrink-0 text-gray-400" aria-hidden="true" />
          {{ props.title }}
        </div>
        <div class="flex items-center gap-x-4 lg:gap-x-6">
          <!-- Separator -->
          <div class="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10" aria-hidden="true" />

          <!-- Profile -->
          <span class="hidden lg:flex lg:items-center">
            <span class="ml-4 text-sm font-semibold leading-6 text-gray-900" aria-hidden="true">
              {{ authStore.fullname }}
            </span>
          </span>

          <!-- Signout button -->
          <RouterLink :to="{ name: 'signout' }" custom v-slot="{ navigate }">
            <button @click="navigate" role="link" class="lg:-m-2.5 p-2.5 text-gray-400 hover:text-gray-500">
              <ArrowRightOnRectangleIcon class="h-6 w-6"/>
            </button>
          </RouterLink>
        </div>
      </div>
    </div>

    <main class="py-10">
      <div class="px-4 sm:px-6 lg:px-8">
        <div v-if="clusterNotFound">Cluster not found</div>
        <div v-else class="home">
          <slot></slot>
        </div>
      </div>
    </main>
  </div>
</template>
