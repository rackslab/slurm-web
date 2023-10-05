<script setup lang="ts">
import { onMounted, onUnmounted, ref, resolveTransitionHooks } from 'vue'
import type { Ref } from 'vue'
import { useRouter, useRoute, onBeforeRouteUpdate } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRuntimeStore } from '@/stores/runtime'
import { useSlurmAPI } from '@/composables/SlurmAPI'
//import { useEventsSource } from '@/composables/EventsSource'
import type { SlurmJob } from '@/composables/SlurmAPI'
import { useHttp } from '@/plugins/http'
import { loadRuntimeConfiguration } from '@/plugins/runtimeConfiguration'
import JobsSorter from '@/components/JobsSorter.vue'
import JobStatusLabel from '@/components/JobStatusLabel.vue'

import {
  Dialog,
  DialogPanel,
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  Popover,
  PopoverButton,
  PopoverGroup,
  PopoverOverlay,
  PopoverPanel,
  TransitionChild,
  TransitionRoot
} from '@headlessui/vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import {
  ChevronDownIcon,
  PhoneIcon,
  PlayCircleIcon,
  RectangleGroupIcon
} from '@heroicons/vue/20/solid'
import {
  ChartPieIcon,
  CursorArrowRaysIcon,
  FingerPrintIcon,
  SquaresPlusIcon
} from '@heroicons/vue/24/outline'

const filters = [
  {
    id: 'state',
    name: 'State',
    options: [
      { value: 'completed', label: 'Completed', checked: false },
      { value: 'running', label: 'Running', checked: false },
      { value: 'pending', label: 'Pending', checked: true }
    ]
  },
  {
    id: 'users',
    name: 'Users',
    options: [
      { value: 'white', label: 'White', checked: false },
      { value: 'beige', label: 'Beige', checked: false },
      { value: 'blue', label: 'Blue', checked: false }
    ]
  },
  {
    id: 'accounts',
    name: 'Accounts',
    options: [
      { value: 's', label: 'S', checked: false },
      { value: 'm', label: 'M', checked: false },
      { value: 'l', label: 'L', checked: false }
    ]
  }
]
const activeFilters = [
  { value: 'objects', label: 'Objects' },
  { value: 'beige', label: 'color:Beige' }
]

const open = ref(false)
const route = useRoute()
const router = useRouter()
const http = useHttp()
const authStore = useAuthStore()
const runtimeStore = useRuntimeStore()
const slurmAPI = useSlurmAPI(http, authStore.token)
const rc = loadRuntimeConfiguration()
//const eventsSource = useEventsSource(rc.api_server, authStore.token)

let jobs: Array<SlurmJob> | null = null
const sortedJobs: Ref<Array<SlurmJob> | null> = ref(null)

let interval: number = 0

async function getJobs() {
  jobs = await slurmAPI.jobs()
  updateSortedJobs()
}

/*
async function streamJobs() {
  try {
    await eventsSource.listen('/streams/jobs')
  } catch(error) {
    console.log(error)
  }
}
*/

function sortJobs() {
  router.push({ name: 'jobs', query: { sort: runtimeStore.jobs.view.sort } })
  updateSortedJobs()
}

function updateSortedJobs() {
  if (jobs) {
    sortedJobs.value = jobs.sort((a, b) => {
      if (runtimeStore.jobs.view.sort == 'user') {
        if (a.user_name > b.user_name) {
          return 1
        }
        if (a.user_name < b.user_name) {
          return -1
        }
        return 0
      } else if (runtimeStore.jobs.view.sort == 'state') {
        if (a.job_state > b.job_state) {
          return 1
        }
        if (a.job_state < b.job_state) {
          return -1
        }
        return 0
      } else {
        // by default, sort by id
        if (a.id > b.id) {
          return 1
        }
        if (a.id < b.id) {
          return -1
        }
        return 0
      }
    })
  }
}

onMounted(() => {
  getJobs()
  interval = setInterval(getJobs, 3000)
  if (route.query.sort) {
    runtimeStore.jobs.view.sort = route.query.sort as string
  }
  //streamJobs()
})

onUnmounted(() => {
  clearInterval(interval)
})

onBeforeRouteUpdate(async (to, from) => {
  // When view route is updated without sort criteria, restore default sort
  // criteria in runtime settings store.
  if (to.query.sort == null) {
    runtimeStore.jobs.view.restoreSortDefault()
  }
})
</script>

