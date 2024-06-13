<!--
  Copyright (c) 2023-2024 Rackslab

  This file is part of Slurm-web.

  SPDX-License-Identifier: GPL-3.0-or-later
-->

<script setup lang="ts">
import { ChevronRightIcon } from '@heroicons/vue/20/solid'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  templateAuthor: {
    type: Boolean
  }
})
</script>

<template>
  <div
    class="mr-10 mt-10 flex min-h-[200px] w-[400px] flex-col rounded-lg border border-gray-200 bg-white shadow dark:border-gray-700 dark:bg-gray-800"
  >
    <div class="m-10">
      <div class="mb-4 flex h-fit">
        <h3 class="truncate text-sm font-medium text-gray-900">{{ props.title }}</h3>
        <span
          v-if="templateAuthor"
          class="ml-2 items-center rounded-full bg-green-50 px-1.5 py-0.5 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20"
          >Author</span
        >
      </div>
      <p class="mt-1 truncate text-sm text-gray-500">{{ props.description }}</p>
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
</template>
