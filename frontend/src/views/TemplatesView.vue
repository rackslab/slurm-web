<!--
  Copyright (c) 2023-2024 Rackslab

  This file is part of Slurm-web.

  SPDX-License-Identifier: GPL-3.0-or-later
-->

<script setup lang="ts">
import ClusterMainLayout from '@/components/ClusterMainLayout.vue'
import { ChevronLeftIcon } from '@heroicons/vue/20/solid'

const props = defineProps({
  cluster: {
    type: String,
    required: true
  }
})
</script>

<template>
  <ClusterMainLayout
    :cluster="props.cluster"
    :viewDetails="[
      { titleView: 'Jobs', routeName: 'jobs' },
      { titleView: 'Templates', routeName: 'templates' }
    ]"
  >
    <router-link :to="{ name: 'jobs' }"
      ><button
        type="button"
        class="mb-16 mt-8 inline-flex items-center gap-x-2 rounded-md bg-slurmweb px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-slurmweb-dark focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slurmweb-dark"
      >
        <ChevronLeftIcon class="-ml-0.5 h-5 w-5" aria-hidden="true" />
        Back to resources
      </button></router-link
    >

    <div class="flex justify-center">
      <div class="flex flex-col pt-10">
        <p class="text-lg font-bold">Manage templates</p>
        <p>Edit or create jobs templates</p>

        <div
          class="mr-10 mt-10 flex min-h-[200px] w-[400px] flex-col rounded-lg border border-gray-200 bg-white shadow dark:border-gray-700 dark:bg-gray-800"
        >
          <div class="m-10">
            <div class="mb-4 flex h-fit">
              <h3 class="truncate text-sm font-medium text-gray-900">title</h3>
              <span
                class="ml-2 items-center rounded-full bg-green-50 px-1.5 py-0.5 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20"
                >Author</span
              >
            </div>
            <p class="mt-1 truncate text-sm text-gray-500">description</p>
          </div>
          <div class="flex-grow"></div>

          <div class="mt-4 w-full border-t border-gray-200 dark:border-gray-700">
            <button
              class="flex w-full items-center justify-center rounded-b-lg py-3 font-medium transition duration-200 ease-in-out hover:bg-slurmweb hover:text-white dark:bg-gray-700"
            >
              Select
              <ChevronRightIcon class="ml-1 h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </ClusterMainLayout>
</template>