<template>
  <div class="bg-white">
    <!-- Mobile filter dialog -->
    <TransitionRoot as="template" :show="open">
      <Dialog as="div" class="relative z-40" @close="open = false">
        <TransitionChild
          as="template"
          enter="transition-opacity ease-linear duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="transition-opacity ease-linear duration-300"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div class="fixed inset-0 z-40 flex">
          <TransitionChild
            as="template"
            enter="transition ease-in-out duration-300 transform"
            enter-from="translate-x-full"
            enter-to="translate-x-0"
            leave="transition ease-in-out duration-300 transform"
            leave-from="translate-x-0"
            leave-to="translate-x-full"
          >
            <DialogPanel
              class="relative ml-auto flex h-full w-full max-w-xs flex-col overflow-y-auto bg-white py-4 pb-12 shadow-xl"
            >
              <div class="flex items-center justify-between px-4">
                <h2 class="text-lg font-medium text-gray-900">Filters</h2>
                <button
                  type="button"
                  class="-mr-2 flex h-10 w-10 items-center justify-center rounded-md bg-white p-2 text-gray-400"
                  @click="open = false"
                >
                  <span class="sr-only">Close menu</span>
                  <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                </button>
              </div>

              <!-- Filters -->
              <form class="mt-4">
                <Disclosure
                  as="div"
                  v-for="section in filters"
                  :key="section.name"
                  class="border-t border-gray-200 px-4 py-6"
                  v-slot="{ open }"
                >
                  <h3 class="-mx-2 -my-3 flow-root">
                    <DisclosureButton
                      class="flex w-full items-center justify-between bg-white px-2 py-3 text-sm text-gray-400"
                    >
                      <span class="font-medium text-gray-900">{{ section.name }}</span>
                      <span class="ml-6 flex items-center">
                        <ChevronDownIcon
                          :class="[open ? '-rotate-180' : 'rotate-0', 'h-5 w-5 transform']"
                          aria-hidden="true"
                        />
                      </span>
                    </DisclosureButton>
                  </h3>
                  <DisclosurePanel class="pt-6">
                    <div class="space-y-6">
                      <div
                        v-for="(option, optionIdx) in section.options"
                        :key="option.value"
                        class="flex items-center"
                      >
                        <input
                          :id="`filter-mobile-${section.id}-${optionIdx}`"
                          :name="`${section.id}[]`"
                          :value="option.value"
                          type="checkbox"
                          :checked="option.checked"
                          class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                        />
                        <label
                          :for="`filter-mobile-${section.id}-${optionIdx}`"
                          class="ml-3 text-sm text-gray-500"
                          >{{ option.label }}</label
                        >
                      </div>
                    </div>
                  </DisclosurePanel>
                </Disclosure>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>

    <div class="mx-auto px-4 py-16 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">Jobs</h1>
      <p class="mt-4 max-w-xl text-sm text-gray-700">Jobs running on Slurm cluster</p>
    </div>

    <!-- Filters -->
    <section aria-labelledby="filter-heading" class="-mx-4 -my-2 sm:-mx-6 lg:-mx-8">
      <h2 id="filter-heading" class="sr-only">Filters</h2>

      <div class="border-b border-gray-200 bg-white pb-4">
        <div class="mx-auto flex items-center justify-between px-4 sm:px-6 lg:px-8">
          <JobsSorter @sort="sortJobs" />

          <button
            type="button"
            class="inline-block text-sm font-medium text-gray-700 hover:text-gray-900"
            @click="open = true"
          >
            Filters
          </button>
        </div>
      </div>

      <!-- Active filters -->
      <div class="bg-gray-100">
        <div class="mx-auto px-4 py-3 sm:flex sm:items-center sm:px-6 lg:px-8">
          <h3 class="text-sm font-medium text-gray-500">
            Filters
            <span class="sr-only">, active</span>
          </h3>

          <div aria-hidden="true" class="hidden h-5 w-px bg-gray-300 sm:ml-4 sm:block" />

          <div class="mt-2 sm:ml-4 sm:mt-0">
            <div class="-m-1 flex flex-wrap items-center">
              <span
                v-for="activeFilter in activeFilters"
                :key="activeFilter.value"
                class="m-1 inline-flex items-center rounded-full border border-gray-200 bg-white py-1.5 pl-3 pr-2 text-sm font-medium text-gray-900"
              >
                <span>{{ activeFilter.label }}</span>
                <button
                  type="button"
                  class="ml-1 inline-flex h-4 w-4 flex-shrink-0 rounded-full p-1 text-gray-400 hover:bg-gray-200 hover:text-gray-500"
                >
                  <span class="sr-only">Remove filter for {{ activeFilter.label }}</span>
                  <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                    <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
                  </svg>
                </button>
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

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
                  State
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  #ID
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  User
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Account
                </th>
                <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Partition
                </th>
                <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6 lg:pr-8">
                  <span class="sr-only">Edit</span>
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 bg-white">
              <tr v-for="job in sortedJobs" :key="job.id">
                <td
                  class="whitespace-nowrap py-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6 lg:pl-8"
                >
                  <JobStatusLabel :status="job.job_state" />
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ job.job_id }}</td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                  {{ job.user_name }}
                </td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ job.account }}</td>
                <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                  {{ job.partition }}
                </td>
                <td
                  class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6 lg:pr-8"
                >
                  <a href="#" class="text-indigo-600 hover:text-indigo-900">
                    Edit
                    <span class="sr-only">, {{ job.job_id }}</span>
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
